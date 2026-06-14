from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch


def load_example_agent(name: str) -> ModuleType:
    root = Path(__file__).resolve().parents[1]
    path = root / "examples" / "agents" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load example agent: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


claude_code_agent = load_example_agent("claude_code_agent")
codex_exec_agent = load_example_agent("codex_exec_agent")


class ClaudeCodeAgentTests(unittest.TestCase):
    def test_build_command_forwards_limits_and_defaults(self) -> None:
        env = {
            "CLAUDE_BIN": "custom-claude",
            "CLAUDE_MODEL": "opus",
            "CLAUDE_PERMISSION_MODE": "acceptEdits",
            "CLAUDE_MAX_TURNS": "4",
            "CLAUDE_EXTRA_ARGS": "--output-format json",
            "CLAUDE_PROMPT_ARG": "Do the benchmark task.",
            "BENCHMARK_MAX_COST_USD": "2.5",
        }

        with patch.dict(os.environ, env, clear=True):
            command = claude_code_agent.build_command()

        self.assertEqual(
            command,
            [
                "custom-claude",
                "-p",
                "--permission-mode",
                "acceptEdits",
                "--model",
                "opus",
                "--max-budget-usd",
                "2.5",
                "--max-turns",
                "4",
                "--no-session-persistence",
                "--output-format",
                "json",
                "Do the benchmark task.",
            ],
        )

    def test_build_command_can_disable_session_persistence_flag(self) -> None:
        with patch.dict(os.environ, {"CLAUDE_NO_SESSION_PERSISTENCE": "0"}, clear=True):
            command = claude_code_agent.build_command()

        self.assertNotIn("--no-session-persistence", command)
        self.assertEqual(command[-1], claude_code_agent.DEFAULT_PROMPT_ARG)

    def test_build_command_rejects_invalid_extra_args(self) -> None:
        with patch.dict(os.environ, {"CLAUDE_EXTRA_ARGS": "'unterminated"}, clear=True):
            with self.assertRaisesRegex(ValueError, "invalid CLAUDE_EXTRA_ARGS"):
                claude_code_agent.build_command()


class CodexExecAgentTests(unittest.TestCase):
    def test_build_command_isolates_user_config_by_default(self) -> None:
        env = {
            "CODEX_BIN": "custom-codex",
            "CODEX_APPROVAL_POLICY": "never",
            "CODEX_SANDBOX": "workspace-write",
            "CODEX_MODEL": "gpt-test",
            "CODEX_EXEC_ARGS": "-c model_reasoning_effort=medium",
        }

        with patch.dict(os.environ, env, clear=True):
            command = codex_exec_agent.build_command(Path("/tmp/repo"))

        self.assertEqual(
            command,
            [
                "custom-codex",
                "--ask-for-approval",
                "never",
                "--sandbox",
                "workspace-write",
                "--model",
                "gpt-test",
                "exec",
                "--cd",
                "/tmp/repo",
                "--skip-git-repo-check",
                "--ephemeral",
                "--ignore-user-config",
                "-c",
                "model_reasoning_effort=medium",
                "--ignore-rules",
                "--disable",
                "plugins",
                "-",
            ],
        )

    def test_build_command_can_disable_user_config_isolation(self) -> None:
        with patch.dict(os.environ, {"CODEX_IGNORE_USER_CONFIG": "0"}, clear=True):
            command = codex_exec_agent.build_command(Path("/tmp/repo"))

        self.assertNotIn("--ignore-user-config", command)

    def test_build_command_keeps_profile_without_default_user_config_isolation(self) -> None:
        with patch.dict(os.environ, {"CODEX_PROFILE": "bench"}, clear=True):
            command = codex_exec_agent.build_command(Path("/tmp/repo"))

        self.assertIn("--profile", command)
        self.assertNotIn("--ignore-user-config", command)
        self.assertIn("--ignore-rules", command)
        self.assertIn("--disable", command)
        self.assertIn("plugins", command)

    def test_build_command_can_disable_rules_isolation(self) -> None:
        with patch.dict(os.environ, {"CODEX_IGNORE_RULES": "0"}, clear=True):
            command = codex_exec_agent.build_command(Path("/tmp/repo"))

        self.assertNotIn("--ignore-rules", command)
        self.assertIn("--disable", command)
        self.assertIn("plugins", command)

    def test_build_command_can_disable_plugin_isolation(self) -> None:
        with patch.dict(os.environ, {"CODEX_DISABLE_PLUGINS": "0"}, clear=True):
            command = codex_exec_agent.build_command(Path("/tmp/repo"))

        self.assertIn("--ignore-rules", command)
        self.assertNotIn("--disable", command)
        self.assertNotIn("plugins", command)

    def test_build_command_rejects_invalid_extra_args(self) -> None:
        with patch.dict(os.environ, {"CODEX_EXEC_ARGS": "'unterminated"}, clear=True):
            with self.assertRaisesRegex(ValueError, "invalid CODEX_EXEC_ARGS"):
                codex_exec_agent.build_command(Path("/tmp/repo"))

    def test_build_prompt_leaves_task_prompt_unchanged_by_default(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            prompt = codex_exec_agent.build_prompt("Do the task.")

        self.assertEqual(prompt, "Do the task.\n")

    def test_build_prompt_can_enable_guard_and_append_suffix(self) -> None:
        env = {
            "CODEX_PROMPT_GUARD": "1",
            "CODEX_PROMPT_SUFFIX": "Return when done.",
        }

        with patch.dict(os.environ, env, clear=True):
            prompt = codex_exec_agent.build_prompt("Do the task.")

        self.assertIn("isolated repository clone", prompt)
        self.assertIn("Do not inspect benchmark task specs", prompt)
        self.assertIn("do not stop after narrating a plan", prompt)
        self.assertIn("make the first small scoped app/test/docs edit", prompt)
        self.assertTrue(prompt.endswith("Do the task.\n\nReturn when done.\n"))


if __name__ == "__main__":
    unittest.main()
