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
        self.assertFalse(flask_hidden_oracle.is_money_key("price_band_counts"))
        self.assertFalse(flask_hidden_oracle.is_money_key("counts_by_price_band"))
        self.assertFalse(flask_hidden_oracle.is_money_key("price_tier"))
        self.assertFalse(flask_hidden_oracle.is_money_key("price_tiers"))
        self.assertTrue(flask_hidden_oracle.is_money_key("unit_price"))
        self.assertTrue(flask_hidden_oracle.is_money_key("total_amount"))

    def test_catalog_price_policy_summary_accepts_nested_price_band_counts(self) -> None:
        counts = flask_hidden_oracle.catalog_price_band_counts(
            {
                "price_bands": {
                    "budget": 1,
                    "standard": 1,
                    "premium": 1,
                }
            }
        )

        self.assertEqual(counts, {"budget": 1, "standard": 1, "premium": 1})

    def test_catalog_price_policy_summary_requires_all_price_band_counts(self) -> None:
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                flask_hidden_oracle.catalog_price_band_counts(
                    {
                        "price_bands": {
                            "budget": 1,
                            "standard": 2,
                        }
                    }
                )

    def test_cart_functional_summary_prefers_summary_object_over_item_rows(self) -> None:
        class Response:
            def __init__(self, status_code: int, payload: dict[str, object]) -> None:
                self.status_code = status_code
                self._payload = payload

            def get_json(self, silent: bool = True) -> dict[str, object]:
                return self._payload

            def get_data(self, as_text: bool = True) -> str:
                return str(self._payload)

        class Client:
            def post(self, path: str, json: dict[str, object]) -> Response:
                items = json.get("items")
                if items == [{"sku": "missing", "quantity": 1}]:
                    return Response(400, {"error": "unknown_sku"})
                if items == [{"sku": "desk-lamp", "quantity": 0}]:
                    return Response(400, {"error": "invalid_quantity"})
                return Response(
                    200,
                    {
                        "items": [
                            {
                                "sku": "desk-lamp",
                                "status": "accepted",
                                "requested_quantity": 2,
                                "accepted_quantity": 2,
                                "rejected_quantity": 0,
                            },
                            {
                                "sku": "standing-mat",
                                "status": "limited",
                                "requested_quantity": 5,
                                "accepted_quantity": 3,
                                "rejected_quantity": 2,
                            },
                        ],
                        "summary": {"requested": 7, "accepted": 5, "rejected": 2},
                    },
                )

            def get(self, path: str) -> Response:
                return Response(
                    200,
                    {
                        "products": [
                            {"sku": "desk-lamp", "stock": 12},
                            {"sku": "notebook", "stock": 48},
                            {"sku": "standing-mat", "stock": 3},
                        ]
                    },
                )

        original_client = flask_hidden_oracle.client
        flask_hidden_oracle.client = lambda: Client()
        try:
            flask_hidden_oracle.check_cart_validation_functional()
        finally:
            flask_hidden_oracle.client = original_client


if __name__ == "__main__":
    unittest.main()
