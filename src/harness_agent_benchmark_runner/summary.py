from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_results(path: str | Path) -> list[dict[str, Any]]:
    result_path = Path(path).expanduser()
    files: list[Path]
    if result_path.is_file():
        files = [result_path]
    else:
        files = sorted(result_path.glob("*.jsonl"))

    records: list[dict[str, Any]] = []
    for file_path in files:
        with file_path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    data = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{file_path}:{line_number}: invalid JSONL record") from exc
                if isinstance(data, dict):
                    records.append(data)
    return records


def summarize_results(records: list[dict[str, Any]]) -> dict[str, Any]:
    totals = new_counter()
    by_task: dict[str, dict[str, int]] = defaultdict(new_counter)

    for record in records:
        task_id = str(record.get("task", {}).get("id", "unknown"))
        scoring = record.get("scoring", {})
        update_counter(totals, scoring)
        update_counter(by_task[task_id], scoring)

    return {
        "total": totals,
        "by_task": dict(sorted(by_task.items())),
    }


def new_counter() -> dict[str, int]:
    return {
        "runs": 0,
        "successes": 0,
        "verification_passed": 0,
        "wrong_file_edits": 0,
        "forbidden_file_edits": 0,
        "runner_errors": 0,
    }


def update_counter(counter: dict[str, int], scoring: dict[str, Any]) -> None:
    counter["runs"] += 1
    if scoring.get("success") is True:
        counter["successes"] += 1
    if scoring.get("verification_passed") is True:
        counter["verification_passed"] += 1
    counter["wrong_file_edits"] += int(scoring.get("wrong_file_edits") or 0)
    counter["forbidden_file_edits"] += int(scoring.get("forbidden_file_edits") or 0)
    if scoring.get("runner_error"):
        counter["runner_errors"] += 1


def format_summary(summary: dict[str, Any]) -> str:
    lines = ["Benchmark Summary", ""]
    total = summary["total"]
    lines.extend(
        [
            f"Runs: {total['runs']}",
            f"Successes: {total['successes']}",
            f"Verification passed: {total['verification_passed']}",
            f"Wrong-file edits: {total['wrong_file_edits']}",
            f"Forbidden-file edits: {total['forbidden_file_edits']}",
            f"Runner errors: {total['runner_errors']}",
            "",
            "By task:",
        ]
    )

    for task_id, values in summary["by_task"].items():
        lines.append(
            "- "
            f"{task_id}: runs={values['runs']}, successes={values['successes']}, "
            f"verification_passed={values['verification_passed']}, "
            f"wrong_file_edits={values['wrong_file_edits']}, "
            f"forbidden_file_edits={values['forbidden_file_edits']}, "
            f"runner_errors={values['runner_errors']}"
        )
    return "\n".join(lines)
