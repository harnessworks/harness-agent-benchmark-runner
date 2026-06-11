#!/usr/bin/env python3
from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo = required_path("BENCHMARK_REPO")
    prompt_file = required_path("BENCHMARK_PROMPT_FILE")
    prompt = prompt_file.read_text(encoding="utf-8")

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

    extra_args = os.environ.get("CODEX_EXEC_ARGS")
    if extra_args:
        try:
            command.extend(shlex.split(extra_args))
        except ValueError as exc:
            raise ValueError(f"invalid CODEX_EXEC_ARGS: {exc}") from exc

    command.append("-")
    return command


if __name__ == "__main__":
    raise SystemExit(main())
