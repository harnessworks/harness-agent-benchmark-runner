from __future__ import annotations

import os
import signal
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

    stdout = ""
    stderr = ""
    try:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            env=merged_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=isinstance(command, str),
            start_new_session=True,
        )
        stdout, stderr = process.communicate(timeout=timeout_seconds)
        duration = time.monotonic() - started
        timed_out = False
        exit_code = process.returncode
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started
        timed_out = True
        exit_code = 124
        stdout = decode_output(exc.stdout)
        stderr = decode_output(exc.stderr)
        terminate_process_group(process)
        final_stdout, final_stderr = process.communicate()
        stdout = final_stdout or stdout
        stderr = final_stderr or stderr
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


def terminate_process_group(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return

    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.terminate()
        process.wait(timeout=5)
    except ProcessLookupError:
        return
    except subprocess.TimeoutExpired:
        if process.poll() is not None:
            return
        try:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
        except ProcessLookupError:
            return
        process.wait()


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
