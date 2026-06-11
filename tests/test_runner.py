from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from harness_agent_benchmark_runner.models import RunnerConfig
from harness_agent_benchmark_runner.runner import run_task
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

    def test_summary_counts_results(self) -> None:
        records = [
            {
                "task": {"id": "task-a"},
                "scoring": {
                    "success": True,
                    "verification_passed": True,
                    "wrong_file_edits": 0,
                    "forbidden_file_edits": 0,
                },
            },
            {
                "task": {"id": "task-a"},
                "scoring": {
                    "success": False,
                    "verification_passed": True,
                    "wrong_file_edits": 1,
                    "forbidden_file_edits": 0,
                },
            },
        ]

        summary = summarize_results(records)

        self.assertEqual(summary["total"]["runs"], 2)
        self.assertEqual(summary["total"]["successes"], 1)
        self.assertEqual(summary["total"]["wrong_file_edits"], 1)
        self.assertEqual(summary["by_task"]["task-a"]["runs"], 2)


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
) -> Path:
    task_path = root / "task.json"
    task_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "id": "fixture-task",
                "description": "Fixture benchmark task.",
                "repo": {"source": str(source_repo), "ref": "HEAD"},
                "prompt": "Run fixture task.",
                "expected_files": expected_files,
                "forbidden_files": [".env", "secrets/**"],
                "verification": {"commands": verification_commands},
            }
        ),
        encoding="utf-8",
    )
    return task_path


def run(command: list[str], *, cwd: Path) -> None:
    subprocess.run(command, cwd=str(cwd), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
    unittest.main()
