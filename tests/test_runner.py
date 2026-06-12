from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from harness_agent_benchmark_runner.models import RunnerConfig
from harness_agent_benchmark_runner.runner import (
    materialize_verification_command,
    run_task,
    run_task_with_retries,
    write_result,
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

    def test_runner_overrides_agent_timeout_before_cap(self) -> None:
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
                        "(repo / 'README.md').write_text(f'{timeout}\\n', encoding='utf-8')",
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
                        "name": "timeout override passed",
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('README.md').read_text() == '20\\n'",
                        ],
                    }
                ],
                extra_fields={"timeout_seconds": 10},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                    agent_timeout_override_seconds=20,
                    max_agent_timeout_seconds=30,
                ),
            )

            self.assertTrue(result["scoring"]["success"])
            self.assertEqual(result["limits"]["agent_timeout_seconds"], 20)
            self.assertEqual(result["limits"]["agent_process_timeout_seconds"], 20)
            self.assertEqual(result["limits"]["agent_timeout_override_seconds"], 20)
            self.assertEqual(result["limits"]["max_agent_timeout_seconds"], 30)

    def test_runner_caps_agent_timeout_override(self) -> None:
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
                        "(repo / 'README.md').write_text(f'{timeout}\\n', encoding='utf-8')",
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
                        "name": "timeout override capped",
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('README.md').read_text() == '15\\n'",
                        ],
                    }
                ],
                extra_fields={"timeout_seconds": 10},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                    agent_timeout_override_seconds=20,
                    max_agent_timeout_seconds=15,
                ),
            )

            self.assertTrue(result["scoring"]["success"])
            self.assertEqual(result["limits"]["agent_timeout_seconds"], 15)
            self.assertEqual(result["limits"]["agent_timeout_override_seconds"], 20)
            self.assertEqual(result["limits"]["max_agent_timeout_seconds"], 15)

    def test_runner_records_agent_stall_watchdog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "import time",
                        "time.sleep(10)",
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
                extra_fields={"timeout_seconds": 30},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                    agent_stall_timeout_seconds=1,
                ),
            )

            self.assertFalse(result["scoring"]["success"])
            self.assertTrue(result["scoring"]["agent_timed_out"])
            self.assertTrue(result["scoring"]["agent_stalled"])
            self.assertFalse(result["scoring"]["execution_success"])
            self.assertEqual(result["agent"]["termination_reason"], "stall_watchdog")
            self.assertEqual(result["limits"]["agent_timeout_seconds"], 30)
            self.assertEqual(result["limits"]["agent_process_timeout_seconds"], 1)
            self.assertEqual(result["limits"]["agent_stall_timeout_seconds"], 1)
            self.assertLess(result["agent"]["duration_seconds"], 5)
            self.assertTrue(any((root / "results").glob("*.jsonl")))

    def test_runner_records_agent_idle_watchdog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "import time",
                        "print('started', flush=True)",
                        "time.sleep(10)",
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
                extra_fields={"timeout_seconds": 30},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                    agent_idle_timeout_seconds=1,
                ),
            )

            self.assertFalse(result["scoring"]["success"])
            self.assertTrue(result["scoring"]["agent_timed_out"])
            self.assertTrue(result["scoring"]["agent_stalled"])
            self.assertEqual(result["agent"]["termination_reason"], "idle_watchdog")
            self.assertEqual(result["limits"]["agent_timeout_seconds"], 30)
            self.assertEqual(result["limits"]["agent_process_timeout_seconds"], 30)
            self.assertEqual(result["limits"]["agent_idle_timeout_seconds"], 1)
            self.assertLess(result["agent"]["duration_seconds"], 5)
            self.assertIn("started", result["agent"]["stdout_tail"])

    def test_agent_idle_watchdog_allows_active_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "import time",
                        "for index in range(4):",
                        "    print(f'tick {index}', flush=True)",
                        "    time.sleep(0.3)",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "(repo / 'README.md').write_text('active\\n', encoding='utf-8')",
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
                            "from pathlib import Path; assert Path('README.md').read_text() == 'active\\n'",
                        ],
                    }
                ],
                extra_fields={"timeout_seconds": 30},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                    agent_idle_timeout_seconds=1,
                ),
            )

            self.assertTrue(result["scoring"]["success"])
            self.assertFalse(result["scoring"]["agent_timed_out"])
            self.assertFalse(result["scoring"]["agent_stalled"])
            self.assertIsNone(result["agent"].get("termination_reason"))
            self.assertIn("tick 3", result["agent"]["stdout_tail"])

    def test_runner_records_agent_no_edit_watchdog_with_active_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "import time",
                        "for index in range(10):",
                        "    print(f'tick {index}', flush=True)",
                        "    time.sleep(0.3)",
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
                extra_fields={"timeout_seconds": 30},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                    agent_no_edit_timeout_seconds=1,
                ),
            )

            self.assertFalse(result["scoring"]["success"])
            self.assertTrue(result["scoring"]["agent_timed_out"])
            self.assertTrue(result["scoring"]["agent_stalled"])
            self.assertEqual(result["agent"]["termination_reason"], "no_edit_watchdog")
            self.assertEqual(result["limits"]["agent_timeout_seconds"], 30)
            self.assertEqual(result["limits"]["agent_process_timeout_seconds"], 30)
            self.assertEqual(result["limits"]["agent_no_edit_timeout_seconds"], 1)
            self.assertLess(result["agent"]["duration_seconds"], 5)
            self.assertIn("tick", result["agent"]["stdout_tail"])

    def test_agent_no_edit_watchdog_allows_observed_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "import time",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "(repo / 'README.md').write_text('changed\\n', encoding='utf-8')",
                        "print('changed', flush=True)",
                        "time.sleep(1.5)",
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
                        "name": "readme changed",
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('README.md').read_text() == 'changed\\n'",
                        ],
                    }
                ],
                extra_fields={"timeout_seconds": 30},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                    agent_no_edit_timeout_seconds=1,
                ),
            )

            self.assertTrue(result["scoring"]["success"])
            self.assertFalse(result["scoring"]["agent_timed_out"])
            self.assertFalse(result["scoring"]["agent_stalled"])
            self.assertIsNone(result["agent"].get("termination_reason"))
            self.assertEqual(result["git"]["changed_files"], ["README.md"])

    def test_runner_records_dimension_scoring_and_benchmark_metadata(self) -> None:
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
                        "(repo / 'README.md').write_text('updated\\n', encoding='utf-8')",
                        "sys.exit(1)",
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
                        "name": "hidden behavior",
                        "dimensions": ["functional", "schema"],
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('README.md').read_text() == 'updated\\n'",
                        ],
                    }
                ],
                extra_fields={
                    "benchmark": {
                        "suite": "fixture-suite",
                        "split": "heldout",
                        "prompt_variant": "partial-realistic",
                        "target_arm": "memory-harness",
                    }
                },
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
            self.assertFalse(result["scoring"]["strict_success"])
            self.assertTrue(result["scoring"]["functional_success"])
            self.assertTrue(result["scoring"]["schema_contract_success"])
            self.assertFalse(result["scoring"]["workflow_success"])
            self.assertEqual(result["verification"][0]["dimensions"], ["functional", "schema"])
            self.assertEqual(result["task"]["benchmark"]["target_arm"], "memory-harness")

    def test_runner_leakage_audit_blocks_agent_before_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            (source_repo / "docs").mkdir()
            (source_repo / "docs" / "memory.md").write_text(
                "The hidden oracle expects catalog-metrics-v1.\n",
                encoding="utf-8",
            )
            run(["git", "add", "docs/memory.md"], cwd=source_repo)
            run(["git", "commit", "-m", "Add docs memory"], cwd=source_repo)
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "(repo / 'README.md').write_text('should not run\\n', encoding='utf-8')",
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
                extra_fields={
                    "leakage_audit": {
                        "forbidden_text": ["catalog-metrics-v1"],
                        "forbidden_paths": ["runs/**"],
                    }
                },
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
            self.assertFalse(result["scoring"]["preflight_passed"])
            self.assertNotIn("agent", result)
            self.assertEqual(result["preflight"]["findings"][0]["type"], "forbidden_text")
            self.assertEqual(result["preflight"]["findings"][0]["path"], "docs/memory.md")

    def test_runner_hides_agent_excluded_paths_until_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            (source_repo / "benchmarks" / "oracles").mkdir(parents=True)
            (source_repo / "benchmarks" / "oracles" / "secret.txt").write_text(
                "hidden answer\n",
                encoding="utf-8",
            )
            run(["git", "add", "benchmarks/oracles/secret.txt"], cwd=source_repo)
            run(["git", "commit", "-m", "Add benchmark oracle"], cwd=source_repo)
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "import subprocess",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "visible = (repo / 'benchmarks').exists()",
                        "parent_leak = any('_agent_excluded' in str(path) for path in repo.parent.rglob('*'))",
                        "show = subprocess.run(",
                        "    ['git', 'show', 'HEAD:benchmarks/oracles/secret.txt'],",
                        "    cwd=repo,",
                        "    stdout=subprocess.PIPE,",
                        "    stderr=subprocess.PIPE,",
                        ")",
                        "leaked = show.returncode == 0",
                        "(repo / 'README.md').write_text(",
                        "    f'benchmarks visible: {visible}; git leaked: {leaked}; parent leaked: {parent_leak}\\n',",
                        "    encoding='utf-8',",
                        ")",
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
                        "name": "excluded path restored",
                        "command": [
                            sys.executable,
                            "-c",
                            (
                                "from pathlib import Path; "
                                "assert Path('README.md').read_text() == "
                                "'benchmarks visible: False; git leaked: False; parent leaked: False\\n'; "
                                "assert Path('benchmarks/oracles/secret.txt').read_text() == 'hidden answer\\n'"
                            ),
                        ],
                    }
                ],
                extra_fields={"agent_excluded_paths": ["benchmarks"]},
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                ),
            )

            self.assertTrue(result["scoring"]["success"])
            self.assertEqual(result["git"]["changed_files"], ["README.md"])
            self.assertEqual(result["git"]["agent_excluded_path_conflicts"], [])
            self.assertEqual(result["task"]["agent_excluded_paths"], ["benchmarks"])

    def test_runner_runs_agent_setup_and_prepends_venv_bin_to_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            (source_repo / ".gitignore").write_text(".venv/\n", encoding="utf-8")
            run(["git", "add", ".gitignore"], cwd=source_repo)
            run(["git", "commit", "-m", "Ignore virtualenv"], cwd=source_repo)
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "import shutil",
                        "import subprocess",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "sentinel = shutil.which('sentinel')",
                        "assert sentinel is not None",
                        "subprocess.run(['sentinel'], cwd=repo, check=True)",
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
                        "name": "setup path used",
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('README.md').read_text() == 'setup path used\\n'",
                        ],
                    }
                ],
                extra_fields={
                    "agent_setup": {
                        "commands": [
                            {
                                "name": "create sentinel in venv bin",
                                "command": [
                                    sys.executable,
                                    "-c",
                                    (
                                        "from pathlib import Path; "
                                        "p=Path('.venv/bin'); p.mkdir(parents=True); "
                                        "s=p/'sentinel'; "
                                        "s.write_text('#!/bin/sh\\necho \"setup path used\" > README.md\\n'); "
                                        "s.chmod(0o755)"
                                    ),
                                ],
                            }
                        ]
                    }
                },
            )

            result = run_task(
                load_task(task_path),
                RunnerConfig(
                    agent_command=f"{sys.executable} {agent}",
                    workspace_root=root / "runs",
                    results_dir=root / "results",
                ),
            )

            self.assertTrue(result["scoring"]["success"])
            self.assertEqual(result["agent_setup"][0]["label"], "create sentinel in venv bin")
            self.assertEqual(result["agent_setup"][0]["exit_code"], 0)
            self.assertEqual(result["git"]["changed_files"], ["README.md"])

    def test_runner_scores_agent_excluded_path_conflict_as_boundary_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_repo = create_git_repo(root / "source")
            (source_repo / "benchmarks").mkdir()
            (source_repo / "benchmarks" / "oracle.txt").write_text("original\n", encoding="utf-8")
            run(["git", "add", "benchmarks/oracle.txt"], cwd=source_repo)
            run(["git", "commit", "-m", "Add benchmark oracle"], cwd=source_repo)
            agent = root / "agent.py"
            agent.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "repo = Path(os.environ['BENCHMARK_REPO'])",
                        "(repo / 'README.md').write_text('updated\\n', encoding='utf-8')",
                        "(repo / 'benchmarks').mkdir()",
                        "(repo / 'benchmarks' / 'oracle.txt').write_text('agent-created\\n', encoding='utf-8')",
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
                        "name": "original restored",
                        "command": [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; assert Path('benchmarks/oracle.txt').read_text() == 'original\\n'",
                        ],
                    }
                ],
                extra_fields={
                    "agent_excluded_paths": ["benchmarks"],
                    "forbidden_files": ["benchmarks/**"],
                },
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
            self.assertEqual(result["git"]["changed_files"], ["README.md"])
            self.assertEqual(
                result["git"]["agent_excluded_path_conflicts"][0]["path"],
                "benchmarks",
            )
            self.assertEqual(result["scoring"]["forbidden_files"], ["benchmarks"])

    def test_summary_counts_results(self) -> None:
        records = [
            {
                "task": {"id": "task-a"},
                "scoring": {
                    "success": True,
                    "verification_passed": True,
                    "first_pass_verification": True,
                    "agent_timed_out": False,
                    "agent_stalled": False,
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
                    "agent_stalled": True,
                    "wrong_file_edits": 1,
                    "forbidden_file_edits": 0,
                },
            },
        ]

        summary = summarize_results(records)

        self.assertEqual(summary["total"]["runs"], 2)
        self.assertEqual(summary["total"]["successes"], 1)
        self.assertEqual(summary["total"]["strict_successes"], 1)
        self.assertEqual(summary["total"]["wrong_file_edits"], 1)
        self.assertEqual(summary["total"]["first_pass_verification"], 1)
        self.assertEqual(summary["total"]["agent_timeouts"], 1)
        self.assertEqual(summary["total"]["agent_stalls"], 1)
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

    def test_write_result_supports_concurrent_jsonl_appends(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            results_dir = root / "results"
            records = [
                {
                    "schema_version": 1,
                    "run_id": f"run-{index}",
                    "task": {"id": "fixture-task"},
                    "scoring": {"success": True},
                }
                for index in range(20)
            ]

            def write(index: int) -> None:
                run_dir = root / f"run-{index}"
                run_dir.mkdir()
                write_result(records[index], results_dir, run_dir)

            with ThreadPoolExecutor(max_workers=4) as executor:
                list(executor.map(write, range(len(records))))

            jsonl_files = sorted(results_dir.glob("*.jsonl"))
            self.assertEqual(len(jsonl_files), 1)
            lines = jsonl_files[0].read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), len(records))
            self.assertEqual(
                {json.loads(line)["run_id"] for line in lines},
                {record["run_id"] for record in records},
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
