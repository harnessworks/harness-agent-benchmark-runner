#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TASK_DIR = REPO_ROOT / "benchmarks" / "tasks" / "flask-hidden"
DEFAULT_AGENT = f"{sys.executable} {REPO_ROOT / 'examples' / 'agents' / 'codex_exec_agent.py'}"
LEGACY_ARMS = ("no-harness", "yes-harness")
THREE_ARMS = ("bare", "workflow-only", "memory-harness")
KNOWN_ARM_SUFFIXES = THREE_ARMS + LEGACY_ARMS


@dataclass(frozen=True)
class TaskPair:
    task_id: str
    no_harness: Path
    yes_harness: Path


@dataclass(frozen=True)
class TaskGroup:
    task_id: str
    arms: dict[str, Path]


@dataclass(frozen=True)
class SuiteSpec:
    suite_id: str
    task_dir: Path
    arms: tuple[str, ...] = ()
    split: str | None = None
    prompt_variant: str | None = None


@dataclass(frozen=True)
class ScheduledRun:
    round_number: int
    task_id: str
    group: str
    task_path: Path


@dataclass(frozen=True)
class ScheduledRunResult:
    index: int
    total: int
    item: ScheduledRun
    returncode: int
    stdout: str
    stderr: str


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    suite = load_suite(args.suite) if args.suite else None
    if suite is not None:
        args.task_dir = suite.task_dir
        if args.arms is None and suite.arms:
            args.arms = ",".join(suite.arms)
    args.task_dir = args.task_dir.resolve()
    args.repeats = args.repeats or default_repeats(args.mode)
    args.task_limit = default_task_limit(args.mode) if args.task_limit is None else args.task_limit
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if args.results is None:
        args.results = REPO_ROOT / "results" / f"hidden-flask-ab-{args.mode}-{stamp}"
    if args.workspace is None:
        args.workspace = REPO_ROOT / "runs" / f"hidden-flask-ab-{args.mode}-{stamp}"

    try:
        required_arms = parse_arms(args.arms)
        groups = load_task_groups(args.task_dir, required_arms=required_arms)
        validate_task_groups(groups)
        selected_groups = groups[: args.task_limit] if args.task_limit else groups
        validate_run_shape(args, selected_groups)
        schedule = build_group_schedule(
            selected_groups,
            args.repeats,
            args.arm_order or arm_order_from_pair_order(args.pair_order),
        )
        print_plan(args, selected_groups, schedule, suite)
        if not args.execute:
            print("\nDry run only. Re-run with --execute to start live agent benchmark runs.")
            return 0
        validate_live_execution(args, selected_groups)
        return execute_schedule(args, schedule)
    except BenchmarkPlanError as exc:
        print(f"benchmark plan error: {exc}", file=sys.stderr)
        return 2


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan and optionally execute the hidden-oracle Flask harness A/B benchmark.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--mode", choices=("pilot", "large"), default="pilot")
    parser.add_argument(
        "--suite",
        type=Path,
        help="optional benchmark suite manifest; supplies task_dir, arms, and prompt-level metadata",
    )
    parser.add_argument("--task-dir", type=Path, default=DEFAULT_TASK_DIR)
    parser.add_argument(
        "--arms",
        help="comma-separated arms to require, for example bare,workflow-only,memory-harness",
    )
    parser.add_argument(
        "--task-limit",
        type=positive_int,
        help="limit task pairs; defaults to 4 for pilot and all task pairs for large",
    )
    parser.add_argument("--repeats", type=positive_int, help="override repeat count")
    parser.add_argument(
        "--pair-order",
        choices=("ab", "ba", "alternate"),
        default="alternate",
        help="A is no-harness, B is yes-harness",
    )
    parser.add_argument(
        "--arm-order",
        choices=("listed", "reverse", "rotate"),
        help="ordering strategy for all arms; defaults to --pair-order compatibility",
    )
    parser.add_argument("--agent-command", default=DEFAULT_AGENT)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--service-tier", default="priority")
    parser.add_argument(
        "--jobs",
        type=positive_int,
        default=1,
        help="maximum runner commands to execute concurrently",
    )
    parser.add_argument("--max-agent-timeout", type=positive_int, default=900)
    parser.add_argument("--max-cost-usd", type=non_negative_float, default=1.0)
    parser.add_argument(
        "--large-min-task-pairs",
        type=positive_int,
        default=8,
        help="minimum task-pair count required for --mode large",
    )
    parser.add_argument(
        "--allow-small-large",
        action="store_true",
        help="allow --mode large with fewer than --large-min-task-pairs task pairs",
    )
    parser.add_argument(
        "--allow-head-ref",
        action="store_true",
        help="allow live execution when a task repo.ref is HEAD",
    )
    parser.add_argument(
        "--allow-dirty-targets",
        action="store_true",
        help="allow live execution against dirty local target repositories",
    )
    parser.add_argument(
        "--show-all-commands",
        action="store_true",
        help="print every runner command in the planned schedule",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="actually run the benchmark; default is a no-cost dry-run plan",
    )
    return parser.parse_args(argv)


def default_repeats(mode: str) -> int:
    return 2 if mode == "pilot" else 10


def default_task_limit(mode: str) -> int | None:
    return 4 if mode == "pilot" else None


def load_suite(path: Path) -> SuiteSpec:
    suite_path = path.expanduser()
    if not suite_path.is_absolute():
        suite_path = (REPO_ROOT / suite_path).resolve()
    data = read_json(suite_path)
    suite_id = require_string(data, "id", suite_path)
    raw_task_dir = require_string(data, "task_dir", suite_path)
    task_dir = Path(raw_task_dir).expanduser()
    if not task_dir.is_absolute():
        task_dir = (suite_path.parent / task_dir).resolve()
    arms = tuple(string_list(data, "arms", suite_path))
    split = optional_string(data, "split", suite_path)
    prompt_variant = optional_string(data, "prompt_variant", suite_path)
    return SuiteSpec(
        suite_id=suite_id,
        task_dir=task_dir,
        arms=arms,
        split=split,
        prompt_variant=prompt_variant,
    )


def parse_arms(value: str | None) -> tuple[str, ...] | None:
    if value is None:
        return None
    arms = tuple(arm.strip() for arm in value.split(",") if arm.strip())
    if not arms:
        raise BenchmarkPlanError("--arms must name at least one arm")
    for arm in arms:
        if arm not in KNOWN_ARM_SUFFIXES:
            allowed = ", ".join(KNOWN_ARM_SUFFIXES)
            raise BenchmarkPlanError(f"unknown arm {arm!r}; allowed arms: {allowed}")
    if len(set(arms)) != len(arms):
        raise BenchmarkPlanError("--arms must not repeat an arm")
    return arms


def load_task_groups(task_dir: Path, required_arms: tuple[str, ...] | None = None) -> list[TaskGroup]:
    if not task_dir.exists():
        raise BenchmarkPlanError(f"task directory does not exist: {task_dir}")

    grouped: dict[str, dict[str, Path]] = {}
    for path in sorted(task_dir.glob("*.json")):
        arm = arm_suffix(path)
        if arm is None:
            continue
        data = read_json(path)
        task_id = require_string(data, "id", path)
        grouped.setdefault(task_id, {})
        if arm in grouped[task_id]:
            raise BenchmarkPlanError(f"duplicate {arm} task for {task_id}")
        grouped[task_id][arm] = path

    if not grouped:
        raise BenchmarkPlanError(f"no hidden Flask task groups found in {task_dir}")

    arms = required_arms or infer_required_arms(grouped)
    groups = []
    for task_id, arm_paths in sorted(grouped.items()):
        missing = [arm for arm in arms if arm not in arm_paths]
        if missing:
            raise BenchmarkPlanError(f"incomplete task group for {task_id}; missing: {', '.join(missing)}")
        groups.append(TaskGroup(task_id=task_id, arms={arm: arm_paths[arm] for arm in arms}))
    if not groups:
        raise BenchmarkPlanError(f"no complete hidden Flask task groups found in {task_dir}")
    return groups


def arm_suffix(path: Path) -> str | None:
    for suffix in sorted(KNOWN_ARM_SUFFIXES, key=len, reverse=True):
        if path.name.endswith(f"-{suffix}.json"):
            return suffix
    return None


def infer_required_arms(grouped: dict[str, dict[str, Path]]) -> tuple[str, ...]:
    observed = set().union(*(set(arms) for arms in grouped.values()))
    if set(THREE_ARMS).issubset(observed):
        return THREE_ARMS
    if set(LEGACY_ARMS).issubset(observed):
        return LEGACY_ARMS
    raise BenchmarkPlanError(
        "could not infer arms; pass --arms or use complete "
        "bare/workflow-only/memory-harness or no-harness/yes-harness task files"
    )


def load_task_pairs(task_dir: Path) -> list[TaskPair]:
    groups = load_task_groups(task_dir, required_arms=LEGACY_ARMS)
    return [
        TaskPair(task_id=group.task_id, no_harness=group.arms["no-harness"], yes_harness=group.arms["yes-harness"])
        for group in groups
    ]


def validate_pairs(pairs: list[TaskPair]) -> None:
    validate_task_groups(
        [
            TaskGroup(pair.task_id, {"no-harness": pair.no_harness, "yes-harness": pair.yes_harness})
            for pair in pairs
        ]
    )


def validate_task_groups(groups: list[TaskGroup]) -> None:
    comparable_keys = (
        "id",
        "description",
        "prompt",
        "timeout_seconds",
        "max_attempts",
        "max_cost_usd",
        "expected_files",
        "forbidden_files",
    )
    for group in groups:
        arm_data = [(arm, path, read_json(path)) for arm, path in group.arms.items()]
        reference_arm, _, reference = arm_data[0]
        for arm, path, data in arm_data:
            for key in comparable_keys:
                if data.get(key) != reference.get(key):
                    raise BenchmarkPlanError(
                        f"{group.task_id} differs on {key}; prompts and scoring boundaries "
                        f"must match across arms ({reference_arm} vs {arm})"
                    )
            if not has_hidden_oracle_command(data, group.task_id):
                raise BenchmarkPlanError(f"{path} does not run the hidden oracle")
            validate_docs_boundary_prompt(data, path)


def has_hidden_oracle_command(data: dict[str, Any], task_id: str) -> bool:
    commands = data.get("verification", {}).get("commands", [])
    encoded = json.dumps(commands, sort_keys=True)
    return "run_flask_hidden_checks.sh" in encoded and task_id in encoded


def validate_docs_boundary_prompt(data: dict[str, Any], path: Path) -> None:
    expected_files = data.get("expected_files", [])
    if "docs/**" not in expected_files or "README.md" in expected_files:
        return

    prompt = require_string(data, "prompt", path)
    required_phrases = (
        "documented docs location",
        "Do not update the root README",
    )
    if not all(phrase in prompt for phrase in required_phrases):
        raise BenchmarkPlanError(
            f"{path} allows docs/** but not README.md; prompt must explicitly direct "
            "companion docs to the documented docs location and exclude root README"
        )


def validate_run_shape(args: argparse.Namespace, groups: list[TaskGroup] | list[TaskPair]) -> None:
    if not groups:
        raise BenchmarkPlanError("no task groups selected")
    if args.mode == "large" and len(groups) < args.large_min_task_pairs and not args.allow_small_large:
        raise BenchmarkPlanError(
            f"large mode selected {len(groups)} task groups; add more hidden tasks or pass "
            "--allow-small-large for a repeat-heavy run over the current set"
        )


def build_schedule(pairs: list[TaskPair], repeats: int, pair_order: str) -> list[ScheduledRun]:
    schedule: list[ScheduledRun] = []
    for round_number in range(1, repeats + 1):
        for pair in pairs:
            for group, task_path in group_order(pair, round_number, pair_order):
                schedule.append(
                    ScheduledRun(
                        round_number=round_number,
                        task_id=pair.task_id,
                        group=group,
                        task_path=task_path,
                    )
                )
    return schedule


def build_group_schedule(groups: list[TaskGroup], repeats: int, arm_order: str) -> list[ScheduledRun]:
    schedule: list[ScheduledRun] = []
    for round_number in range(1, repeats + 1):
        for group in groups:
            for label, task_path in ordered_group_arms(group, round_number, arm_order):
                schedule.append(
                    ScheduledRun(
                        round_number=round_number,
                        task_id=group.task_id,
                        group=label,
                        task_path=task_path,
                    )
                )
    return schedule


def group_order(pair: TaskPair, round_number: int, pair_order: str) -> list[tuple[str, Path]]:
    ab = [("A:no-harness", pair.no_harness), ("B:yes-harness", pair.yes_harness)]
    if pair_order == "ab":
        return ab
    if pair_order == "ba":
        return list(reversed(ab))
    if round_number % 2 == 0:
        return list(reversed(ab))
    return ab


def ordered_group_arms(group: TaskGroup, round_number: int, arm_order: str) -> list[tuple[str, Path]]:
    items = list(group.arms.items())
    if arm_order == "reverse":
        items = list(reversed(items))
    elif arm_order == "rotate" and items:
        offset = (round_number - 1) % len(items)
        items = items[offset:] + items[:offset]
    return [(f"{chr(ord('A') + index)}:{arm}", path) for index, (arm, path) in enumerate(items)]


def arm_order_from_pair_order(pair_order: str) -> str:
    if pair_order == "ab":
        return "listed"
    if pair_order == "ba":
        return "reverse"
    return "rotate"


def print_plan(
    args: argparse.Namespace,
    groups: list[TaskGroup],
    schedule: list[ScheduledRun],
    suite: SuiteSpec | None = None,
) -> None:
    print("Hidden Flask Harness Benchmark Plan")
    print(f"Mode: {args.mode}")
    print(f"Execute: {args.execute}")
    if suite is not None:
        print(f"Suite: {suite.suite_id}")
        if suite.split:
            print(f"Split: {suite.split}")
        if suite.prompt_variant:
            print(f"Prompt variant: {suite.prompt_variant}")
    print(f"Task groups: {len(groups)}")
    print(f"Arms: {', '.join(groups[0].arms) if groups else '-'}")
    print(f"Repeats: {args.repeats}")
    print(f"Planned runs: {len(schedule)}")
    print(f"Jobs: {args.jobs}")
    print(f"Arm order: {args.arm_order or arm_order_from_pair_order(args.pair_order)}")
    print(f"Model: {args.model}")
    print(f"Codex exec args: {codex_exec_args(args)}")
    print(f"Workspace: {args.workspace}")
    print(f"Results: {args.results}")
    print("Tasks:")
    for group in groups:
        print(f"- {group.task_id}")

    commands = [build_runner_command(args, item) for item in schedule]
    if args.show_all_commands or len(commands) <= 40:
        print("\nRunner commands:")
        for command in commands:
            print(shlex.join(command))
    else:
        print("\nRunner commands: showing first 12 of " f"{len(commands)}")
        for command in commands[:12]:
            print(shlex.join(command))
        print("...")


def validate_live_execution(args: argparse.Namespace, groups: list[TaskGroup]) -> None:
    if not args.allow_head_ref:
        head_refs = []
        for group in groups:
            for path in group.arms.values():
                data = read_json(path)
                if data.get("repo", {}).get("ref", "HEAD") == "HEAD":
                    head_refs.append(str(path))
        if head_refs:
            raise BenchmarkPlanError(
                "live execution requires pinned repo.ref values, not HEAD: " + ", ".join(head_refs)
            )

    if not args.allow_dirty_targets:
        dirty = dirty_target_repositories(groups)
        if dirty:
            formatted = ", ".join(f"{path} ({status})" for path, status in dirty)
            raise BenchmarkPlanError(f"dirty target repositories are not allowed: {formatted}")


def dirty_target_repositories(groups: list[TaskGroup]) -> list[tuple[Path, str]]:
    dirty: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for group in groups:
        for task_path in group.arms.values():
            data = read_json(task_path)
            source = require_string(require_dict(data, "repo", task_path), "source", task_path)
            resolved = resolve_repo_source(source, task_path)
            if resolved is None or resolved in seen:
                continue
            seen.add(resolved)
            if not (resolved / ".git").exists():
                continue
            completed = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=resolved,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if completed.returncode != 0:
                dirty.append((resolved, completed.stderr.strip() or "git status failed"))
            elif completed.stdout.strip():
                dirty.append((resolved, completed.stdout.strip().splitlines()[0]))
    return dirty


def execute_schedule(args: argparse.Namespace, schedule: list[ScheduledRun]) -> int:
    args.workspace.mkdir(parents=True, exist_ok=True)
    args.results.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["CODEX_MODEL"] = args.model
    env["CODEX_EXEC_ARGS"] = codex_exec_args(args)
    nonzero_commands = 0

    if args.jobs > 1:
        return execute_schedule_parallel(args, schedule, env)

    for index, item in enumerate(schedule, start=1):
        print_start(index, len(schedule), item)
        result = run_scheduled_command(args, item, index, len(schedule), env)
        print_run_output(result)
        if result.returncode != 0:
            nonzero_commands += 1
            print_nonzero_exit(result.returncode)
    if nonzero_commands:
        print(f"\nCompleted schedule with {nonzero_commands} non-zero runner exits.")
    else:
        print("\nCompleted schedule with all runner commands exiting zero.")
    return 0


def execute_schedule_parallel(
    args: argparse.Namespace,
    schedule: list[ScheduledRun],
    env: dict[str, str],
) -> int:
    nonzero_commands = 0
    next_index = 0
    futures: dict[Future[ScheduledRunResult], int] = {}
    total = len(schedule)

    def submit_next(executor: ThreadPoolExecutor) -> None:
        nonlocal next_index
        if next_index >= total:
            return
        item = schedule[next_index]
        index = next_index + 1
        next_index += 1
        print_start(index, total, item)
        future = executor.submit(run_scheduled_command, args, item, index, total, env)
        futures[future] = index

    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        for _ in range(min(args.jobs, total)):
            submit_next(executor)

        while futures:
            done, _ = wait(futures, return_when=FIRST_COMPLETED)
            for future in sorted(done, key=lambda item: futures[item]):
                futures.pop(future)
                result = future.result()
                print_completion(result)
                print_run_output(result)
                if result.returncode != 0:
                    nonzero_commands += 1
                    print_nonzero_exit(result.returncode)
                submit_next(executor)

    if nonzero_commands:
        print(f"\nCompleted schedule with {nonzero_commands} non-zero runner exits.")
    else:
        print("\nCompleted schedule with all runner commands exiting zero.")
    return 0


def run_scheduled_command(
    args: argparse.Namespace,
    item: ScheduledRun,
    index: int,
    total: int,
    env: dict[str, str],
) -> ScheduledRunResult:
    completed = subprocess.run(
        build_runner_command(args, item),
        cwd=REPO_ROOT,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return ScheduledRunResult(
        index=index,
        total=total,
        item=item,
        returncode=completed.returncode,
        stdout=completed.stdout or "",
        stderr=completed.stderr or "",
    )


def print_start(index: int, total: int, item: ScheduledRun) -> None:
    print(
        f"\n[{index}/{total}] start round={item.round_number} "
        f"task={item.task_id} group={item.group}",
        flush=True,
    )


def print_completion(result: ScheduledRunResult) -> None:
    print(
        f"\n[{result.index}/{result.total}] finish round={result.item.round_number} "
        f"task={result.item.task_id} group={result.item.group} "
        f"exit={result.returncode}",
        flush=True,
    )


def print_run_output(result: ScheduledRunResult) -> None:
    if result.stdout:
        sys.stdout.write(result.stdout)
        if not result.stdout.endswith("\n"):
            sys.stdout.write("\n")
    if result.stderr:
        sys.stderr.write(result.stderr)
        if not result.stderr.endswith("\n"):
            sys.stderr.write("\n")
    sys.stdout.flush()
    sys.stderr.flush()


def print_nonzero_exit(returncode: int) -> None:
    print(
        f"runner command exited {returncode}; continuing because failed "
        "benchmark attempts are expected data"
    )


def build_runner_command(args: argparse.Namespace, item: ScheduledRun) -> list[str]:
    return [
        sys.executable,
        "-m",
        "harness_agent_benchmark_runner",
        "run",
        "--task",
        str(item.task_path),
        "--agent-command",
        args.agent_command,
        "--workspace",
        str(args.workspace),
        "--results",
        str(args.results),
        "--max-agent-timeout",
        str(args.max_agent_timeout),
        "--max-cost-usd",
        str(args.max_cost_usd),
    ]


def codex_exec_args(args: argparse.Namespace) -> str:
    parts = [f"-c model_reasoning_effort={args.reasoning_effort}"]
    if args.service_tier:
        parts.append(f"-c service_tier={args.service_tier}")
    return " ".join(parts)


def resolve_repo_source(source: str, task_path: Path) -> Path | None:
    if "://" in source or source.startswith("git@"):
        return None
    source_path = Path(source).expanduser()
    candidates = [source_path] if source_path.is_absolute() else [
        (REPO_ROOT / source_path).resolve(),
        (task_path.parent / source_path).resolve(),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as stream:
            data = json.load(stream)
    except OSError as exc:
        raise BenchmarkPlanError(f"could not read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise BenchmarkPlanError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise BenchmarkPlanError(f"{path} must contain a JSON object")
    return data


def require_dict(data: dict[str, Any], key: str, path: Path) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise BenchmarkPlanError(f"{path}: {key} must be an object")
    return value


def require_string(data: dict[str, Any], key: str, path: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str):
        raise BenchmarkPlanError(f"{path}: {key} must be a string")
    return value


def optional_string(data: dict[str, Any], key: str, path: Path) -> str | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise BenchmarkPlanError(f"{path}: {key} must be a string when provided")
    return value


def string_list(data: dict[str, Any], key: str, path: Path) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise BenchmarkPlanError(f"{path}: {key} must be a list of strings")
    return value


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed


def non_negative_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be greater than or equal to 0")
    return parsed


class BenchmarkPlanError(Exception):
    pass


if __name__ == "__main__":
    raise SystemExit(main())
