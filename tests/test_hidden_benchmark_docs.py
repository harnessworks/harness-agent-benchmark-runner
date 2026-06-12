from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPRESENTATIVE_DOCS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "benchmarks" / "latest.md",
    REPO_ROOT
    / "docs"
    / "benchmarks"
    / "2026-06-11-hidden-oracle-harness-effect-ab-3x.md",
]


class HiddenBenchmarkDocsTests(unittest.TestCase):
    def test_partial_large_run_is_not_promoted_to_representative_docs(self) -> None:
        forbidden_markers = [
            "hidden-flask-ab-large-20260612T001733Z",
            "results/hidden-flask-ab-large-20260612T001733Z/2026-06-12.jsonl",
        ]

        for path in REPRESENTATIVE_DOCS:
            text = path.read_text(encoding="utf-8")
            for marker in forbidden_markers:
                self.assertNotIn(marker, text, msg=f"{marker} leaked into {path}")

    def test_readme_separates_strict_success_from_verification_and_boundary(self) -> None:
        text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        normalized = " ".join(text.split())

        self.assertIn("Run-time strict successes", text)
        self.assertIn("Current concept-docs rescore", text)
        self.assertIn("Verification passed", text)
        self.assertIn("strict boundary miss", text)
        self.assertIn("not a functional failure by itself", normalized)


if __name__ == "__main__":
    unittest.main()
