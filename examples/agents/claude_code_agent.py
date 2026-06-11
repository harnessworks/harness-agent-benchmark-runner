#!/usr/bin/env python3
"""Claude Code adapter for the benchmark runner.

The runner executes this inside each isolated clone with the standard
BENCHMARK_* environment variables. This adapter feeds the task prompt to the
Claude Code CLI in non-interactive mode and lets it edit the clone in place.

Requires an authenticated Claude Code CLI on the host (`claude login` or an
`ANTHROPIC_API_KEY` in the environment). It will NOT work in an environment
where `claude` reports "Not logged in".

Optional environment knobs:
- CLAUDE_BIN: Claude Code binary, default "claude"
- CLAUDE_MODEL: model passed as --model (e.g. "opus", "sonnet")
- CLAUDE_PERMISSION_MODE: default "bypassPermissions" (non-interactive edits)
- CLAUDE_MAX_TURNS: optional --max-turns value for print mode
- CLAUDE_NO_SESSION_PERSISTENCE: default "1"; pass --no-session-persistence
- CLAUDE_PROMPT_ARG: short instruction passed as the print-mode query
- CLAUDE_EXTRA_ARGS: extra shell-parsed args appended to the command
"""
from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path

DEFAULT_PROMPT_ARG = (
    "Read the benchmark task from stdin, edit the current repository in place, "
    "and stop when the task should pass its verification commands."
)


def required_path(name: str) -> Path:
    value = os.environ.get(name)
    if not value:
        print(f"missing required environment variable: {name}", file=sys.stderr)
        raise SystemExit(2)
    return Path(value).expanduser().resolve()


def env_enabled(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() not in {"", "0", "false", "no", "off"}


def build_command() -> list[str]:
    command = [os.environ.get("CLAUDE_BIN", "claude"), "-p"]

    permission_mode = os.environ.get("CLAUDE_PERMISSION_MODE", "bypassPermissions")
    if permission_mode:
        command.extend(["--permission-mode", permission_mode])

    model = os.environ.get("CLAUDE_MODEL")
    if model:
        command.extend(["--model", model])

    max_cost = os.environ.get("BENCHMARK_MAX_COST_USD")
    if max_cost:
        command.extend(["--max-budget-usd", max_cost])

    max_turns = os.environ.get("CLAUDE_MAX_TURNS")
    if max_turns:
        command.extend(["--max-turns", max_turns])

    if env_enabled("CLAUDE_NO_SESSION_PERSISTENCE", default=True):
        command.append("--no-session-persistence")

    extra_args = os.environ.get("CLAUDE_EXTRA_ARGS")
    if extra_args:
        try:
            command.extend(shlex.split(extra_args))
        except ValueError as exc:
            raise ValueError(f"invalid CLAUDE_EXTRA_ARGS: {exc}") from exc

    command.append(os.environ.get("CLAUDE_PROMPT_ARG", DEFAULT_PROMPT_ARG))

    return command


def main() -> int:
    repo = required_path("BENCHMARK_REPO")
    prompt = required_path("BENCHMARK_PROMPT_FILE").read_text(encoding="utf-8")

    try:
        command = build_command()
    except ValueError as exc:
        print(f"claude adapter error: {exc}", file=sys.stderr)
        return 2

    completed = subprocess.run(
        command,
        cwd=str(repo),
        input=prompt,
        text=True,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
