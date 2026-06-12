from __future__ import annotations

import importlib.util
import io
import json
import contextlib
import sys
import threading
import time
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_hidden_flask_ab.py"
REPO_ROOT = Path(__file__).resolve().parents[1]
BALANCED_TASK_DIR = REPO_ROOT / "benchmarks" / "tasks" / "flask-hidden-balanced"
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

    def test_current_hidden_flask_ab_prompts_match_within_pairs(self) -> None:
        pairs = hidden_ab.load_task_pairs(hidden_ab.DEFAULT_TASK_DIR)
        hidden_ab.validate_pairs(pairs)

        for pair in pairs:
            no_harness = hidden_ab.read_json(pair.no_harness)
            yes_harness = hidden_ab.read_json(pair.yes_harness)

            self.assertEqual(
                no_harness["prompt"],
                yes_harness["prompt"],
                msg=f"{pair.task_id} prompt differs between A/B targets",
            )

    def test_hidden_flask_docs_boundary_excludes_root_readme_explicitly(self) -> None:
        pairs = hidden_ab.load_task_pairs(hidden_ab.DEFAULT_TASK_DIR)
        hidden_ab.validate_pairs(pairs)

        for pair in pairs:
            for task_path in (pair.no_harness, pair.yes_harness):
                data = hidden_ab.read_json(task_path)
                expected_files = set(data["expected_files"])
                prompt = data["prompt"]

                self.assertIn("docs/**", expected_files)
                self.assertNotIn("README.md", expected_files)
                self.assertIn("documented docs location", prompt)
                self.assertIn("Do not update the root README", prompt)

    def test_balanced_hidden_flask_task_set_plans_exactly_twenty_runs(self) -> None:
        pairs = hidden_ab.load_task_pairs(BALANCED_TASK_DIR)
        hidden_ab.validate_pairs(pairs)
        schedule = hidden_ab.build_schedule(pairs, repeats=1, pair_order="alternate")

        self.assertEqual(len(pairs), 10)
        self.assertEqual(len(schedule), 20)
        for pair in pairs:
            for task_path in (pair.no_harness, pair.yes_harness):
                data = hidden_ab.read_json(task_path)
                self.assertNotEqual(data["repo"]["ref"], "HEAD")

    def test_balanced_hidden_flask_prompts_match_and_include_contracts(self) -> None:
        pairs = hidden_ab.load_task_pairs(BALANCED_TASK_DIR)
        hidden_ab.validate_pairs(pairs)

        for pair in pairs:
            no_harness = hidden_ab.read_json(pair.no_harness)
            yes_harness = hidden_ab.read_json(pair.yes_harness)
            prompt = no_harness["prompt"]

            self.assertEqual(
                prompt,
                yes_harness["prompt"],
                msg=f"{pair.task_id} balanced prompt differs between A/B targets",
            )
            for phrase in (
                "Endpoint and method:",
                "Success status:",
                "Top-level",
                "Core business rule:",
                "source of truth",
                "documented docs location",
                "Do not update the root README",
            ):
                self.assertIn(phrase, prompt, msg=f"{pair.task_id} missing {phrase!r}")

            if "POST " in prompt:
                for phrase in ("Request JSON schema:", "unknown_sku", "invalid_quantity"):
                    self.assertIn(phrase, prompt, msg=f"{pair.task_id} missing {phrase!r}")

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

    def test_rejects_ambiguous_docs_prompt_when_root_readme_is_outside_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp)
            write_hidden_task(
                task_dir / "alpha-no-harness.json",
                "alpha",
                "../flask-no-harness",
                prompt="Update the application, tests, and related project docs.",
            )
            write_hidden_task(
                task_dir / "alpha-yes-harness.json",
                "alpha",
                "../flask-yes-harness",
                prompt="Update the application, tests, and related project docs.",
            )

            pairs = hidden_ab.load_task_pairs(task_dir)
            with self.assertRaises(hidden_ab.BenchmarkPlanError):
                hidden_ab.validate_pairs(pairs)

    def test_execute_schedule_honors_jobs_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = Namespace(
                workspace=root / "runs",
                results=root / "results",
                model="fixture-model",
                reasoning_effort="medium",
                service_tier="",
                jobs=2,
                agent_command="fixture-agent",
                max_agent_timeout=60,
                max_cost_usd=1.0,
            )
            schedule = [
                hidden_ab.ScheduledRun(1, f"task-{index}", "A:no-harness", Path(f"task-{index}.json"))
                for index in range(4)
            ]
            lock = threading.Lock()
            active = 0
            max_active = 0

            def fake_run(command: list[str], **kwargs: object) -> hidden_ab.subprocess.CompletedProcess[str]:
                nonlocal active, max_active
                with lock:
                    active += 1
                    max_active = max(max_active, active)
                time.sleep(0.05)
                with lock:
                    active -= 1
                return hidden_ab.subprocess.CompletedProcess(command, 0, stdout="ok\n", stderr="")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                mock.patch.object(hidden_ab.subprocess, "run", side_effect=fake_run),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = hidden_ab.execute_schedule(args, schedule)

            self.assertEqual(exit_code, 0)
            self.assertEqual(max_active, 2)


def write_hidden_task(
    path: Path,
    task_id: str,
    repo_source: str,
    prompt: str | None = None,
) -> None:
    if prompt is None:
        prompt = (
            "Update the application, tests, and companion documentation in the "
            "repository's documented docs location. Do not update the root README "
            "unless the task explicitly asks for README changes."
        )
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "id": task_id,
                "description": "fixture hidden task",
                "repo": {"source": repo_source, "ref": "abc123"},
                "prompt": prompt,
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
