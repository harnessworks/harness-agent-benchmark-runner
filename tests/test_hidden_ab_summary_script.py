from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "summarize_hidden_ab.py"
SPEC = importlib.util.spec_from_file_location("summarize_hidden_ab", SCRIPT_PATH)
assert SPEC is not None
hidden_summary = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["summarize_hidden_ab"] = hidden_summary
SPEC.loader.exec_module(hidden_summary)


class HiddenABSummaryScriptTests(unittest.TestCase):
    def test_formats_ab_markdown_with_duration_percentiles(self) -> None:
        records = [
            record("../flask-no-harness", "alpha", False, False, 10),
            record("../flask-no-harness", "alpha", True, True, 30),
            record("../flask-yes-harness", "alpha", True, True, 20),
            record("../flask-yes-harness", "beta", True, True, 40),
        ]

        markdown = hidden_summary.format_markdown(records)

        self.assertIn("| `flask-no-harness` | 2 | 1 | 50.0% | 1 |", markdown)
        self.assertIn("| `flask-yes-harness` | 2 | 2 | 100.0% | 2 |", markdown)
        self.assertIn("| `flask-no-harness` | `alpha` | 2 | 1 | 50.0% |", markdown)
        self.assertIn("30s", markdown)


def record(
    source: str,
    task_id: str,
    success: bool,
    verification_passed: bool,
    duration_seconds: float,
) -> dict[str, object]:
    return {
        "repo": {"source": source},
        "task": {"id": task_id},
        "agent": {"duration_seconds": duration_seconds},
        "scoring": {
            "success": success,
            "verification_passed": verification_passed,
            "agent_timed_out": False,
            "wrong_file_edits": 0,
            "forbidden_file_edits": 0,
        },
    }


if __name__ == "__main__":
    unittest.main()
