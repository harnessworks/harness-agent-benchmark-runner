#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from harness_agent_benchmark_runner.summary import load_results  # noqa: E402


SPEAKER_MARKERS = {"codex", "exec", "user", "assistant", "system"}
PLANNING_RE = re.compile(
    r"\b("
    r"i(?:'|’)m going to|i am going to|i(?:'|’)ll|i will|"
    r"we(?:'|’)ll|we will|going to|next,? i|plan|"
    r"add|update|implement|wire|expose"
    r")\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class NoEditStall:
    run_id: str
    target: str
    task_id: str
    duration_seconds: float | None
    seconds_without_repo_change: float | None
    seconds_since_last_output: float | None
    last_codex_phase: str
    last_codex_message: str
    log_path: str


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Triage no-edit watchdog stops from hidden benchmark JSONL results.",
    )
    parser.add_argument("--results", required=True, help="JSONL file or results directory")
    parser.add_argument(
        "--message-chars",
        type=positive_int,
        default=180,
        help="maximum last Codex message characters to include in the Markdown table",
    )
    args = parser.parse_args(argv)

    records = load_results(args.results)
    print(format_markdown(records, message_chars=args.message_chars))
    return 0


def format_markdown(records: list[dict[str, Any]], *, message_chars: int = 180) -> str:
    stalls = collect_no_edit_stalls(records, message_chars=message_chars)
    lines = [
        "## No-Edit Stall Triage",
        "",
        f"No-edit watchdog records: {len(stalls)}",
    ]
    if not stalls:
        return "\n".join(lines)

    lines.extend(
        [
            "",
            "| Run ID | Target | Task | Duration | Seconds without repo change | Seconds since last output | Last Codex phase | Last Codex message |",
            "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for stall in stalls:
        lines.append(
            "| "
            f"`{escape_cell(stall.run_id)}` | "
            f"`{escape_cell(stall.target)}` | "
            f"`{escape_cell(stall.task_id)}` | "
            f"{duration(stall.duration_seconds)} | "
            f"{duration(stall.seconds_without_repo_change)} | "
            f"{duration(stall.seconds_since_last_output)} | "
            f"{escape_cell(stall.last_codex_phase)} | "
            f"{escape_cell(stall.last_codex_message)} |"
        )
    return "\n".join(lines)


def collect_no_edit_stalls(
    records: list[dict[str, Any]], *, message_chars: int
) -> list[NoEditStall]:
    stalls: list[NoEditStall] = []
    for record in records:
        agent = record.get("agent", {})
        if not isinstance(agent, dict):
            continue
        if agent.get("termination_reason") != "no_edit_watchdog":
            continue
        watchdog = agent.get("watchdog", {})
        if not isinstance(watchdog, dict):
            watchdog = {}
        last_message = read_last_codex_message(agent.get("log_path"), max_chars=message_chars)
        stalls.append(
            NoEditStall(
                run_id=str(record.get("run_id", "unknown")),
                target=target_label(record),
                task_id=str(record.get("task", {}).get("id", "unknown")),
                duration_seconds=as_number(agent.get("duration_seconds")),
                seconds_without_repo_change=as_number(
                    watchdog.get("seconds_without_observed_repo_changes")
                ),
                seconds_since_last_output=as_number(watchdog.get("seconds_since_last_output")),
                last_codex_phase=classify_last_codex_message(last_message),
                last_codex_message=last_message or "-",
                log_path=str(agent.get("log_path") or ""),
            )
        )
    return stalls


def read_last_codex_message(log_path: object, *, max_chars: int) -> str:
    if not isinstance(log_path, str):
        return ""
    path = Path(log_path)
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    messages: list[str] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "codex":
            index += 1
            continue
        index += 1
        message_lines: list[str] = []
        while index < len(lines):
            stripped = lines[index].strip()
            if stripped in SPEAKER_MARKERS:
                break
            if stripped.startswith("Stopped by no-edit watchdog"):
                break
            message_lines.append(lines[index])
            index += 1
        message = compact_text("\n".join(message_lines))
        if message:
            messages.append(message)
    if not messages:
        return ""
    return truncate(messages[-1], max_chars)


def classify_last_codex_message(message: str) -> str:
    if not message:
        return "unknown"
    if PLANNING_RE.search(message):
        return "post-planning"
    return "after-agent-output"


def target_label(record: dict[str, Any]) -> str:
    benchmark = record.get("task", {}).get("benchmark", {})
    if isinstance(benchmark, dict) and isinstance(benchmark.get("target_arm"), str):
        return benchmark["target_arm"]
    return str(record.get("repo", {}).get("source", "unknown"))


def compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 1)].rstrip() + "…"


def duration(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.1f}s"


def as_number(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
