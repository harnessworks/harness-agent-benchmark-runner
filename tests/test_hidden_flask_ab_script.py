from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_hidden_flask_ab.py"
SPEC = importlib.util.spec_from_file_location("run_hidden_flask_ab", SCRIPT_PATH)
assert SPEC is not None
hidden_ab = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["run_hidden_flask_ab"] = hidden_ab
SPEC.loader.exec_module(hidden_ab)


class HiddenFlaskABScriptTests(unittest.TestCase):
    def test_current_hidden_flask_task_set_has_large_ab_shape(self) -> None:
        pairs = hidden_ab.load_task_pairs(hidden_ab.DEFAULT_TASK_DIR)
        hidden_ab.validate_pairs(pairs)

        self.assertEqual(len(pairs), 10)
        for pair in pairs:
            for task_path in (pair.no_harness, pair.yes_harness):
                data = hidden_ab.read_json(task_path)
                self.assertNotEqual(data["repo"]["ref"], "HEAD")

    def test_loads_pairs_and_alternates_schedule(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp)
            write_hidden_task(task_dir / "alpha-no-harness.json", "alpha", "../flask-no-harness")
            write_hidden_task(task_dir / "alpha-yes-harness.json", "alpha", "../flask-yes-harness")

            pairs = hidden_ab.load_task_pairs(task_dir)
            hidden_ab.validate_pairs(pairs)
            schedule = hidden_ab.build_schedule(pairs, repeats=2, pair_order="alternate")

            self.assertEqual([pair.task_id for pair in pairs], ["alpha"])
            self.assertEqual(
                [item.group for item in schedule],
                ["A:no-harness", "B:yes-harness", "B:yes-harness", "A:no-harness"],
            )

    def test_large_mode_requires_enough_task_pairs_by_default(self) -> None:
        pair = hidden_ab.TaskPair(
            task_id="alpha",
            no_harness=Path("alpha-no-harness.json"),
            yes_harness=Path("alpha-yes-harness.json"),
        )
        args = Namespace(mode="large", large_min_task_pairs=8, allow_small_large=False)

        with self.assertRaises(hidden_ab.BenchmarkPlanError):
            hidden_ab.validate_run_shape(args, [pair])

    def test_allows_small_large_when_explicit(self) -> None:
        pair = hidden_ab.TaskPair(
            task_id="alpha",
            no_harness=Path("alpha-no-harness.json"),
            yes_harness=Path("alpha-yes-harness.json"),
        )
        args = Namespace(mode="large", large_min_task_pairs=8, allow_small_large=True)

        hidden_ab.validate_run_shape(args, [pair])


def write_hidden_task(path: Path, task_id: str, repo_source: str) -> None:
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "id": task_id,
                "description": "fixture hidden task",
                "repo": {"source": repo_source, "ref": "abc123"},
                "prompt": "Use repository conventions.",
                "timeout_seconds": 600,
                "max_attempts": 1,
                "max_cost_usd": 1.0,
                "expected_files": ["app/**", "tests/**", "docs/**"],
                "forbidden_files": ["benchmarks/**"],
                "verification": {
                    "commands": [
                        {
                            "name": "hidden oracle",
                            "command": ["bash", "run_flask_hidden_checks.sh", task_id],
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
