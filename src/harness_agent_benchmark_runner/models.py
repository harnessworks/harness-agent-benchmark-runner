from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RepoSpec:
    source: str
    ref: str = "HEAD"


@dataclass(frozen=True)
class CommandSpec:
    command: str | list[str]
    name: str | None = None
    timeout_seconds: int | None = None

    @property
    def label(self) -> str:
        if self.name:
            return self.name
        if isinstance(self.command, str):
            return self.command
        return " ".join(self.command)


@dataclass(frozen=True)
class TaskSpec:
    schema_version: int
    task_id: str
    description: str
    repo: RepoSpec
    prompt: str
    prompt_ref: str | None = None
    timeout_seconds: int = 900
    max_attempts: int = 1
    max_cost_usd: float | None = None
    expected_files: tuple[str, ...] = ()
    forbidden_files: tuple[str, ...] = ()
    verification_commands: tuple[CommandSpec, ...] = ()
    source_path: Path | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: Path | None = None) -> "TaskSpec":
        require_type(data, "schema_version", int)
        require_type(data, "id", str)
        require_type(data, "description", str)
        require_type(data, "repo", dict)
        require_type(data, "prompt", str)

        repo_data = data["repo"]
        require_type(repo_data, "source", str)
        repo_ref = repo_data.get("ref", "HEAD")
        if not isinstance(repo_ref, str):
            raise ValueError("repo.ref must be a string when provided")

        verification_data = data.get("verification", {})
        if verification_data is None:
            verification_data = {}
        if not isinstance(verification_data, dict):
            raise ValueError("verification must be an object when provided")

        raw_commands = verification_data.get("commands", [])
        if not isinstance(raw_commands, list):
            raise ValueError("verification.commands must be a list")

        commands = tuple(parse_command_spec(item) for item in raw_commands)

        return cls(
            schema_version=data["schema_version"],
            task_id=data["id"],
            description=data["description"],
            repo=RepoSpec(source=repo_data["source"], ref=repo_ref),
            prompt=data["prompt"],
            prompt_ref=optional_string(data, "prompt_ref"),
            timeout_seconds=positive_int(data, "timeout_seconds", default=900),
            max_attempts=positive_int(data, "max_attempts", default=1),
            max_cost_usd=optional_non_negative_float(data, "max_cost_usd"),
            expected_files=tuple(string_list(data, "expected_files")),
            forbidden_files=tuple(string_list(data, "forbidden_files")),
            verification_commands=commands,
            source_path=source_path,
        )


def parse_command_spec(value: Any) -> CommandSpec:
    if isinstance(value, str):
        return CommandSpec(command=value)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return CommandSpec(command=value)
    if isinstance(value, dict):
        command = value.get("command")
        if not isinstance(command, str) and not (
            isinstance(command, list) and all(isinstance(item, str) for item in command)
        ):
            raise ValueError("verification command must be a string or list of strings")
        name = value.get("name")
        if name is not None and not isinstance(name, str):
            raise ValueError("verification command name must be a string")
        timeout = value.get("timeout_seconds")
        if timeout is not None and (
            isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0
        ):
            raise ValueError("verification command timeout_seconds must be a positive integer")
        return CommandSpec(command=command, name=name, timeout_seconds=timeout)
    raise ValueError("verification command entries must be strings, lists, or objects")


def require_type(data: dict[str, Any], key: str, expected_type: type) -> None:
    if key not in data:
        raise ValueError(f"missing required field: {key}")
    if not isinstance(data[key], expected_type):
        raise ValueError(f"{key} must be {expected_type.__name__}")


def optional_string(data: dict[str, Any], key: str) -> str | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string when provided")
    return value


def positive_int(data: dict[str, Any], key: str, default: int) -> int:
    value = data.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{key} must be a positive integer when provided")
    return value


def optional_non_negative_float(data: dict[str, Any], key: str) -> float | None:
    value = data.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise ValueError(f"{key} must be a non-negative number when provided")
    return float(value)


def string_list(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a list of strings when provided")
    return value


@dataclass(frozen=True)
class ProcessResult:
    label: str
    command: str | list[str]
    cwd: str
    exit_code: int
    duration_seconds: float
    log_path: str
    timed_out: bool = False
    stdout_tail: str = ""
    stderr_tail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "command": self.command,
            "cwd": self.cwd,
            "exit_code": self.exit_code,
            "duration_seconds": round(self.duration_seconds, 3),
            "log_path": self.log_path,
            "timed_out": self.timed_out,
            "stdout_tail": self.stdout_tail,
            "stderr_tail": self.stderr_tail,
        }


@dataclass(frozen=True)
class RunnerConfig:
    agent_command: str
    workspace_root: Path = Path("runs")
    results_dir: Path = Path("results")
    keep_runs: bool = True
    default_command_timeout_seconds: int = 300
    max_attempts_override: int | None = None
    max_agent_timeout_seconds: int | None = None
    max_cost_usd_override: float | None = None
    output_tail_chars: int = 4000
    repo_source_override: str | None = None
    repo_ref_override: str | None = None
    extra_env: dict[str, str] = field(default_factory=dict)
