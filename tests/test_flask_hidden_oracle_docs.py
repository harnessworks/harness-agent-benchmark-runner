from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path


ORACLE_PATH = Path(__file__).resolve().parents[1] / "benchmarks" / "oracles" / "flask_hidden_oracle.py"
SPEC = importlib.util.spec_from_file_location("flask_hidden_oracle", ORACLE_PATH)
assert SPEC is not None
flask_hidden_oracle = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["flask_hidden_oracle"] = flask_hidden_oracle
SPEC.loader.exec_module(flask_hidden_oracle)


class FlaskHiddenOracleDocsTests(unittest.TestCase):
    def test_glossary_docs_are_checked_by_concepts_not_exact_endpoint_phrase(self) -> None:
        glossary = flask_hidden_oracle.normalize_doc_text(
            """
            # Domain Glossary

            ## Availability Badge

            The availability badge is exposed by
            `GET /products/<sku>/availability` for known catalog SKUs.

            - `in_stock`: the product has stock of 10 or more.
            - `low_stock`: the product has stock greater than 0 and less than 10.
            """
        )

        self.assertNotIn("availability badge endpoint", glossary)
        flask_hidden_oracle.expect_terms(
            glossary,
            ("/products/<sku>/availability", "in_stock", "low_stock"),
            "glossary must document availability route and badges",
        )

    def test_generic_product_route_does_not_satisfy_availability_docs(self) -> None:
        glossary = flask_hidden_oracle.normalize_doc_text(
            """
            # Domain Glossary

            The `/products` route exposes product availability details.

            - `in_stock`
            - `low_stock`
            """
        )

        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                flask_hidden_oracle.expect_terms(
                    glossary,
                    ("/products/<sku>/availability", "in_stock", "low_stock"),
                    "glossary must document availability route and badges",
                )

    def test_glossary_docs_still_fail_when_route_concept_is_missing(self) -> None:
        glossary = flask_hidden_oracle.normalize_doc_text(
            """
            # Domain Glossary

            ## Stock Risk

            Risk bands are `critical`, `watch`, and `healthy`.
            """
        )

        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                flask_hidden_oracle.expect_terms(
                    glossary,
                    ("/inventory/risk-report", "critical", "watch", "healthy"),
                    "glossary must document stock risk route and bands",
                )

    def test_schema_money_key_detection_allows_band_labels(self) -> None:
        self.assertFalse(flask_hidden_oracle.is_money_key("price_band"))
        self.assertFalse(flask_hidden_oracle.is_money_key("price_bands"))
        self.assertTrue(flask_hidden_oracle.is_money_key("unit_price"))
        self.assertTrue(flask_hidden_oracle.is_money_key("total_amount"))


if __name__ == "__main__":
    unittest.main()
