from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "triage_no_edit_stalls.py"
SPEC = importlib.util.spec_from_file_location("triage_no_edit_stalls", SCRIPT_PATH)
assert SPEC is not None
stall_triage = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["triage_no_edit_stalls"] = stall_triage
SPEC.loader.exec_module(stall_triage)


class NoEditStallTriageScriptTests(unittest.TestCase):
    def test_formats_empty_triage(self) -> None:
        markdown = stall_triage.format_markdown([record("alpha", termination_reason=None)])

        self.assertIn("## No-Edit Stall Triage", markdown)
        self.assertIn("No-edit watchdog records: 0", markdown)
        self.assertNotIn("| Run ID |", markdown)

    def test_extracts_last_codex_message_and_classifies_post_planning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "agent.log"
            log_path.write_text(
                "\n".join(
                    [
                        "codex",
                        "I found the decision record.",
                        "exec",
                        "rg -n price docs",
                        " succeeded in 0ms:",
                        "codex",
                        "I'm going to add the reusable helper, route, and tests.",
                        "",
                        "Stopped by no-edit watchdog after 360 seconds without repository changes.",
                    ]
                ),
                encoding="utf-8",
            )
            item = record(
                "alpha",
                log_path=log_path,
                termination_reason="no_edit_watchdog",
                watchdog={
                    "seconds_without_observed_repo_changes": 360.04,
                    "seconds_since_last_output": 83.269,
                },
            )

            markdown = stall_triage.format_markdown([item])

        self.assertIn("No-edit watchdog records: 1", markdown)
        self.assertIn("`full-harness`", markdown)
        self.assertIn("360.0s", markdown)
        self.assertIn("83.3s", markdown)
        self.assertIn("post-planning", markdown)
        self.assertIn("I'm going to add the reusable helper, route, and tests.", markdown)

    def test_missing_log_keeps_unknown_phase(self) -> None:
        item = record(
            "alpha",
            termination_reason="no_edit_watchdog",
            watchdog={"seconds_without_observed_repo_changes": 180},
        )

        stalls = stall_triage.collect_no_edit_stalls([item], message_chars=80)

        self.assertEqual(stalls[0].last_codex_phase, "unknown")
        self.assertEqual(stalls[0].last_codex_message, "-")


def record(
    task_id: str,
    *,
    log_path: Path | None = None,
    termination_reason: str | None,
    watchdog: dict[str, object] | None = None,
) -> dict[str, object]:
    agent: dict[str, object] = {
        "duration_seconds": 360.04,
        "log_path": str(log_path) if log_path else None,
    }
    if termination_reason is not None:
        agent["termination_reason"] = termination_reason
    if watchdog is not None:
        agent["watchdog"] = watchdog
    return {
        "run_id": "20260614T000000Z-alpha-deadbeef",
        "repo": {"source": "../flask-memory-harness"},
        "task": {
            "id": task_id,
            "benchmark": {"target_arm": "full-harness"},
        },
        "agent": agent,
        "scoring": {
            "agent_stalled": termination_reason == "no_edit_watchdog",
            "agent_timed_out": termination_reason == "no_edit_watchdog",
        },
    }


if __name__ == "__main__":
    unittest.main()
