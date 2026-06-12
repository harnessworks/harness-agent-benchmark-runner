from __future__ import annotations

import os
import selectors
import signal
import subprocess
import time
from pathlib import Path
from typing import Callable, Mapping

from .models import ProcessResult


def run_process(
    command: str | list[str],
    *,
    cwd: Path,
    label: str,
    timeout_seconds: int,
    timeout_reason: str = "timeout",
    idle_timeout_seconds: int | None = None,
    idle_timeout_reason: str = "idle_watchdog",
    no_edit_timeout_seconds: int | None = None,
    no_edit_timeout_reason: str = "no_edit_watchdog",
    no_edit_has_changes: Callable[[], bool] | None = None,
    env: Mapping[str, str] | None = None,
    log_path: Path,
    tail_chars: int = 4000,
) -> ProcessResult:
    started = time.monotonic()
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    if no_edit_timeout_seconds is not None and no_edit_has_changes is None:
        raise ValueError("no_edit_has_changes is required with no_edit_timeout_seconds")

    if idle_timeout_seconds is not None or no_edit_timeout_seconds is not None:
        result = run_process_with_idle_watchdog(
            command,
            cwd=cwd,
            label=label,
            timeout_seconds=timeout_seconds,
            timeout_reason=timeout_reason,
            idle_timeout_seconds=idle_timeout_seconds,
            idle_timeout_reason=idle_timeout_reason,
            no_edit_timeout_seconds=no_edit_timeout_seconds,
            no_edit_timeout_reason=no_edit_timeout_reason,
            no_edit_has_changes=no_edit_has_changes,
            env=merged_env,
            log_path=log_path,
            tail_chars=tail_chars,
            started=started,
        )
        return result

    stdout = ""
    stderr = ""
    termination_reason: str | None = None
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
        termination_reason = timeout_reason
        exit_code = 124
        stdout = decode_output(exc.stdout)
        stderr = decode_output(exc.stderr)
        terminate_process_group(process)
        final_stdout, final_stderr = process.communicate()
        stdout = final_stdout or stdout
        stderr = final_stderr or stderr
        if timeout_reason == "stall_watchdog":
            stderr += f"\nStopped by stall watchdog after {timeout_seconds} seconds.\n"
        else:
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
        termination_reason=termination_reason,
        stdout_tail=stdout[-tail_chars:],
        stderr_tail=stderr[-tail_chars:],
    )


def run_process_with_idle_watchdog(
    command: str | list[str],
    *,
    cwd: Path,
    label: str,
    timeout_seconds: int,
    timeout_reason: str,
    idle_timeout_seconds: int | None,
    idle_timeout_reason: str,
    no_edit_timeout_seconds: int | None,
    no_edit_timeout_reason: str,
    no_edit_has_changes: Callable[[], bool] | None,
    env: Mapping[str, str],
    log_path: Path,
    tail_chars: int,
    started: float,
) -> ProcessResult:
    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=isinstance(command, str),
        start_new_session=True,
    )
    selector = selectors.DefaultSelector()
    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    streams: dict[int, tuple[str, list[bytes]]] = {}
    for name, pipe, chunks in (
        ("stdout", process.stdout, stdout_chunks),
        ("stderr", process.stderr, stderr_chunks),
    ):
        if pipe is None:
            continue
        os.set_blocking(pipe.fileno(), False)
        selector.register(pipe, selectors.EVENT_READ)
        streams[pipe.fileno()] = (name, chunks)

    timed_out = False
    termination_reason: str | None = None
    exit_code: int | None = None
    last_activity = started
    no_edit_observed = False
    next_no_edit_check = started
    timeout_message = ""

    try:
        while True:
            now = time.monotonic()
            if process.poll() is not None:
                exit_code = process.returncode
                drain_ready_streams(selector, streams)
                break

            elapsed = now - started
            wall_remaining = timeout_seconds - elapsed
            if wall_remaining <= 0:
                timed_out = True
                termination_reason = timeout_reason
                exit_code = 124
                timeout_message = timeout_message_for(timeout_reason, timeout_seconds)
                terminate_process_group(process)
                drain_ready_streams(selector, streams, timeout_seconds=1.0)
                break

            watchdog_deadlines = [wall_remaining]
            if idle_timeout_seconds is not None:
                idle_remaining = idle_timeout_seconds - (now - last_activity)
                if idle_remaining <= 0:
                    timed_out = True
                    termination_reason = idle_timeout_reason
                    exit_code = 124
                    timeout_message = (
                        f"\nStopped by idle watchdog after {idle_timeout_seconds} seconds without output.\n"
                    )
                    terminate_process_group(process)
                    drain_ready_streams(selector, streams, timeout_seconds=1.0)
                    break
                watchdog_deadlines.append(idle_remaining)

            if no_edit_timeout_seconds is not None and not no_edit_observed:
                if now >= next_no_edit_check:
                    no_edit_observed = bool(no_edit_has_changes and no_edit_has_changes())
                    next_no_edit_check = now + 1.0
                if not no_edit_observed:
                    no_edit_remaining = no_edit_timeout_seconds - elapsed
                    if no_edit_remaining <= 0:
                        no_edit_observed = bool(no_edit_has_changes and no_edit_has_changes())
                    if not no_edit_observed and no_edit_remaining <= 0:
                        timed_out = True
                        termination_reason = no_edit_timeout_reason
                        exit_code = 124
                        timeout_message = (
                            f"\nStopped by no-edit watchdog after {no_edit_timeout_seconds} "
                            "seconds without repository changes.\n"
                        )
                        terminate_process_group(process)
                        drain_ready_streams(selector, streams, timeout_seconds=1.0)
                        break
                    if not no_edit_observed:
                        watchdog_deadlines.append(no_edit_remaining)
                        watchdog_deadlines.append(next_no_edit_check - now)

            wait_time = min(0.25, *(max(0.01, remaining) for remaining in watchdog_deadlines))
            events = selector.select(wait_time)
            if not events:
                continue
            for key, _ in events:
                if read_ready_stream(key.fileobj, selector, streams):
                    last_activity = time.monotonic()
    finally:
        selector.close()
        for pipe in (process.stdout, process.stderr):
            if pipe is not None:
                pipe.close()

    duration = time.monotonic() - started
    stdout = decode_output(b"".join(stdout_chunks))
    stderr = decode_output(b"".join(stderr_chunks))
    if timeout_message:
        stderr += timeout_message
    if exit_code is None:
        exit_code = process.returncode

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
        termination_reason=termination_reason,
        stdout_tail=stdout[-tail_chars:],
        stderr_tail=stderr[-tail_chars:],
    )


def timeout_message_for(timeout_reason: str, timeout_seconds: int) -> str:
    if timeout_reason == "stall_watchdog":
        return f"\nStopped by stall watchdog after {timeout_seconds} seconds.\n"
    return f"\nTimed out after {timeout_seconds} seconds.\n"


def drain_ready_streams(
    selector: selectors.BaseSelector,
    streams: dict[int, tuple[str, list[bytes]]],
    *,
    timeout_seconds: float = 0.0,
) -> None:
    deadline = time.monotonic() + timeout_seconds
    while selector.get_map():
        wait_time = 0.0 if timeout_seconds == 0 else max(0.0, deadline - time.monotonic())
        events = selector.select(wait_time)
        if not events:
            break
        for key, _ in events:
            read_ready_stream(key.fileobj, selector, streams)
        if timeout_seconds != 0 and time.monotonic() >= deadline:
            break


def read_ready_stream(
    stream: object,
    selector: selectors.BaseSelector,
    streams: dict[int, tuple[str, list[bytes]]],
) -> bool:
    fileno = stream.fileno()  # type: ignore[attr-defined]
    try:
        data = os.read(fileno, 8192)
    except BlockingIOError:
        return False
    if not data:
        try:
            selector.unregister(stream)
        except KeyError:
            pass
        streams.pop(fileno, None)
        return False
    streams[fileno][1].append(data)
    return True


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
