#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from harness_agent_benchmark_runner.summary import load_results  # noqa: E402


@dataclass
class Aggregate:
    runs: int = 0
    successes: int = 0
    verification_passed: int = 0
    wrong_file_edits: int = 0
    forbidden_file_edits: int = 0
    timeouts: int = 0
    durations: list[float] = field(default_factory=list)

    def update(self, record: dict[str, Any]) -> None:
        scoring = record.get("scoring", {})
        self.runs += 1
        if scoring.get("success") is True:
            self.successes += 1
        if scoring.get("verification_passed") is True:
            self.verification_passed += 1
        self.wrong_file_edits += int(scoring.get("wrong_file_edits") or 0)
        self.forbidden_file_edits += int(scoring.get("forbidden_file_edits") or 0)
        if scoring.get("agent_timed_out") is True:
            self.timeouts += 1
        duration = record.get("agent", {}).get("duration_seconds")
        if isinstance(duration, (int, float)):
            self.durations.append(float(duration))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize hidden Flask A/B JSONL results as public-safe Markdown.",
    )
    parser.add_argument("--results", required=True, help="JSONL file or results directory")
    args = parser.parse_args(argv)

    records = load_results(args.results)
    print(format_markdown(records))
    return 0


def format_markdown(records: list[dict[str, Any]]) -> str:
    by_target: dict[str, Aggregate] = defaultdict(Aggregate)
    by_target_task: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)

    for record in records:
        target = target_label(record)
        task_id = str(record.get("task", {}).get("id", "unknown"))
        by_target[target].update(record)
        by_target_task[(target, task_id)].update(record)

    lines = [
        "## Headline",
        "",
        "| Target | Runs | Successes | Success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for target, values in sorted(by_target.items()):
        lines.append(headline_row(target, values))

    lines.extend(
        [
            "",
            "## Per-Task Results",
            "",
            "| Target | Task | Runs | Successes | Success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for (target, task_id), values in sorted(by_target_task.items()):
        lines.append(task_row(target, task_id, values))
    return "\n".join(lines)


def headline_row(target: str, values: Aggregate) -> str:
    return (
        f"| `{target}` | {values.runs} | {values.successes} | {rate(values.successes, values.runs)} | "
        f"{values.verification_passed} | {values.wrong_file_edits} | {values.forbidden_file_edits} | "
        f"{values.timeouts} | {duration(percentile(values.durations, 50))} | "
        f"{duration(percentile(values.durations, 95))} |"
    )


def task_row(target: str, task_id: str, values: Aggregate) -> str:
    return (
        f"| `{target}` | `{task_id}` | {values.runs} | {values.successes} | "
        f"{rate(values.successes, values.runs)} | {values.verification_passed} | "
        f"{values.wrong_file_edits} | {values.forbidden_file_edits} | {values.timeouts} | "
        f"{duration(percentile(values.durations, 50))} | {duration(percentile(values.durations, 95))} |"
    )


def target_label(record: dict[str, Any]) -> str:
    source = str(record.get("repo", {}).get("source", "unknown"))
    if "flask-no-harness" in source:
        return "flask-no-harness"
    if "flask-yes-harness" in source:
        return "flask-yes-harness"
    return source


def rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "-"
    return f"{(numerator / denominator) * 100:.1f}%"


def percentile(values: list[float], percentile_value: int) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, math.ceil((percentile_value / 100) * len(ordered)) - 1)
    return ordered[index]


def duration(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.0f}s"


if __name__ == "__main__":
    raise SystemExit(main())
