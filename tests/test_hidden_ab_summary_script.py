from __future__ import annotations

import importlib.util
import sys
import tempfile
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

        self.assertIn("Strict scored successes", markdown)
        self.assertIn("Verification passed", markdown)
        self.assertIn("Wrong-file edits", markdown)
        self.assertIn("Hidden access", markdown)
        self.assertIn("Stalls", markdown)
        self.assertIn("| `flask-no-harness` | 2 | 1 | 50.0% | 1 |", markdown)
        self.assertIn("| `flask-yes-harness` | 2 | 2 | 100.0% | 2 |", markdown)
        self.assertIn("| `flask-no-harness` | `alpha` | 2 | 1 | 50.0% |", markdown)
        self.assertIn("30s", markdown)

    def test_counts_direct_hidden_access_without_counting_docs_mentions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hidden_log = root / "hidden.log"
            hidden_log.write_text(
                "/bin/zsh -lc 'rg --files benchmarks/oracles benchmarks/tasks'\n",
                encoding="utf-8",
            )
            docs_log = root / "docs.log"
            docs_log.write_text(
                "Focused oracle gate: bash benchmarks/oracles/run_checks.sh <task-id>\n",
                encoding="utf-8",
            )
            records = [
                record("../flask-yes-harness", "alpha", False, False, 20, hidden_log),
                record("../flask-no-harness", "alpha", False, False, 10, docs_log),
            ]

            markdown = hidden_summary.format_markdown(records)

        self.assertIn("| `flask-yes-harness` | 1 | 0 | 0.0% | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |", markdown)
        self.assertIn("| `flask-no-harness` | 1 | 0 | 0.0% | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |", markdown)


def record(
    source: str,
    task_id: str,
    success: bool,
    verification_passed: bool,
    duration_seconds: float,
    log_path: Path | None = None,
) -> dict[str, object]:
    return {
        "repo": {"source": source},
        "task": {"id": task_id},
        "agent": {"duration_seconds": duration_seconds, "log_path": str(log_path) if log_path else None},
        "scoring": {
            "success": success,
            "verification_passed": verification_passed,
            "agent_timed_out": False,
            "agent_stalled": False,
            "wrong_file_edits": 0,
            "forbidden_file_edits": 0,
        },
    }


if __name__ == "__main__":
    unittest.main()
