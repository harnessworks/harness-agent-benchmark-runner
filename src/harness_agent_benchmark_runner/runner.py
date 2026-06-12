from __future__ import annotations

import fnmatch
import json
import os
import shutil
import subprocess
import tempfile
import uuid
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import ProcessResult, RunnerConfig, TaskSpec
from .processes import run_process

try:
    import fcntl
except ImportError:  # pragma: no cover - fcntl is unavailable on Windows.
    fcntl = None


def run_task(
    task: TaskSpec,
    config: RunnerConfig,
    *,
    attempt_number: int = 1,
    attempt_limit: int | None = None,
    raise_on_runner_error: bool = True,
) -> dict[str, Any]:
    attempt_limit = attempt_limit or resolve_attempt_limit(task, config)
    run_id = make_run_id(task.task_id)
    started_at = now_iso()
    run_dir = config.workspace_root.expanduser().resolve() / run_id
    repo_dir = run_dir / "repo"
    logs_dir = run_dir / "logs"
    prompt_path = run_dir / "prompt.txt"
    agent_timeout_seconds = effective_agent_timeout_seconds(task, config)
    agent_process_timeout_seconds, agent_timeout_reason = effective_agent_process_timeout(
        agent_timeout_seconds,
        config,
    )
    max_cost_usd = effective_max_cost_usd(task, config)

    run_dir.mkdir(parents=True, exist_ok=False)
    logs_dir.mkdir(parents=True, exist_ok=True)

    try:
        repo_source = config.repo_source_override or task.repo.source
        repo_ref = config.repo_ref_override or task.repo.ref
        resolved_source = resolve_repo_source(repo_source, task.source_path)
        clone_repository(resolved_source, repo_dir)
        checkout_ref(repo_dir, repo_ref)
        repository_ref = git_output(repo_dir, ["git", "rev-parse", "HEAD"])
        preflight = run_preflight_audit(task, repo_dir)
        if not preflight["passed"]:
            finished_at = now_iso()
            result = {
                "schema_version": 1,
                "run_id": run_id,
                "started_at": started_at,
                "finished_at": finished_at,
                "attempt": {
                    "number": attempt_number,
                    "limit": attempt_limit,
                },
                "limits": {
                    "agent_timeout_seconds": agent_timeout_seconds,
                    "agent_process_timeout_seconds": agent_process_timeout_seconds,
                    "agent_timeout_override_seconds": config.agent_timeout_override_seconds,
                    "agent_stall_timeout_seconds": config.agent_stall_timeout_seconds,
                    "agent_idle_timeout_seconds": config.agent_idle_timeout_seconds,
                    "max_agent_timeout_seconds": config.max_agent_timeout_seconds,
                    "max_cost_usd": max_cost_usd,
                },
                "task": task_result_metadata(task),
                "repo": {
                    "source": repo_source,
                    "resolved_source": resolved_source,
                    "ref": repo_ref,
                    "repository_ref": repository_ref,
                    "isolated_path": str(repo_dir),
                },
                "preflight": preflight,
                "scoring": preflight_failure_scoring(preflight),
            }
            write_result(result, config.results_dir.expanduser().resolve(), run_dir)
            return result

        agent_exclusions = hide_agent_excluded_paths(task, repo_dir)
        agent_git = isolate_agent_git_if_needed(task, repo_dir)
        agent_setup_results = run_agent_setup_commands(task, config, repo_dir, logs_dir)
        prompt_path.write_text(task.prompt, encoding="utf-8")
        agent_env = {
            "BENCHMARK_REPO": str(repo_dir),
            "BENCHMARK_PROMPT": task.prompt,
            "BENCHMARK_PROMPT_FILE": str(prompt_path),
            "BENCHMARK_TASK_ID": task.task_id,
            "BENCHMARK_RUN_ID": run_id,
            "BENCHMARK_ATTEMPT_NUMBER": str(attempt_number),
            "BENCHMARK_ATTEMPT_LIMIT": str(attempt_limit),
            "BENCHMARK_TIMEOUT_SECONDS": str(agent_timeout_seconds),
            **config.extra_env,
        }
        venv_bin = repo_dir / ".venv" / "bin"
        if venv_bin.is_dir():
            agent_env["PATH"] = str(venv_bin) + os.pathsep + os.environ.get("PATH", "")
        if max_cost_usd is not None:
            agent_env["BENCHMARK_MAX_COST_USD"] = str(max_cost_usd)

        try:
            agent_result = run_process(
                config.agent_command,
                cwd=repo_dir,
                label="agent",
                timeout_seconds=agent_process_timeout_seconds,
                timeout_reason=agent_timeout_reason,
                idle_timeout_seconds=config.agent_idle_timeout_seconds,
                env=agent_env,
                log_path=logs_dir / "agent.log",
                tail_chars=config.output_tail_chars,
            )
        finally:
            restore_agent_git(agent_git, repo_dir)
            agent_exclusion_conflicts = restore_agent_excluded_paths(
                agent_exclusions,
                repo_dir,
                run_dir / "_agent_excluded_conflicts",
            )

        diff_check = run_process(
            ["git", "diff", "--check"],
            cwd=repo_dir,
            label="git diff --check",
            timeout_seconds=config.default_command_timeout_seconds,
            log_path=logs_dir / "git-diff-check.log",
            tail_chars=config.output_tail_chars,
        )

        verification_results = run_verification_commands(task, config, repo_dir, logs_dir)
        changed_files = collect_changed_files(repo_dir)
        changed_files_for_scoring = sorted(
            {*changed_files, *(conflict["path"] for conflict in agent_exclusion_conflicts)}
        )
        wrong_files = classify_wrong_files(changed_files_for_scoring, task.expected_files)
        forbidden_files = matching_files(changed_files_for_scoring, task.forbidden_files)
        verification_passed = all(result.exit_code == 0 for result in verification_results)
        dimension_scoring = calculate_dimension_scoring(
            preflight_passed=preflight["passed"],
            agent_result=agent_result,
            diff_check=diff_check,
            verification_results=verification_results,
            verification_passed=verification_passed,
            wrong_files=wrong_files,
            forbidden_files=forbidden_files,
        )
        success = (
            preflight["passed"]
            and agent_result.exit_code == 0
            and diff_check.exit_code == 0
            and verification_passed
            and not wrong_files
            and not forbidden_files
        )

        finished_at = now_iso()
        result = {
            "schema_version": 1,
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "attempt": {
                "number": attempt_number,
                "limit": attempt_limit,
            },
            "limits": {
                "agent_timeout_seconds": agent_timeout_seconds,
                "agent_process_timeout_seconds": agent_process_timeout_seconds,
                "agent_timeout_override_seconds": config.agent_timeout_override_seconds,
                "agent_stall_timeout_seconds": config.agent_stall_timeout_seconds,
                "agent_idle_timeout_seconds": config.agent_idle_timeout_seconds,
                "max_agent_timeout_seconds": config.max_agent_timeout_seconds,
                "max_cost_usd": max_cost_usd,
            },
            "task": task_result_metadata(task),
            "repo": {
                "source": repo_source,
                "resolved_source": resolved_source,
                "ref": repo_ref,
                "repository_ref": repository_ref,
                "isolated_path": str(repo_dir),
            },
            "preflight": preflight,
            "agent_setup": [result.to_dict() for result in agent_setup_results],
            "agent": agent_result.to_dict(),
            "git": {
                "changed_files": changed_files,
                "agent_excluded_path_conflicts": agent_exclusion_conflicts,
                "diff_stat": git_output(repo_dir, ["git", "diff", "--stat"], allow_failure=True),
                "status": git_output(repo_dir, ["git", "status", "--short"], allow_failure=True),
                "diff_check": diff_check.to_dict(),
            },
            "verification": [result.to_dict() for result in verification_results],
            "scoring": {
                "success": success,
                "strict_success": dimension_scoring["strict_success"],
                "functional_success": dimension_scoring["functional_success"],
                "schema_contract_success": dimension_scoring["schema_contract_success"],
                "workflow_success": dimension_scoring["workflow_success"],
                "boundary_success": dimension_scoring["boundary_success"],
                "execution_success": dimension_scoring["execution_success"],
                "preflight_passed": preflight["passed"],
                "dimensions": dimension_scoring,
                "agent_exit_code": agent_result.exit_code,
                "agent_timed_out": agent_result.timed_out,
                "agent_stalled": agent_stalled(agent_result),
                "verification_passed": verification_passed,
                "first_pass_verification": attempt_number == 1 and verification_passed,
                "wrong_file_edits": len(wrong_files),
                "wrong_files": wrong_files,
                "forbidden_file_edits": len(forbidden_files),
                "forbidden_files": forbidden_files,
            },
        }

        write_result(result, config.results_dir.expanduser().resolve(), run_dir)
        return result
    except Exception as exc:
        result = {
            "schema_version": 1,
            "run_id": run_id,
            "started_at": started_at,
            "finished_at": now_iso(),
            "attempt": {
                "number": attempt_number,
                "limit": attempt_limit,
            },
            "limits": {
                "agent_timeout_seconds": agent_timeout_seconds,
                "agent_process_timeout_seconds": agent_process_timeout_seconds,
                "agent_timeout_override_seconds": config.agent_timeout_override_seconds,
                "agent_stall_timeout_seconds": config.agent_stall_timeout_seconds,
                "agent_idle_timeout_seconds": config.agent_idle_timeout_seconds,
                "max_agent_timeout_seconds": config.max_agent_timeout_seconds,
                "max_cost_usd": max_cost_usd,
            },
            "task": {"id": task.task_id, "description": task.description},
            "repo": {"source": config.repo_source_override or task.repo.source},
            "scoring": runner_error_scoring(type(exc).__name__),
            "error": str(exc),
        }
        write_result(result, config.results_dir.expanduser().resolve(), run_dir)
        if raise_on_runner_error:
            raise
        return result
    finally:
        if not config.keep_runs:
            shutil.rmtree(run_dir, ignore_errors=True)


def run_task_with_retries(task: TaskSpec, config: RunnerConfig) -> list[dict[str, Any]]:
    attempt_limit = resolve_attempt_limit(task, config)
    if attempt_limit <= 0:
        raise ValueError("attempt limit must be greater than 0")
    results: list[dict[str, Any]] = []
    for attempt_number in range(1, attempt_limit + 1):
        result = run_task(
            task,
            config,
            attempt_number=attempt_number,
            attempt_limit=attempt_limit,
            raise_on_runner_error=False,
        )
        results.append(result)
        if result.get("scoring", {}).get("success") is True:
            break
    return results


def task_result_metadata(task: TaskSpec) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "id": task.task_id,
        "description": task.description,
        "prompt_ref": task.prompt_ref,
        "timeout_seconds": task.timeout_seconds,
        "max_attempts": task.max_attempts,
        "max_cost_usd": task.max_cost_usd,
        "expected_files": list(task.expected_files),
        "forbidden_files": list(task.forbidden_files),
    }
    if task.agent_excluded_paths:
        metadata["agent_excluded_paths"] = list(task.agent_excluded_paths)
    if task.agent_setup_commands:
        metadata["agent_setup"] = {
            "commands": [command.label for command in task.agent_setup_commands],
        }
    if task.benchmark:
        metadata["benchmark"] = task.benchmark
    return metadata


def run_agent_setup_commands(
    task: TaskSpec,
    config: RunnerConfig,
    repo_dir: Path,
    logs_dir: Path,
) -> list[ProcessResult]:
    results: list[ProcessResult] = []
    for index, command in enumerate(task.agent_setup_commands, start=1):
        timeout = command.timeout_seconds or config.default_command_timeout_seconds
        results.append(
            replace(
                run_process(
                    materialize_verification_command(command.command, task.source_path),
                    cwd=repo_dir,
                    label=command.label,
                    timeout_seconds=timeout,
                    log_path=logs_dir / f"agent-setup-{index}.log",
                    tail_chars=config.output_tail_chars,
                ),
                dimensions=command.dimensions,
            )
        )
    return results


def hide_agent_excluded_paths(
    task: TaskSpec,
    repo_dir: Path,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for raw_path in task.agent_excluded_paths:
        relative_path = normalize_agent_excluded_path(raw_path)
        source = repo_dir / relative_path
        if not source.exists():
            continue
        records.append(
            {
                "path": relative_path.as_posix(),
                "entries": snapshot_path(source, repo_dir),
            }
        )
        remove_path(source)
    return records


def isolate_agent_git_if_needed(
    task: TaskSpec,
    repo_dir: Path,
) -> dict[str, str]:
    if not task.agent_excluded_paths:
        return {}
    original_git = repo_dir / ".git"
    if not original_git.exists():
        return {}

    hidden_root = Path(tempfile.mkdtemp(prefix="harness-agent-git-"))
    hidden_root.mkdir(parents=True, exist_ok=True)
    original_git_path = hidden_root / "original.git"
    agent_git_path = hidden_root / "agent.git"
    shutil.move(str(original_git), str(original_git_path))
    run_git(repo_dir, ["git", "init", "-b", "main"])
    run_git(repo_dir, ["git", "config", "user.email", "benchmark@example.com"])
    run_git(repo_dir, ["git", "config", "user.name", "Benchmark Runner"])
    run_git(repo_dir, ["git", "add", "-A"])
    run_git(repo_dir, ["git", "commit", "--quiet", "-m", "Agent visible baseline"])
    return {
        "hidden_root": str(hidden_root),
        "original_git_path": str(original_git_path),
        "agent_git_path": str(agent_git_path),
    }


def restore_agent_git(state: dict[str, str], repo_dir: Path) -> None:
    if not state:
        return
    agent_git = repo_dir / ".git"
    if agent_git.exists():
        shutil.move(str(agent_git), state["agent_git_path"])
    original_git = Path(state["original_git_path"])
    if original_git.exists():
        shutil.move(str(original_git), str(agent_git))
    hidden_root = Path(state["hidden_root"])
    if hidden_root.exists():
        shutil.rmtree(hidden_root, ignore_errors=True)


def restore_agent_excluded_paths(
    records: list[dict[str, Any]],
    repo_dir: Path,
    conflict_root: Path,
) -> list[dict[str, str]]:
    conflicts: list[dict[str, str]] = []
    for record in reversed(records):
        relative_path = Path(record["path"])
        destination = repo_dir / relative_path
        if destination.exists():
            conflict_path = conflict_root / relative_path
            conflict_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(destination), str(conflict_path))
            conflicts.append(
                {
                    "path": relative_path.as_posix(),
                    "preserved_path": str(conflict_path),
                }
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        restore_snapshot(record["entries"], repo_dir)
    return sorted(conflicts, key=lambda item: item["path"])


def snapshot_path(path: Path, repo_dir: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    paths = [path]
    if path.is_dir() and not path.is_symlink():
        paths.extend(sorted(path.rglob("*")))

    for item in paths:
        relative_path = item.relative_to(repo_dir).as_posix()
        if item.is_symlink():
            entries.append(
                {
                    "type": "symlink",
                    "path": relative_path,
                    "target": os.readlink(item),
                }
            )
        elif item.is_dir():
            entries.append(
                {
                    "type": "dir",
                    "path": relative_path,
                    "mode": item.stat().st_mode & 0o777,
                }
            )
        elif item.is_file():
            entries.append(
                {
                    "type": "file",
                    "path": relative_path,
                    "mode": item.stat().st_mode & 0o777,
                    "content": item.read_bytes(),
                }
            )
    return entries


def restore_snapshot(entries: list[dict[str, Any]], repo_dir: Path) -> None:
    for entry in entries:
        path = repo_dir / entry["path"]
        if entry["type"] == "dir":
            path.mkdir(parents=True, exist_ok=True)
            path.chmod(entry["mode"])
        elif entry["type"] == "file":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(entry["content"])
            path.chmod(entry["mode"])
        elif entry["type"] == "symlink":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(entry["target"])


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def normalize_agent_excluded_path(value: str) -> Path:
    path = Path(value)
    if (
        not value.strip()
        or value.strip() == "."
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ValueError(f"agent_excluded_paths entries must be relative paths under the repo: {value!r}")
    return path


def run_git(repo_dir: Path, command: list[str]) -> None:
    subprocess.run(
        command,
        cwd=str(repo_dir),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def run_preflight_audit(task: TaskSpec, repo_dir: Path) -> dict[str, Any]:
    audit = task.leakage_audit
    files = collect_repository_files(repo_dir)
    findings: list[dict[str, Any]] = []

    status = git_output(repo_dir, ["git", "status", "--porcelain=v1"], allow_failure=True)
    if status.strip():
        findings.append(
            {
                "type": "dirty_isolated_clone",
                "path": ".",
                "detail": status.strip().splitlines()[0],
            }
        )

    for path in files:
        for pattern in audit.forbidden_paths:
            if path_matches(path, pattern):
                findings.append(
                    {
                        "type": "forbidden_path",
                        "path": path,
                        "pattern": pattern,
                    }
                )

    if audit.forbidden_text:
        for path in files:
            full_path = repo_dir / path
            if not full_path.is_file():
                continue
            text = read_text_for_audit(full_path)
            if text is None:
                continue
            for needle in audit.forbidden_text:
                if not needle:
                    continue
                index = text.find(needle)
                if index >= 0:
                    findings.append(
                        {
                            "type": "forbidden_text",
                            "path": path,
                            "text": needle,
                            "line": text.count("\n", 0, index) + 1,
                        }
                    )

    return {
        "passed": not findings,
        "findings": findings,
        "checked": {
            "repository_files": len(files),
            "isolated_clone_clean": not status.strip(),
            "forbidden_paths": list(audit.forbidden_paths),
            "forbidden_text": list(audit.forbidden_text),
        },
    }


def collect_repository_files(repo_dir: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard", "-z"],
        cwd=str(repo_dir),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode == 0:
        return sorted(path for path in completed.stdout.split("\0") if path)

    files = []
    for path in repo_dir.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        files.append(path.relative_to(repo_dir).as_posix())
    return sorted(files)


def read_text_for_audit(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\0" in raw:
        return None
    return raw.decode("utf-8", errors="ignore")


def calculate_dimension_scoring(
    *,
    preflight_passed: bool,
    agent_result: ProcessResult,
    diff_check: ProcessResult,
    verification_results: list[ProcessResult],
    verification_passed: bool,
    wrong_files: list[str],
    forbidden_files: list[str],
) -> dict[str, bool]:
    execution_success = agent_result.exit_code == 0 and not agent_result.timed_out
    boundary_success = not wrong_files and not forbidden_files
    diff_success = diff_check.exit_code == 0
    functional_success = preflight_passed and verification_dimension_success(
        verification_results,
        "functional",
        verification_passed,
    )
    schema_contract_success = preflight_passed and verification_dimension_success(
        verification_results,
        "schema",
        verification_passed,
    )
    workflow_success = (
        preflight_passed
        and execution_success
        and diff_success
        and boundary_success
        and verification_dimension_success(verification_results, "workflow", verification_passed)
    )
    strict_success = (
        preflight_passed
        and execution_success
        and diff_success
        and verification_passed
        and boundary_success
    )
    return {
        "functional_success": functional_success,
        "schema_contract_success": schema_contract_success,
        "workflow_success": workflow_success,
        "boundary_success": boundary_success,
        "execution_success": execution_success,
        "strict_success": strict_success,
    }


def verification_dimension_success(
    verification_results: list[ProcessResult],
    dimension: str,
    legacy_fallback: bool,
) -> bool:
    selected = [result for result in verification_results if dimension in result.dimensions]
    if selected:
        return all(result.exit_code == 0 for result in selected)
    if any(result.dimensions for result in verification_results):
        return True
    return legacy_fallback


def preflight_failure_scoring(preflight: dict[str, Any]) -> dict[str, Any]:
    dimensions = {
        "functional_success": False,
        "schema_contract_success": False,
        "workflow_success": False,
        "boundary_success": False,
        "execution_success": False,
        "strict_success": False,
    }
    return {
        "success": False,
        "strict_success": False,
        "functional_success": False,
        "schema_contract_success": False,
        "workflow_success": False,
        "boundary_success": False,
        "execution_success": False,
        "preflight_passed": False,
        "preflight_findings": len(preflight.get("findings", [])),
        "dimensions": dimensions,
        "agent_exit_code": None,
        "agent_timed_out": False,
        "agent_stalled": False,
        "verification_passed": False,
        "first_pass_verification": False,
        "wrong_file_edits": 0,
        "wrong_files": [],
        "forbidden_file_edits": 0,
        "forbidden_files": [],
    }


def runner_error_scoring(error_type: str) -> dict[str, Any]:
    scoring = preflight_failure_scoring({"findings": []})
    scoring["runner_error"] = error_type
    return scoring


def agent_stalled(agent_result: ProcessResult) -> bool:
    return agent_result.timed_out and agent_result.termination_reason in {
        "stall_watchdog",
        "idle_watchdog",
    }


def run_verification_commands(
    task: TaskSpec,
    config: RunnerConfig,
    repo_dir: Path,
    logs_dir: Path,
) -> list[ProcessResult]:
    results: list[ProcessResult] = []
    for index, command in enumerate(task.verification_commands, start=1):
        timeout = command.timeout_seconds or config.default_command_timeout_seconds
        results.append(
            replace(
                run_process(
                    materialize_verification_command(command.command, task.source_path),
                    cwd=repo_dir,
                    label=command.label,
                    timeout_seconds=timeout,
                    log_path=logs_dir / f"verify-{index}.log",
                    tail_chars=config.output_tail_chars,
                ),
                dimensions=command.dimensions,
            )
        )
    return results


def materialize_verification_command(command: str | list[str], task_path: Path | None) -> str | list[str]:
    if task_path is None:
        return command

    replacements = {
        "{task_dir}": str(task_path.parent),
        "{task_file}": str(task_path),
    }

    def replace(value: str) -> str:
        for placeholder, replacement in replacements.items():
            value = value.replace(placeholder, replacement)
        return value

    if isinstance(command, str):
        return replace(command)
    return [replace(part) for part in command]


def resolve_attempt_limit(task: TaskSpec, config: RunnerConfig) -> int:
    if config.max_attempts_override is not None:
        return config.max_attempts_override
    return task.max_attempts


def effective_agent_timeout_seconds(task: TaskSpec, config: RunnerConfig) -> int:
    task_timeout = config.agent_timeout_override_seconds or task.timeout_seconds
    if config.max_agent_timeout_seconds is None:
        return task_timeout
    return min(task_timeout, config.max_agent_timeout_seconds)


def effective_agent_process_timeout(
    agent_timeout_seconds: int,
    config: RunnerConfig,
) -> tuple[int, str]:
    stall_timeout = config.agent_stall_timeout_seconds
    if stall_timeout is not None and stall_timeout < agent_timeout_seconds:
        return stall_timeout, "stall_watchdog"
    return agent_timeout_seconds, "timeout"


def effective_max_cost_usd(task: TaskSpec, config: RunnerConfig) -> float | None:
    if config.max_cost_usd_override is not None:
        return config.max_cost_usd_override
    return task.max_cost_usd


def resolve_repo_source(source: str, task_path: Path | None) -> str:
    if is_probable_url(source):
        return source

    source_path = Path(source).expanduser()
    candidates = []
    if source_path.is_absolute():
        candidates.append(source_path)
    else:
        candidates.append((Path.cwd() / source_path).resolve())
        if task_path is not None:
            candidates.append((task_path.parent / source_path).resolve())

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    return str(candidates[0])


def is_probable_url(value: str) -> bool:
    return "://" in value or value.startswith("git@")


def clone_repository(source: str, destination: Path) -> None:
    subprocess.run(
        ["git", "clone", "--quiet", source, str(destination)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def checkout_ref(repo_dir: Path, ref: str) -> None:
    if ref == "HEAD":
        return
    subprocess.run(
        ["git", "checkout", "--quiet", ref],
        cwd=str(repo_dir),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def collect_changed_files(repo_dir: Path) -> list[str]:
    output = git_output(repo_dir, ["git", "status", "--porcelain=v1"], allow_failure=True)
    files: set[str] = set()
    for line in output.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            old_path, new_path = path.split(" -> ", 1)
            files.add(old_path)
            files.add(new_path)
        else:
            files.add(path)
    return sorted(files)


def classify_wrong_files(changed_files: list[str], expected_patterns: tuple[str, ...]) -> list[str]:
    if not expected_patterns:
        return []
    return [path for path in changed_files if not matches_any(path, expected_patterns)]


def matching_files(changed_files: list[str], patterns: tuple[str, ...]) -> list[str]:
    return [path for path in changed_files if matches_any(path, patterns)]


def matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    return any(path_matches(path, pattern) for pattern in patterns)


def path_matches(path: str, pattern: str) -> bool:
    normalized_path = path.strip("/")
    normalized_pattern = pattern.strip("/")
    if normalized_path == normalized_pattern:
        return True
    if fnmatch.fnmatch(normalized_path, normalized_pattern):
        return True
    if normalized_pattern.endswith("/**"):
        prefix = normalized_pattern[:-3].rstrip("/")
        return normalized_path == prefix or normalized_path.startswith(prefix + "/")
    if "/" not in normalized_pattern and fnmatch.fnmatch(Path(normalized_path).name, normalized_pattern):
        return True
    return False


def git_output(repo_dir: Path, command: list[str], allow_failure: bool = False) -> str:
    completed = subprocess.run(
        command,
        cwd=str(repo_dir),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0 and not allow_failure:
        raise RuntimeError(completed.stderr.strip() or f"command failed: {' '.join(command)}")
    return completed.stdout.rstrip("\n")


def write_result(result: dict[str, Any], results_dir: Path, run_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    result_path = run_dir / "result.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    jsonl_path = results_dir / f"{day}.jsonl"
    line = json.dumps(result, sort_keys=True) + "\n"

    if fcntl is None:
        with jsonl_path.open("a", encoding="utf-8") as stream:
            stream.write(line)
        return

    lock_path = results_dir / f"{day}.jsonl.lock"
    with lock_path.open("w", encoding="utf-8") as lock_stream:
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX)
        try:
            with jsonl_path.open("a", encoding="utf-8") as stream:
                stream.write(line)
        finally:
            fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)


def make_run_id(task_id: str) -> str:
    safe_task = "".join(char if char.isalnum() or char in "-_" else "-" for char in task_id).strip("-")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}-{safe_task}-{uuid.uuid4().hex[:8]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
