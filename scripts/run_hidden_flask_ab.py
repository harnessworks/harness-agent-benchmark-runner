#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TASK_DIR = REPO_ROOT / "benchmarks" / "tasks" / "flask-hidden"
DEFAULT_AGENT = f"{sys.executable} {REPO_ROOT / 'examples' / 'agents' / 'codex_exec_agent.py'}"


@dataclass(frozen=True)
class TaskPair:
    task_id: str
    no_harness: Path
    yes_harness: Path


@dataclass(frozen=True)
class ScheduledRun:
    round_number: int
    task_id: str
    group: str
    task_path: Path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    args.task_dir = args.task_dir.resolve()
    args.repeats = args.repeats or default_repeats(args.mode)
    args.task_limit = default_task_limit(args.mode) if args.task_limit is None else args.task_limit
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if args.results is None:
        args.results = REPO_ROOT / "results" / f"hidden-flask-ab-{args.mode}-{stamp}"
    if args.workspace is None:
        args.workspace = REPO_ROOT / "runs" / f"hidden-flask-ab-{args.mode}-{stamp}"

    try:
        pairs = load_task_pairs(args.task_dir)
        validate_pairs(pairs)
        selected_pairs = pairs[: args.task_limit] if args.task_limit else pairs
        validate_run_shape(args, selected_pairs)
        schedule = build_schedule(selected_pairs, args.repeats, args.pair_order)
        print_plan(args, selected_pairs, schedule)
        if not args.execute:
            print("\nDry run only. Re-run with --execute to start live agent benchmark runs.")
            return 0
        validate_live_execution(args, selected_pairs)
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
    parser.add_argument("--task-dir", type=Path, default=DEFAULT_TASK_DIR)
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
    parser.add_argument("--agent-command", default=DEFAULT_AGENT)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--service-tier", default="priority")
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


def load_task_pairs(task_dir: Path) -> list[TaskPair]:
    if not task_dir.exists():
        raise BenchmarkPlanError(f"task directory does not exist: {task_dir}")

    grouped: dict[str, dict[str, Path]] = {}
    for path in sorted(task_dir.glob("*.json")):
        data = read_json(path)
        task_id = require_string(data, "id", path)
        if path.name.endswith("-no-harness.json"):
            side = "no_harness"
        elif path.name.endswith("-yes-harness.json"):
            side = "yes_harness"
        else:
            continue
        grouped.setdefault(task_id, {})
        if side in grouped[task_id]:
            raise BenchmarkPlanError(f"duplicate {side} task for {task_id}")
        grouped[task_id][side] = path

    pairs = []
    for task_id, sides in sorted(grouped.items()):
        if "no_harness" not in sides or "yes_harness" not in sides:
            raise BenchmarkPlanError(f"incomplete A/B pair for task id: {task_id}")
        pairs.append(TaskPair(task_id, sides["no_harness"], sides["yes_harness"]))
    if not pairs:
        raise BenchmarkPlanError(f"no hidden Flask task pairs found in {task_dir}")
    return pairs


def validate_pairs(pairs: list[TaskPair]) -> None:
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
    for pair in pairs:
        no_data = read_json(pair.no_harness)
        yes_data = read_json(pair.yes_harness)
        for key in comparable_keys:
            if no_data.get(key) != yes_data.get(key):
                raise BenchmarkPlanError(f"{pair.task_id} differs on {key}; A/B prompts must match")
        if not has_hidden_oracle_command(no_data, pair.task_id):
            raise BenchmarkPlanError(f"{pair.no_harness} does not run the hidden oracle")
        if not has_hidden_oracle_command(yes_data, pair.task_id):
            raise BenchmarkPlanError(f"{pair.yes_harness} does not run the hidden oracle")
        validate_docs_boundary_prompt(no_data, pair.no_harness)
        validate_docs_boundary_prompt(yes_data, pair.yes_harness)


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


def validate_run_shape(args: argparse.Namespace, pairs: list[TaskPair]) -> None:
    if not pairs:
        raise BenchmarkPlanError("no task pairs selected")
    if args.mode == "large" and len(pairs) < args.large_min_task_pairs and not args.allow_small_large:
        raise BenchmarkPlanError(
            f"large mode selected {len(pairs)} task pairs; add more hidden tasks or pass "
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


def group_order(pair: TaskPair, round_number: int, pair_order: str) -> list[tuple[str, Path]]:
    ab = [("A:no-harness", pair.no_harness), ("B:yes-harness", pair.yes_harness)]
    if pair_order == "ab":
        return ab
    if pair_order == "ba":
        return list(reversed(ab))
    if round_number % 2 == 0:
        return list(reversed(ab))
    return ab


def print_plan(args: argparse.Namespace, pairs: list[TaskPair], schedule: list[ScheduledRun]) -> None:
    print("Hidden Flask Harness A/B Benchmark Plan")
    print(f"Mode: {args.mode}")
    print(f"Execute: {args.execute}")
    print(f"Task pairs: {len(pairs)}")
    print(f"Repeats: {args.repeats}")
    print(f"Planned runs: {len(schedule)}")
    print(f"Pair order: {args.pair_order} (A=no-harness, B=yes-harness)")
    print(f"Model: {args.model}")
    print(f"Codex exec args: {codex_exec_args(args)}")
    print(f"Workspace: {args.workspace}")
    print(f"Results: {args.results}")
    print("Tasks:")
    for pair in pairs:
        print(f"- {pair.task_id}")

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


def validate_live_execution(args: argparse.Namespace, pairs: list[TaskPair]) -> None:
    if not args.allow_head_ref:
        head_refs = []
        for pair in pairs:
            for path in (pair.no_harness, pair.yes_harness):
                data = read_json(path)
                if data.get("repo", {}).get("ref", "HEAD") == "HEAD":
                    head_refs.append(str(path))
        if head_refs:
            raise BenchmarkPlanError(
                "live execution requires pinned repo.ref values, not HEAD: " + ", ".join(head_refs)
            )

    if not args.allow_dirty_targets:
        dirty = dirty_target_repositories(pairs)
        if dirty:
            formatted = ", ".join(f"{path} ({status})" for path, status in dirty)
            raise BenchmarkPlanError(f"dirty target repositories are not allowed: {formatted}")


def dirty_target_repositories(pairs: list[TaskPair]) -> list[tuple[Path, str]]:
    dirty: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for pair in pairs:
        for task_path in (pair.no_harness, pair.yes_harness):
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

    for index, item in enumerate(schedule, start=1):
        print(
            f"\n[{index}/{len(schedule)}] round={item.round_number} "
            f"task={item.task_id} group={item.group}"
        )
        completed = subprocess.run(build_runner_command(args, item), cwd=REPO_ROOT, env=env, check=False)
        if completed.returncode != 0:
            nonzero_commands += 1
            print(
                f"runner command exited {completed.returncode}; continuing because failed "
                "benchmark attempts are expected data"
            )
    if nonzero_commands:
        print(f"\nCompleted schedule with {nonzero_commands} non-zero runner exits.")
    else:
        print("\nCompleted schedule with all runner commands exiting zero.")
    return 0


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
