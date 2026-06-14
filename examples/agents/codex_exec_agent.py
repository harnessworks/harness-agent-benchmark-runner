#!/usr/bin/env python3
"""Codex CLI adapter for benchmark tasks.

The runner executes this inside each isolated clone with the standard
BENCHMARK_* environment variables. This adapter feeds the task prompt to
`codex exec` and lets it edit the clone in place.

Optional environment knobs:
- CODEX_BIN: Codex binary, default "codex"
- CODEX_APPROVAL_POLICY: default "never"
- CODEX_SANDBOX: default "workspace-write"
- CODEX_MODEL: optional model passed as --model
- CODEX_PROFILE: optional profile passed as --profile
- CODEX_IGNORE_USER_CONFIG: default enabled unless CODEX_PROFILE is set
- CODEX_IGNORE_RULES: default enabled; disables user/project execpolicy .rules
- CODEX_DISABLE_PLUGINS: default enabled; disables Codex plugin loading
- CODEX_PROMPT_GUARD: default disabled; prepends generic benchmark guardrails
- CODEX_PROMPT_PREFIX: override the default benchmark guardrail prefix
- CODEX_PROMPT_SUFFIX: optional prompt text appended after the task prompt
- CODEX_EXEC_ARGS: extra shell-parsed args appended to the `codex exec` command
"""
from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path


DEFAULT_PROMPT_PREFIX = """You are completing one benchmark task in an isolated repository clone.

Keep exploration short and implementation-focused:
- Read only app code, tests, README/docs, and project guidance needed for this task.
- Do not inspect benchmark task specs, benchmark oracle code, previous runs/results, credentials, or git history unless the task prompt explicitly asks.
- If companion docs are requested and no docs directory exists, create a focused docs/ note; do not update the root README unless explicitly asked.
- After you identify the relevant implementation direction, start a small scoped repository edit before extended additional analysis.
- Make focused edits, run focused tests when practical, and stop once the task should pass verification."""


def main() -> int:
    repo = required_path("BENCHMARK_REPO")
    prompt_file = required_path("BENCHMARK_PROMPT_FILE")
    prompt = build_prompt(prompt_file.read_text(encoding="utf-8"))

    try:
        command = build_command(repo)
    except ValueError as exc:
        print(f"codex adapter error: {exc}", file=sys.stderr)
        return 2

    completed = subprocess.run(
        command,
        cwd=str(repo),
        input=prompt,
        text=True,
        check=False,
    )
    return completed.returncode


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


def build_prompt(task_prompt: str) -> str:
    parts: list[str] = []
    if env_enabled("CODEX_PROMPT_GUARD", default=False):
        prefix = os.environ.get("CODEX_PROMPT_PREFIX", DEFAULT_PROMPT_PREFIX)
        if prefix.strip():
            parts.append(prefix.strip())

    if task_prompt.strip():
        parts.append(task_prompt.strip())

    suffix = os.environ.get("CODEX_PROMPT_SUFFIX", "")
    if suffix.strip():
        parts.append(suffix.strip())

    return "\n\n".join(parts) + "\n"


def build_command(repo: Path) -> list[str]:
    command = [os.environ.get("CODEX_BIN", "codex")]

    approval_policy = os.environ.get("CODEX_APPROVAL_POLICY", "never")
    if approval_policy:
        command.extend(["--ask-for-approval", approval_policy])

    sandbox = os.environ.get("CODEX_SANDBOX", "workspace-write")
    if sandbox:
        command.extend(["--sandbox", sandbox])

    model = os.environ.get("CODEX_MODEL")
    if model:
        command.extend(["--model", model])

    profile = os.environ.get("CODEX_PROFILE")
    if profile:
        command.extend(["--profile", profile])

    command.extend(["exec", "--cd", str(repo), "--skip-git-repo-check", "--ephemeral"])

    if env_enabled("CODEX_IGNORE_USER_CONFIG", default=profile is None):
        command.append("--ignore-user-config")

    extra_args = os.environ.get("CODEX_EXEC_ARGS")
    if extra_args:
        try:
            command.extend(shlex.split(extra_args))
        except ValueError as exc:
            raise ValueError(f"invalid CODEX_EXEC_ARGS: {exc}") from exc

    if env_enabled("CODEX_IGNORE_RULES", default=True):
        command.append("--ignore-rules")

    if env_enabled("CODEX_DISABLE_PLUGINS", default=True):
        command.extend(["--disable", "plugins"])

    command.append("-")
    return command


if __name__ == "__main__":
    raise SystemExit(main())
