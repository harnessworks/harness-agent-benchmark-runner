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


if __name__ == "__main__":
    unittest.main()
