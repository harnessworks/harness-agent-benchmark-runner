from __future__ import annotations

import fnmatch
import json
import shutil
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import ProcessResult, RunnerConfig, TaskSpec
from .processes import run_process


def run_task(task: TaskSpec, config: RunnerConfig) -> dict[str, Any]:
    run_id = make_run_id(task.task_id)
    started_at = now_iso()
    run_dir = config.workspace_root.expanduser().resolve() / run_id
    repo_dir = run_dir / "repo"
    logs_dir = run_dir / "logs"
    prompt_path = run_dir / "prompt.txt"

    run_dir.mkdir(parents=True, exist_ok=False)
    logs_dir.mkdir(parents=True, exist_ok=True)

    try:
        repo_source = config.repo_source_override or task.repo.source
        repo_ref = config.repo_ref_override or task.repo.ref
        resolved_source = resolve_repo_source(repo_source, task.source_path)
        clone_repository(resolved_source, repo_dir)
        checkout_ref(repo_dir, repo_ref)
        repository_ref = git_output(repo_dir, ["git", "rev-parse", "HEAD"])

        prompt_path.write_text(task.prompt, encoding="utf-8")
        agent_env = {
            "BENCHMARK_REPO": str(repo_dir),
            "BENCHMARK_PROMPT": task.prompt,
            "BENCHMARK_PROMPT_FILE": str(prompt_path),
            "BENCHMARK_TASK_ID": task.task_id,
            "BENCHMARK_RUN_ID": run_id,
            **config.extra_env,
        }

        agent_result = run_process(
            config.agent_command,
            cwd=repo_dir,
            label="agent",
            timeout_seconds=task.timeout_seconds,
            env=agent_env,
            log_path=logs_dir / "agent.log",
            tail_chars=config.output_tail_chars,
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
        wrong_files = classify_wrong_files(changed_files, task.expected_files)
        forbidden_files = matching_files(changed_files, task.forbidden_files)
        verification_passed = all(result.exit_code == 0 for result in verification_results)
        success = (
            agent_result.exit_code == 0
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
            "task": {
                "id": task.task_id,
                "description": task.description,
                "prompt_ref": task.prompt_ref,
                "expected_files": list(task.expected_files),
                "forbidden_files": list(task.forbidden_files),
            },
            "repo": {
                "source": repo_source,
                "resolved_source": resolved_source,
                "ref": repo_ref,
                "repository_ref": repository_ref,
                "isolated_path": str(repo_dir),
            },
            "agent": agent_result.to_dict(),
            "git": {
                "changed_files": changed_files,
                "diff_stat": git_output(repo_dir, ["git", "diff", "--stat"], allow_failure=True),
                "status": git_output(repo_dir, ["git", "status", "--short"], allow_failure=True),
                "diff_check": diff_check.to_dict(),
            },
            "verification": [result.to_dict() for result in verification_results],
            "scoring": {
                "success": success,
                "agent_exit_code": agent_result.exit_code,
                "verification_passed": verification_passed,
                "first_pass_verification": verification_passed,
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
            "task": {"id": task.task_id, "description": task.description},
            "repo": {"source": config.repo_source_override or task.repo.source},
            "scoring": {"success": False, "runner_error": type(exc).__name__},
            "error": str(exc),
        }
        write_result(result, config.results_dir.expanduser().resolve(), run_dir)
        raise
    finally:
        if not config.keep_runs:
            shutil.rmtree(run_dir, ignore_errors=True)


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
            run_process(
                command.command,
                cwd=repo_dir,
                label=command.label,
                timeout_seconds=timeout,
                log_path=logs_dir / f"verify-{index}.log",
                tail_chars=config.output_tail_chars,
            )
        )
    return results


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
    with jsonl_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(result, sort_keys=True) + "\n")


def make_run_id(task_id: str) -> str:
    safe_task = "".join(char if char.isalnum() or char in "-_" else "-" for char in task_id).strip("-")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}-{safe_task}-{uuid.uuid4().hex[:8]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
