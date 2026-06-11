from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Mapping

from .models import ProcessResult


def run_process(
    command: str | list[str],
    *,
    cwd: Path,
    label: str,
    timeout_seconds: int,
    env: Mapping[str, str] | None = None,
    log_path: Path,
    tail_chars: int = 4000,
) -> ProcessResult:
    started = time.monotonic()
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            env=merged_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            shell=isinstance(command, str),
            check=False,
        )
        duration = time.monotonic() - started
        timed_out = False
        exit_code = completed.returncode
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started
        timed_out = True
        exit_code = 124
        stdout = decode_output(exc.stdout)
        stderr = decode_output(exc.stderr)
        stderr += f"\nTimed out after {timeout_seconds} seconds.\n"

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        format_log(command, cwd=cwd, exit_code=exit_code, duration=duration, stdout=stdout, stderr=stderr),
        encoding="utf-8",
    )

    return ProcessResult(
        label=label,
        command=command,
        cwd=str(cwd),
        exit_code=exit_code,
        duration_seconds=duration,
        log_path=str(log_path),
        timed_out=timed_out,
        stdout_tail=stdout[-tail_chars:],
        stderr_tail=stderr[-tail_chars:],
    )


def decode_output(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.decode("utf-8", errors="replace")


def format_log(
    command: str | list[str],
    *,
    cwd: Path,
    exit_code: int,
    duration: float,
    stdout: str,
    stderr: str,
) -> str:
    return "\n".join(
        [
            f"command: {command}",
            f"cwd: {cwd}",
            f"exit_code: {exit_code}",
            f"duration_seconds: {duration:.3f}",
            "",
            "## stdout",
            stdout,
            "",
            "## stderr",
            stderr,
            "",
        ]
    )
