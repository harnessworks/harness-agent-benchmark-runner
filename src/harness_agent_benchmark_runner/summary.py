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
        "strict_successes": 0,
        "functional_successes": 0,
        "schema_contract_successes": 0,
        "workflow_successes": 0,
        "boundary_successes": 0,
        "execution_successes": 0,
        "preflight_failures": 0,
        "verification_passed": 0,
        "first_pass_verification": 0,
        "agent_timeouts": 0,
        "agent_stalls": 0,
        "wrong_file_edits": 0,
        "forbidden_file_edits": 0,
        "runner_errors": 0,
    }


def update_counter(counter: dict[str, int], scoring: dict[str, Any]) -> None:
    counter["runs"] += 1
    if scoring.get("success") is True:
        counter["successes"] += 1
    if scoring.get("strict_success", scoring.get("success")) is True:
        counter["strict_successes"] += 1
    if scoring.get("functional_success") is True:
        counter["functional_successes"] += 1
    if scoring.get("schema_contract_success") is True:
        counter["schema_contract_successes"] += 1
    if scoring.get("workflow_success") is True:
        counter["workflow_successes"] += 1
    if scoring.get("boundary_success") is True:
        counter["boundary_successes"] += 1
    if scoring.get("execution_success") is True:
        counter["execution_successes"] += 1
    if scoring.get("preflight_passed") is False:
        counter["preflight_failures"] += 1
    if scoring.get("verification_passed") is True:
        counter["verification_passed"] += 1
    if scoring.get("first_pass_verification") is True:
        counter["first_pass_verification"] += 1
    if scoring.get("agent_timed_out") is True:
        counter["agent_timeouts"] += 1
    if scoring.get("agent_stalled") is True:
        counter["agent_stalls"] += 1
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
            f"Strict successes: {total['strict_successes']}",
            f"Functional successes: {total['functional_successes']}",
            f"Schema-contract successes: {total['schema_contract_successes']}",
            f"Workflow successes: {total['workflow_successes']}",
            f"Boundary successes: {total['boundary_successes']}",
            f"Execution successes: {total['execution_successes']}",
            f"Preflight failures: {total['preflight_failures']}",
            f"Verification passed: {total['verification_passed']}",
            f"First-pass verification: {total['first_pass_verification']}",
            f"Agent timeouts: {total['agent_timeouts']}",
            f"Agent stalls: {total['agent_stalls']}",
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
            f"strict_successes={values['strict_successes']}, "
            f"functional_successes={values['functional_successes']}, "
            f"schema_contract_successes={values['schema_contract_successes']}, "
            f"workflow_successes={values['workflow_successes']}, "
            f"boundary_successes={values['boundary_successes']}, "
            f"execution_successes={values['execution_successes']}, "
            f"preflight_failures={values['preflight_failures']}, "
            f"verification_passed={values['verification_passed']}, "
            f"first_pass_verification={values['first_pass_verification']}, "
            f"agent_timeouts={values['agent_timeouts']}, "
            f"agent_stalls={values['agent_stalls']}, "
            f"wrong_file_edits={values['wrong_file_edits']}, "
            f"forbidden_file_edits={values['forbidden_file_edits']}, "
            f"runner_errors={values['runner_errors']}"
        )
    return "\n".join(lines)
