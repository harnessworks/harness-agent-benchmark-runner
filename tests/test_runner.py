from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from harness_agent_benchmark_runner.models import RunnerConfig
from harness_agent_benchmark_runner.runner import (
    materialize_verification_command,
    run_task,
    run_task_with_retries,
)
from harness_agent_benchmark_runner.summary import summarize_results
from harness_agent_benchmark_runner.tasks import load_task


class RunnerTests(unittest.TestCase):
    def test_runner_records_successful_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "(repo / 'README.md').write_text('updated\\n', encoding='utf-8')",
                    ]
                ),
                encoding="utf-8",
            )
            task_path = write_task(
                root,
                source_repo,
                expected_files=["README.md"],
                verification_commands=[
                    {
                        "name": "readme updated",
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('README.md').read_text() == 'updated\\n'",
                        ],
                    }
                ],
            )

            task = load_task(task_path)
            result = run_task(
                task,
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                ),
            )

            self.assertTrue(result["scoring"]["success"])
            self.assertEqual(result["git"]["changed_files"], ["README.md"])
            self.assertEqual(result["scoring"]["wrong_file_edits"], 0)
            self.assertTrue(any((root / "results").glob("*.jsonl")))
            self.assertEqual(result["attempt"], {"number": 1, "limit": 1})

    def test_runner_flags_wrong_file_edit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "(repo / 'unexpected.txt').write_text('bad\\n', encoding='utf-8')",
                    ]
                ),
                encoding="utf-8",
            )
            task_path = write_task(
                root,
                source_repo,
                expected_files=["README.md"],
                verification_commands=[
                    {"name": "always passes", "command": [sys.executable, "-c", "pass"]}
                ],
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                ),
            )

            self.assertFalse(result["scoring"]["success"])
            self.assertEqual(result["scoring"]["wrong_file_edits"], 1)
            self.assertEqual(result["scoring"]["wrong_files"], ["unexpected.txt"])

    def test_runner_retries_until_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "import sys",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "attempt = int(os.environ['BENCHMARK_ATTEMPT_NUMBER'])",
                        "if attempt == 1:",
                        "    sys.exit(1)",
                        "(repo / 'README.md').write_text('updated\\n', encoding='utf-8')",
                    ]
                ),
                encoding="utf-8",
            )
            task_path = write_task(
                root,
                source_repo,
                expected_files=["README.md"],
                verification_commands=[
                    {
                        "name": "readme updated",
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('README.md').read_text() == 'updated\\n'",
                        ],
                    }
                ],
                extra_fields={"max_attempts": 2},
            )

            results = run_task_with_retries(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                ),
            )

            self.assertEqual(len(results), 2)
            self.assertFalse(results[0]["scoring"]["success"])
            self.assertEqual(results[0]["attempt"], {"number": 1, "limit": 2})
            self.assertTrue(results[1]["scoring"]["success"])
            self.assertEqual(results[1]["attempt"], {"number": 2, "limit": 2})
            self.assertFalse(results[1]["scoring"]["first_pass_verification"])

    def test_runner_caps_agent_timeout_and_passes_budget_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "timeout = os.environ['BENCHMARK_TIMEOUT_SECONDS']",
                        "budget = os.environ['BENCHMARK_MAX_COST_USD']",
                        "(repo / 'README.md').write_text(f'{timeout}\\n{budget}\\n', encoding='utf-8')",
                    ]
                ),
                encoding="utf-8",
            )
            task_path = write_task(
                root,
                source_repo,
                expected_files=["README.md"],
                verification_commands=[
                    {
                        "name": "limits passed",
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('README.md').read_text() == '3\\n1.25\\n'",
                        ],
                    }
                ],
                extra_fields={"timeout_seconds": 10, "max_cost_usd": 9},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                    max_agent_timeout_seconds=3,
                    max_cost_usd_override=1.25,
                ),
            )

            self.assertTrue(result["scoring"]["success"])
            self.assertEqual(result["limits"]["agent_timeout_seconds"], 3)
            self.assertEqual(result["limits"]["max_cost_usd"], 1.25)

    def test_summary_counts_results(self) -> None:
        records = [
            {
                "task": {"id": "task-a"},
                "scoring": {
                    "success": True,
                    "verification_passed": True,
                    "first_pass_verification": True,
                    "agent_timed_out": False,
                    "wrong_file_edits": 0,
                    "forbidden_file_edits": 0,
                },
            },
            {
                "task": {"id": "task-a"},
                "scoring": {
                    "success": False,
                    "verification_passed": True,
                    "first_pass_verification": False,
                    "agent_timed_out": True,
                    "wrong_file_edits": 1,
                    "forbidden_file_edits": 0,
                },
            },
        ]

        summary = summarize_results(records)

        self.assertEqual(summary["total"]["runs"], 2)
        self.assertEqual(summary["total"]["successes"], 1)
        self.assertEqual(summary["total"]["wrong_file_edits"], 1)
        self.assertEqual(summary["total"]["first_pass_verification"], 1)
        self.assertEqual(summary["total"]["agent_timeouts"], 1)
        self.assertEqual(summary["by_task"]["task-a"]["runs"], 2)

    def test_materialize_verification_command_replaces_task_placeholders(self) -> None:
        task_path = Path("/tmp/benchmarks/tasks/fixture.json")

        self.assertEqual(
            materialize_verification_command(
                ["bash", "{task_dir}/../oracles/check.sh", "{task_file}"],
                task_path,
            ),
            [
                "bash",
                "/tmp/benchmarks/tasks/../oracles/check.sh",
                "/tmp/benchmarks/tasks/fixture.json",
            ],
        )
        self.assertEqual(
            materialize_verification_command("python {task_dir}/check.py", task_path),
            "python /tmp/benchmarks/tasks/check.py",
        )


def create_git_repo(path: Path) -> Path:
    path.mkdir(parents=True)
    (path / "README.md").write_text("initial\n", encoding="utf-8")
    run(["git", "init", "-b", "main"], cwd=path)
    run(["git", "config", "user.email", "benchmark@example.com"], cwd=path)
    run(["git", "config", "user.name", "Benchmark Test"], cwd=path)
    run(["git", "add", "README.md"], cwd=path)
    run(["git", "commit", "-m", "Initial commit"], cwd=path)
    return path


def write_task(
    root: Path,
    source_repo: Path,
    *,
    expected_files: list[str],
    verification_commands: list[dict[str, object]],
    extra_fields: dict[str, object] | None = None,
) -> Path:
    task_path = root / "task.json"
    data: dict[str, object] = {
        "schema_version": 1,
        "id": "fixture-task",
        "description": "Fixture benchmark task.",
        "repo": {"source": str(source_repo), "ref": "HEAD"},
        "prompt": "Run fixture task.",
        "expected_files": expected_files,
        "forbidden_files": [".env", "secrets/**"],
        "verification": {"commands": verification_commands},
    }
    if extra_fields:
        data.update(extra_fields)
    task_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )
    return task_path


def run(command: list[str], *, cwd: Path) -> None:
    subprocess.run(command, cwd=str(cwd), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
    unittest.main()
