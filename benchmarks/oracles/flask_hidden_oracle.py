#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")
MONEY_KEY_TERMS = ("amount", "cost", "discount", "price", "subtotal", "tax", "total", "value")


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        fail("usage: flask_hidden_oracle.py <task-id> [strict|functional|schema]")

    mode = argv[2] if len(argv) == 3 else "strict"
    checks_by_mode = {
        "strict": strict_checks(),
        "functional": functional_checks(),
        "schema": schema_checks(),
    }
    if mode not in checks_by_mode:
        fail(f"unknown hidden oracle mode: {mode}")

    checks = checks_by_mode[mode]
    task_id = argv[1]
    if task_id not in checks:
        fail(f"unknown hidden task id for {mode} oracle: {task_id}")

    checks[task_id]()
    print(f"{task_id}: hidden {mode} oracle passed")
    return 0


def strict_checks() -> dict[str, Any]:
    return {
        "hidden-effect-availability-badge": check_availability_badge,
        "hidden-effect-stock-risk": check_stock_risk,
        "hidden-effect-supplier-readiness": check_supplier_readiness,
        "hidden-effect-bundle-quote": check_bundle_quote,
        "hidden-effect-cart-validation": check_cart_validation,
        "hidden-effect-catalog-metrics": check_catalog_metrics,
        "hidden-effect-catalog-segments": check_catalog_segments,
        "hidden-effect-pick-list": check_pick_list,
        "hidden-effect-reservation-preview": check_reservation_preview,
        "hidden-effect-tax-preview": check_tax_preview,
    }


def functional_checks() -> dict[str, Any]:
    return {
        "hidden-effect-availability-badge": check_availability_badge_functional,
        "hidden-effect-bundle-quote": check_bundle_quote_functional,
        "hidden-effect-cart-validation": check_cart_validation_functional,
        "hidden-effect-catalog-metrics": check_catalog_metrics_functional,
        "hidden-effect-catalog-segments": check_catalog_segments_functional,
    }


def schema_checks() -> dict[str, Any]:
    return {
        "hidden-effect-availability-badge": lambda: check_get_schema_style(
            "/products/standing-mat/availability",
            "availability badge",
        ),
        "hidden-effect-bundle-quote": check_bundle_quote_schema,
        "hidden-effect-cart-validation": check_cart_validation_schema,
        "hidden-effect-catalog-metrics": lambda: check_get_schema_style(
            "/catalog/metrics",
            "catalog metrics",
        ),
        "hidden-effect-catalog-segments": lambda: check_get_schema_style(
            "/catalog/segments",
            "catalog segments",
        ),
    }


def client():
    from app import create_app

    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def check_availability_badge() -> None:
    response = client().get("/products/standing-mat/availability")
    assert_status(response, 200)
    payload = json_payload(response)
    product = payload.get("product")
    availability = payload.get("availability")
    meta = payload.get("meta")

    expect(product == {"sku": "standing-mat", "stock": 3}, "availability product summary is wrong")
    expect(isinstance(availability, dict), "availability badge must include availability object")
    expect(availability.get("badge") == "low_stock", "standing-mat availability badge is wrong")
    expect(availability.get("orderable") is True, "standing-mat must be orderable")
    expect(availability.get("restock_recommended") is True, "standing-mat must recommend restock")
    expect("low stock" in str(availability.get("message", "")).lower(), "availability message must mention low stock")
    expect(isinstance(meta, dict), "availability badge must include meta object")
    expect(meta.get("service") == "flask-no-harness", "availability meta.service is wrong")
    expect(meta.get("source") == "catalog", "availability meta.source must be catalog")

    in_stock = json_payload(client().get("/products/desk-lamp/availability"))
    expect(in_stock.get("availability", {}).get("badge") == "in_stock", "desk-lamp badge must be in_stock")
    expect(in_stock.get("availability", {}).get("restock_recommended") is False, "desk-lamp must not recommend restock")

    missing = client().get("/products/missing/availability")
    assert_status(missing, 404)
    missing_payload = json_payload(missing)
    expect(missing_payload.get("error") == "product_not_found", "missing availability SKU must return product_not_found")
    expect(missing_payload.get("sku") == "missing", "missing availability response must echo sku")

    glossary = glossary_text()
    expect_terms(
        glossary,
        ("/products/<sku>/availability", "in_stock", "low_stock"),
        "glossary must document availability route and badges",
    )


def check_stock_risk() -> None:
    response = client().get("/inventory/risk-report")
    assert_status(response, 200)
    payload = json_payload(response)
    risks = payload.get("risks")
    summary = payload.get("summary")
    meta = payload.get("meta")

    expect(isinstance(risks, list), "stock risk report must return risks list")
    expect(
        [
            (item.get("sku"), item.get("status"), item.get("action"), item.get("stock"))
            for item in risks
        ]
        == [
            ("standing-mat", "critical", "reorder_now", 3),
            ("desk-lamp", "watch", "monitor", 12),
            ("notebook", "healthy", "none", 48),
        ],
        "stock risk classification is wrong",
    )
    expect(summary == {"critical": 1, "watch": 1, "healthy": 1}, "stock risk summary is wrong")
    expect(isinstance(meta, dict), "stock risk report must include meta object")
    expect(meta.get("source") == "catalog", "stock risk meta.source must be catalog")
    expect(meta.get("service") == "flask-no-harness", "stock risk meta.service is wrong")
    expect(meta.get("rules") == "stock-risk-v1", "stock risk meta.rules is wrong")

    glossary = glossary_text()
    expect_terms(
        glossary,
        ("/inventory/risk-report", "critical", "watch", "healthy"),
        "glossary must document stock risk route and bands",
    )


def check_supplier_readiness() -> None:
    response = client().get("/suppliers/readiness")
    assert_status(response, 200)
    payload = json_payload(response)
    suppliers = payload.get("suppliers")
    summary = payload.get("summary")
    meta = payload.get("meta")

    expect(isinstance(suppliers, list), "supplier readiness must return suppliers list")
    expect(
        [
            (
                item.get("sku"),
                item.get("supplier"),
                item.get("lead_time_days"),
                item.get("status"),
            )
            for item in suppliers
        ]
        == [
            ("desk-lamp", "bright-co", 6, "ready"),
            ("notebook", "paperhouse", 2, "ready"),
            ("standing-mat", "ergo-supply", 9, "at_risk"),
        ],
        "supplier readiness rows are wrong",
    )
    expect(summary == {"ready": 2, "at_risk": 1}, "supplier readiness summary is wrong")
    expect(isinstance(meta, dict), "supplier readiness must include meta object")
    expect(meta.get("source") == "catalog", "supplier readiness meta.source must be catalog")
    expect(meta.get("service") == "flask-no-harness", "supplier readiness meta.service is wrong")

    decision = docs_text("docs/decisions")
    normalized = " ".join(decision.split()).lower()
    expect("get /suppliers/readiness" in normalized, "decision must mention GET /suppliers/readiness")
    expect("supplier readiness" in normalized, "decision must mention supplier readiness")
    expect("lead time" in normalized, "decision must mention lead time")


def check_bundle_quote() -> None:
    response = client().post(
        "/catalog/bundle-quote",
        json={
            "bundle": [
                {"sku": "desk-lamp", "quantity": 1},
                {"sku": "notebook", "quantity": 4},
            ]
        },
    )
    assert_status(response, 200)
    payload = json_payload(response)
    expect(payload.get("currency") == "USD", "bundle quote currency must be USD")
    expect(payload.get("item_count") == 5, "bundle quote item_count is wrong")
    expect_money(payload.get("subtotal"), Decimal("37.50"), "bundle quote subtotal")
    expect_money(payload.get("discount"), Decimal("3.75"), "bundle quote discount")
    expect_money(payload.get("total"), Decimal("33.75"), "bundle quote total")
    expect(str(payload.get("discount_rate")) in {"0.10", "0.1"}, "bundle quote discount_rate is wrong")
    meta = payload.get("meta")
    expect(isinstance(meta, dict), "bundle quote must include meta object")
    expect(meta.get("mode") == "quote", "bundle quote meta.mode must be quote")
    expect(meta.get("service") == "flask-no-harness", "bundle quote meta.service is wrong")

    unknown = client().post("/catalog/bundle-quote", json={"bundle": [{"sku": "missing", "quantity": 1}]})
    assert_status(unknown, 400)
    expect(json_payload(unknown).get("error") == "unknown_sku", "unknown bundle SKU must return unknown_sku")

    invalid = client().post("/catalog/bundle-quote", json={"bundle": [{"sku": "desk-lamp", "quantity": 0}]})
    assert_status(invalid, 400)
    expect(json_payload(invalid).get("error") == "invalid_quantity", "invalid bundle quantity must return invalid_quantity")

    decision = docs_text("docs/decisions")
    normalized = " ".join(decision.split()).lower()
    expect("post /catalog/bundle-quote" in normalized, "decision must mention POST /catalog/bundle-quote")
    expect("bundle discount" in normalized, "decision must mention bundle discount")
    expect("preview-only" in normalized, "decision must mention preview-only quote behavior")


def check_reservation_preview() -> None:
    response = client().post(
        "/inventory/reservations/preview",
        json={
            "items": [
                {"sku": "desk-lamp", "quantity": 4},
                {"sku": "standing-mat", "quantity": 2},
            ]
        },
    )
    assert_status(response, 200)
    payload = json_payload(response)
    reservations = payload.get("reservations")
    summary = payload.get("summary")
    meta = payload.get("meta")

    expect(isinstance(reservations, list), "reservation preview must return reservations list")
    expect(
        [
            (
                item.get("sku"),
                item.get("status"),
                item.get("requested_quantity"),
                item.get("accepted_quantity"),
                item.get("rejected_quantity"),
                item.get("projected_stock"),
            )
            for item in reservations
        ]
        == [
            ("desk-lamp", "reserved", 4, 4, 0, 8),
            ("standing-mat", "partial", 2, 1, 1, 2),
        ],
        "reservation preview rows are wrong",
    )
    expect(summary == {"requested": 6, "accepted": 5, "rejected": 1}, "reservation preview summary is wrong")
    expect(isinstance(meta, dict), "reservation preview must include meta object")
    expect(meta.get("mode") == "preview", "reservation preview meta.mode must be preview")
    expect(meta.get("safety_stock") == 2, "reservation preview safety stock is wrong")
    expect(meta.get("service") == "flask-no-harness", "reservation preview meta.service is wrong")

    products = json_payload(client().get("/products")).get("products")
    standing_mat = next(product for product in products if product["sku"] == "standing-mat")
    expect(standing_mat.get("stock") == 3, "reservation preview must not mutate catalog stock")

    unknown = client().post("/inventory/reservations/preview", json={"items": [{"sku": "missing", "quantity": 1}]})
    assert_status(unknown, 400)
    expect(json_payload(unknown).get("error") == "unknown_sku", "unknown reservation SKU must return unknown_sku")

    invalid = client().post("/inventory/reservations/preview", json={"items": [{"sku": "desk-lamp", "quantity": 0}]})
    assert_status(invalid, 400)
    expect(json_payload(invalid).get("error") == "invalid_quantity", "invalid reservation quantity must return invalid_quantity")

    glossary = glossary_text()
    expect_terms(
        glossary,
        ("/inventory/reservations/preview", "safety stock", "2"),
        "glossary must document reservation preview route and safety stock",
    )


def check_cart_validation() -> None:
    response = client().post(
        "/cart/validate",
        json={
            "items": [
                {"sku": "desk-lamp", "quantity": 2},
                {"sku": "standing-mat", "quantity": 5},
            ]
        },
    )
    assert_status(response, 200)
    payload = json_payload(response)
    items = payload.get("items")
    summary = payload.get("summary")
    meta = payload.get("meta")

    expect(isinstance(items, list), "cart validation must return items list")
    expect(
        [
            (
                item.get("sku"),
                item.get("status"),
                item.get("requested_quantity"),
                item.get("accepted_quantity"),
                item.get("rejected_quantity"),
            )
            for item in items
        ]
        == [
            ("desk-lamp", "accepted", 2, 2, 0),
            ("standing-mat", "limited", 5, 3, 2),
        ],
        "cart validation rows are wrong",
    )
    expect(summary == {"requested": 7, "accepted": 5, "rejected": 2}, "cart validation summary is wrong")
    expect(isinstance(meta, dict), "cart validation must include meta object")
    expect(meta.get("mode") == "validation", "cart validation meta.mode is wrong")
    expect(meta.get("service") == "flask-no-harness", "cart validation meta.service is wrong")

    products = json_payload(client().get("/products")).get("products")
    standing_mat = next(product for product in products if product["sku"] == "standing-mat")
    expect(standing_mat.get("stock") == 3, "cart validation must not mutate stock")

    unknown = client().post("/cart/validate", json={"items": [{"sku": "missing", "quantity": 1}]})
    assert_status(unknown, 400)
    expect(json_payload(unknown).get("error") == "unknown_sku", "unknown cart SKU must return unknown_sku")

    invalid = client().post("/cart/validate", json={"items": [{"sku": "desk-lamp", "quantity": 0}]})
    assert_status(invalid, 400)
    expect(json_payload(invalid).get("error") == "invalid_quantity", "invalid cart quantity must return invalid_quantity")

    decision = " ".join(docs_text("docs/decisions").split()).lower()
    expect("post /cart/validate" in decision, "decision must mention POST /cart/validate")
    expect("preview-only" in decision, "decision must describe preview-only validation")
    expect("limited" in decision, "decision must mention limited cart status")


def check_catalog_metrics() -> None:
    response = client().get("/catalog/metrics")
    assert_status(response, 200)
    payload = json_payload(response)
    metrics = payload.get("metrics")
    meta = payload.get("meta")

    expect(isinstance(metrics, dict), "catalog metrics must return metrics object")
    expect(metrics.get("total_skus") == 3, "catalog metrics total_skus is wrong")
    expect(metrics.get("total_units") == 63, "catalog metrics total_units is wrong")
    expect_money(metrics.get("inventory_value"), Decimal("573.00"), "catalog metrics inventory_value")
    expect_money(metrics.get("average_price"), Decimal("22.92"), "catalog metrics average_price")
    expect(metrics.get("highest_stock_sku") == "notebook", "catalog metrics highest_stock_sku is wrong")
    expect(metrics.get("lowest_stock_sku") == "standing-mat", "catalog metrics lowest_stock_sku is wrong")
    expect(isinstance(meta, dict), "catalog metrics must include meta object")
    expect(meta.get("source") == "catalog", "catalog metrics meta.source is wrong")
    expect(meta.get("service") == "flask-no-harness", "catalog metrics meta.service is wrong")
    expect(meta.get("rules") == "catalog-metrics-v1", "catalog metrics rules marker is wrong")

    glossary = glossary_text()
    expect_terms(
        glossary,
        ("/catalog/metrics", "inventory value", "average price"),
        "glossary must document catalog metrics route and concepts",
    )


def check_catalog_segments() -> None:
    response = client().get("/catalog/segments")
    assert_status(response, 200)
    payload = json_payload(response)
    segments = payload.get("segments")
    summary = payload.get("summary")
    meta = payload.get("meta")

    expect(isinstance(segments, list), "catalog segments must return segments list")
    expect(
        [
            (item.get("sku"), item.get("price_band"), item.get("stock_band"))
            for item in segments
        ]
        == [
            ("desk-lamp", "standard", "steady"),
            ("notebook", "budget", "deep"),
            ("standing-mat", "premium", "scarce"),
        ],
        "catalog segment rows are wrong",
    )
    expect(
        summary == {
            "price_bands": {"budget": 1, "standard": 1, "premium": 1},
            "stock_bands": {"scarce": 1, "steady": 1, "deep": 1},
        },
        "catalog segment summary is wrong",
    )
    expect(isinstance(meta, dict), "catalog segments must include meta object")
    expect(meta.get("source") == "catalog", "catalog segments meta.source is wrong")
    expect(meta.get("service") == "flask-no-harness", "catalog segments meta.service is wrong")
    expect(meta.get("rules") == "catalog-segments-v1", "catalog segments rules marker is wrong")

    glossary = glossary_text()
    expect_terms(
        glossary,
        ("/catalog/segments", "budget", "standard", "premium", "scarce", "steady", "deep"),
        "glossary must document catalog segments route and bands",
    )


def check_pick_list() -> None:
    response = client().post(
        "/warehouse/pick-list",
        json={
            "items": [
                {"sku": "notebook", "quantity": 3},
                {"sku": "desk-lamp", "quantity": 1},
            ]
        },
    )
    assert_status(response, 200)
    payload = json_payload(response)
    picks = payload.get("picks")
    summary = payload.get("summary")
    meta = payload.get("meta")

    expect(isinstance(picks, list), "pick list must return picks list")
    expect(
        [
            (item.get("sku"), item.get("bin"), item.get("quantity"))
            for item in picks
        ]
        == [
            ("desk-lamp", "A1", 1),
            ("notebook", "B2", 3),
        ],
        "pick list rows are wrong",
    )
    expect(summary == {"total_units": 4, "distinct_skus": 2}, "pick list summary is wrong")
    expect(isinstance(meta, dict), "pick list must include meta object")
    expect(meta.get("mode") == "pick", "pick list meta.mode is wrong")
    expect(meta.get("service") == "flask-no-harness", "pick list meta.service is wrong")

    unknown = client().post("/warehouse/pick-list", json={"items": [{"sku": "missing", "quantity": 1}]})
    assert_status(unknown, 400)
    expect(json_payload(unknown).get("error") == "unknown_sku", "unknown pick SKU must return unknown_sku")

    invalid = client().post("/warehouse/pick-list", json={"items": [{"sku": "desk-lamp", "quantity": 0}]})
    assert_status(invalid, 400)
    expect(json_payload(invalid).get("error") == "invalid_quantity", "invalid pick quantity must return invalid_quantity")

    decision = " ".join(docs_text("docs/decisions").split()).lower()
    expect("post /warehouse/pick-list" in decision, "decision must mention POST /warehouse/pick-list")
    expect("bin map" in decision, "decision must mention bin map")
    expect("a1" in decision and "b2" in decision and "c3" in decision, "decision must document pick bins")


def check_tax_preview() -> None:
    response = client().post(
        "/orders/tax-preview",
        json={
            "items": [
                {"sku": "desk-lamp", "quantity": 1},
                {"sku": "notebook", "quantity": 2},
            ]
        },
    )
    assert_status(response, 200)
    payload = json_payload(response)
    expect(payload.get("currency") == "USD", "tax preview currency must be USD")
    expect(payload.get("item_count") == 3, "tax preview item_count is wrong")
    expect_money(payload.get("subtotal"), Decimal("31.00"), "tax preview subtotal")
    expect(str(payload.get("tax_rate")) in {"0.0825", "0.08250"}, "tax preview tax_rate is wrong")
    expect_money(payload.get("tax"), Decimal("2.56"), "tax preview tax")
    expect_money(payload.get("total"), Decimal("33.56"), "tax preview total")
    meta = payload.get("meta")
    expect(isinstance(meta, dict), "tax preview must include meta object")
    expect(meta.get("mode") == "tax_preview", "tax preview meta.mode is wrong")
    expect(meta.get("service") == "flask-no-harness", "tax preview meta.service is wrong")

    unknown = client().post("/orders/tax-preview", json={"items": [{"sku": "missing", "quantity": 1}]})
    assert_status(unknown, 400)
    expect(json_payload(unknown).get("error") == "unknown_sku", "unknown tax preview SKU must return unknown_sku")

    invalid = client().post("/orders/tax-preview", json={"items": [{"sku": "desk-lamp", "quantity": 0}]})
    assert_status(invalid, 400)
    expect(json_payload(invalid).get("error") == "invalid_quantity", "invalid tax preview quantity must return invalid_quantity")

    decision = " ".join(docs_text("docs/decisions").split()).lower()
    expect("post /orders/tax-preview" in decision, "decision must mention POST /orders/tax-preview")
    expect("preview-only" in decision, "decision must describe preview-only tax behavior")
    expect("tax rate" in decision and "0.0825" in decision, "decision must mention tax rate 0.0825")


def check_availability_badge_functional() -> None:
    response = client().get("/products/standing-mat/availability")
    assert_status(response, 200)
    payload = json_payload(response)
    availability = object_field(payload, "availability", default=payload)

    expect(
        normalized_status(availability, ("badge", "status", "state")) == "low_stock",
        "standing-mat availability status must be low_stock",
    )
    expect(availability.get("orderable") is True, "standing-mat must be orderable")
    expect(availability.get("restock_recommended") is True, "standing-mat must recommend restock")
    expect(isinstance(availability.get("message"), str), "availability must include a human-readable message")

    product = payload.get("product") or availability.get("product")
    if product is not None:
        expect(isinstance(product, dict), "availability product summary must be an object when present")
        expect(product.get("sku") == "standing-mat", "availability product sku is wrong")
        expect(product.get("stock") == 3, "availability product stock is wrong")

    in_stock = json_payload(client().get("/products/desk-lamp/availability"))
    in_stock_availability = object_field(in_stock, "availability", default=in_stock)
    expect(
        normalized_status(in_stock_availability, ("badge", "status", "state")) == "in_stock",
        "desk-lamp availability status must be in_stock",
    )
    expect(
        in_stock_availability.get("restock_recommended") is False,
        "desk-lamp must not recommend restock",
    )

    missing = client().get("/products/missing/availability")
    assert_status(missing, 404)
    missing_payload = json_payload(missing)
    expect(missing_payload.get("error") == "product_not_found", "missing SKU must return product_not_found")
    expect(missing_payload.get("sku") == "missing", "missing response must echo sku")

    glossary = glossary_text()
    expect_terms(
        glossary,
        ("/products/<sku>/availability", "in_stock", "low_stock"),
        "glossary must document availability route and statuses",
    )


def check_bundle_quote_functional() -> None:
    response, request_key = first_successful_post(
        "/catalog/bundle-quote",
        (
            {
                "bundle": [
                    {"sku": "desk-lamp", "quantity": 1},
                    {"sku": "notebook", "quantity": 4},
                ]
            },
            {
                "items": [
                    {"sku": "desk-lamp", "quantity": 1},
                    {"sku": "notebook", "quantity": 4},
                ]
            },
        ),
        "bundle quote",
    )
    payload = json_payload(response)
    expect(first_present(payload, ("currency",)) == "USD", "bundle quote currency must be USD")
    expect(first_present(payload, ("item_count",)) == 5, "bundle quote item_count is wrong")
    expect_money(first_present(payload, ("subtotal",)), Decimal("37.50"), "bundle quote subtotal")
    expect_money(first_present(payload, ("discount",)), Decimal("3.75"), "bundle quote discount")
    expect_money(first_present(payload, ("total",)), Decimal("33.75"), "bundle quote total")
    discount_rate = first_present(payload, ("discount_rate",), required=False)
    if discount_rate is not None:
        expect(str(discount_rate) in {"0.10", "0.1"}, "bundle quote discount_rate is wrong")

    unknown = client().post(
        "/catalog/bundle-quote",
        json={request_key: [{"sku": "missing", "quantity": 1}]},
    )
    assert_status(unknown, 400)
    expect(json_payload(unknown).get("error") == "unknown_sku", "unknown bundle SKU must return unknown_sku")

    invalid = client().post(
        "/catalog/bundle-quote",
        json={request_key: [{"sku": "desk-lamp", "quantity": 0}]},
    )
    assert_status(invalid, 400)
    expect(json_payload(invalid).get("error") == "invalid_quantity", "invalid quantity must return invalid_quantity")

    decision = docs_text("docs/decisions") + "\n" + docs_text("docs/domain")
    normalized = " ".join(decision.split()).lower()
    expect("post /catalog/bundle-quote" in normalized, "docs must mention POST /catalog/bundle-quote")
    expect("bundle discount" in normalized, "docs must mention bundle discount")
    expect("preview" in normalized, "docs must mention preview behavior")


def check_cart_validation_functional() -> None:
    response = client().post(
        "/cart/validate",
        json={
            "items": [
                {"sku": "desk-lamp", "quantity": 2},
                {"sku": "standing-mat", "quantity": 5},
            ]
        },
    )
    assert_status(response, 200)
    payload = json_payload(response)
    rows = rows_by_sku(payload)
    desk_lamp = rows.get("desk-lamp")
    standing_mat = rows.get("standing-mat")
    expect(isinstance(desk_lamp, dict), "cart validation must include desk-lamp row")
    expect(isinstance(standing_mat, dict), "cart validation must include standing-mat row")
    expect(normalized_status(desk_lamp, ("status", "state")) == "accepted", "desk-lamp row must be accepted")
    expect(normalized_status(standing_mat, ("status", "state")) == "limited", "standing-mat row must be limited")
    expect(first_present(standing_mat, ("accepted_quantity", "accepted", "available_quantity")) == 3, "standing-mat accepted quantity is wrong")
    expect(first_present(standing_mat, ("rejected_quantity", "rejected")) == 2, "standing-mat rejected quantity is wrong")

    expect(first_present(payload, ("requested", "requested_quantity")) == 7, "cart requested summary is wrong")
    expect(first_present(payload, ("accepted", "accepted_quantity")) == 5, "cart accepted summary is wrong")
    expect(first_present(payload, ("rejected", "rejected_quantity")) == 2, "cart rejected summary is wrong")

    products = json_payload(client().get("/products")).get("products")
    standing_product = next(product for product in products if product["sku"] == "standing-mat")
    expect(standing_product.get("stock") == 3, "cart validation must not mutate stock")

    unknown = client().post("/cart/validate", json={"items": [{"sku": "missing", "quantity": 1}]})
    assert_status(unknown, 400)
    expect(json_payload(unknown).get("error") == "unknown_sku", "unknown cart SKU must return unknown_sku")

    invalid = client().post("/cart/validate", json={"items": [{"sku": "desk-lamp", "quantity": 0}]})
    assert_status(invalid, 400)
    expect(json_payload(invalid).get("error") == "invalid_quantity", "invalid cart quantity must return invalid_quantity")


def check_catalog_metrics_functional() -> None:
    response = client().get("/catalog/metrics")
    assert_status(response, 200)
    payload = json_payload(response)
    metrics = object_field(payload, "metrics", default=payload)

    expect(first_present(metrics, ("total_skus", "sku_count", "skus")) == 3, "catalog metrics sku count is wrong")
    expect(first_present(metrics, ("total_units", "unit_count", "stock_units")) == 63, "catalog metrics total units is wrong")
    expect_money(first_present(metrics, ("inventory_value",)), Decimal("573.00"), "catalog metrics inventory value")
    expect_money(first_present(metrics, ("average_price", "average_item_price")), Decimal("22.92"), "catalog metrics average price")
    expect(
        first_present(metrics, ("highest_stock_sku", "max_stock_sku")) == "notebook",
        "catalog metrics highest stock sku is wrong",
    )
    expect(
        first_present(metrics, ("lowest_stock_sku", "min_stock_sku")) == "standing-mat",
        "catalog metrics lowest stock sku is wrong",
    )

    glossary = glossary_text()
    expect_terms(
        glossary,
        ("/catalog/metrics", "inventory value", "average price"),
        "glossary must document catalog metrics route and concepts",
    )


def check_catalog_segments_functional() -> None:
    response = client().get("/catalog/segments")
    assert_status(response, 200)
    payload = json_payload(response)
    rows = rows_by_sku(payload)
    expected = {
        "desk-lamp": ("standard", "steady"),
        "notebook": ("budget", "deep"),
        "standing-mat": ("premium", "scarce"),
    }
    for sku, (price_band, stock_band) in expected.items():
        row = rows.get(sku)
        expect(isinstance(row, dict), f"catalog segments must include {sku} row")
        expect(row.get("price_band") == price_band, f"{sku} price band is wrong")
        expect(row.get("stock_band") == stock_band, f"{sku} stock band is wrong")

    expect(first_present(payload, ("budget",)) == 1, "catalog segments budget count is wrong")
    expect(first_present(payload, ("standard",)) == 1, "catalog segments standard count is wrong")
    expect(first_present(payload, ("premium",)) == 1, "catalog segments premium count is wrong")
    expect(first_present(payload, ("scarce",)) == 1, "catalog segments scarce count is wrong")
    expect(first_present(payload, ("steady",)) == 1, "catalog segments steady count is wrong")
    expect(first_present(payload, ("deep",)) == 1, "catalog segments deep count is wrong")

    glossary = glossary_text()
    expect_terms(
        glossary,
        ("/catalog/segments", "budget", "standard", "premium", "scarce", "steady", "deep"),
        "glossary must document catalog segments route and bands",
    )


def check_bundle_quote_schema() -> None:
    response, request_key = first_successful_post(
        "/catalog/bundle-quote",
        (
            {"bundle": [{"sku": "desk-lamp", "quantity": 1}]},
            {"items": [{"sku": "desk-lamp", "quantity": 1}]},
        ),
        "bundle quote schema",
    )
    check_response_schema_style(response, "bundle quote")
    error_response = client().post(
        "/catalog/bundle-quote",
        json={request_key: [{"sku": "missing", "quantity": 1}]},
    )
    check_error_schema_style(error_response, "bundle quote unknown SKU")


def check_cart_validation_schema() -> None:
    response = client().post("/cart/validate", json={"items": [{"sku": "desk-lamp", "quantity": 1}]})
    check_response_schema_style(response, "cart validation")
    error_response = client().post("/cart/validate", json={"items": [{"sku": "missing", "quantity": 1}]})
    check_error_schema_style(error_response, "cart validation unknown SKU")


def check_get_schema_style(path: str, label: str) -> None:
    response = client().get(path)
    check_response_schema_style(response, label)


def check_response_schema_style(response: Any, label: str) -> None:
    assert_status(response, 200)
    payload = json_payload(response)
    expect_snake_case_keys(payload, label)
    expect_money_like_values(payload, label)
    meta = payload.get("meta")
    expect(isinstance(meta, dict), f"{label} must include meta object")
    expect(meta.get("service") == "flask-no-harness", f"{label} meta.service is wrong")


def check_error_schema_style(response: Any, label: str) -> None:
    expect(response.status_code in {400, 404}, f"{label} must return a client error status")
    payload = json_payload(response)
    expect_snake_case_keys(payload, label)
    expect(isinstance(payload.get("error"), str), f"{label} error response must include error string")


def assert_status(response: Any, expected_status: int) -> None:
    expect(
        response.status_code == expected_status,
        f"expected status {expected_status}, got {response.status_code}: {response.get_data(as_text=True)}",
    )


def json_payload(response: Any) -> dict[str, Any]:
    payload = response.get_json(silent=True)
    expect(isinstance(payload, dict), f"response was not a JSON object: {response.get_data(as_text=True)}")
    return payload


def object_field(payload: dict[str, Any], key: str, *, default: dict[str, Any]) -> dict[str, Any]:
    value = payload.get(key)
    if value is None:
        return default
    expect(isinstance(value, dict), f"{key} must be an object when present")
    return value


def normalized_status(payload: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = payload.get(key)
        if value is not None:
            return str(value).strip().lower().replace(" ", "_")
    return ""


def normalized_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(normalized_text(child) for child in value.values())
    if isinstance(value, list):
        return " ".join(normalized_text(child) for child in value)
    return str(value).lower()


def first_successful_post(
    path: str,
    payloads: tuple[dict[str, Any], ...],
    label: str,
) -> tuple[Any, str]:
    last_response = None
    for payload in payloads:
        response = client().post(path, json=payload)
        if response.status_code == 200:
            return response, next(iter(payload))
        last_response = response
    if last_response is None:
        fail(f"{label} did not receive any request payloads")
    assert_status(last_response, 200)
    fail(f"{label} did not accept any supported request envelope")


def first_present(payload: Any, keys: tuple[str, ...], *, required: bool = True) -> Any:
    if isinstance(payload, dict):
        for key in keys:
            if key in payload:
                return payload[key]
        for child in payload.values():
            value = first_present(child, keys, required=False)
            if value is not None:
                return value
    elif isinstance(payload, list):
        for child in payload:
            value = first_present(child, keys, required=False)
            if value is not None:
                return value
    if required:
        fail(f"missing expected field matching one of: {', '.join(keys)}")
    return None


def rows_by_sku(payload: Any) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    collect_rows_by_sku(payload, rows)
    return rows


def collect_rows_by_sku(value: Any, rows: dict[str, dict[str, Any]]) -> None:
    if isinstance(value, dict):
        sku = value.get("sku")
        if isinstance(sku, str):
            rows[sku] = value
        for child in value.values():
            collect_rows_by_sku(child, rows)
    elif isinstance(value, list):
        for child in value:
            collect_rows_by_sku(child, rows)


def expect_snake_case_keys(value: Any, label: str, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            expect(isinstance(key, str) and bool(SNAKE_CASE.match(key)), f"{label} key {path}.{key} must be snake_case")
            expect_snake_case_keys(child, label, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            expect_snake_case_keys(child, label, f"{path}[{index}]")


def expect_money_like_values(value: Any, label: str, path: str = "$", key: str = "") -> None:
    if isinstance(value, dict):
        for child_key, child in value.items():
            child_path = f"{path}.{child_key}"
            if is_money_key(child_key):
                expect_decimal_compatible(child, label, child_path)
            expect_money_like_values(child, label, child_path, child_key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            expect_money_like_values(child, label, f"{path}[{index}]", key)


def is_money_key(key: str) -> bool:
    return any(term in key for term in MONEY_KEY_TERMS)


def expect_decimal_compatible(value: Any, label: str, path: str) -> None:
    expect(value is not None and not isinstance(value, bool), f"{label} {path} must be decimal-compatible")
    try:
        Decimal(str(value))
    except Exception as exc:  # noqa: BLE001
        fail(f"{label} {path} must be decimal-compatible: {value!r} ({exc})")


def docs_text(relative_dir: str) -> str:
    directory = ROOT / relative_dir
    expect(directory.exists(), f"missing documentation directory: {relative_dir}")
    files = sorted(path for path in directory.glob("*.md") if path.name != "README.md")
    expect(bool(files), f"no documentation records found under {relative_dir}")
    return "\n".join(path.read_text(encoding="utf-8") for path in files)


def glossary_text() -> str:
    glossary = ROOT / "docs" / "domain" / "glossary.md"
    expect(glossary.exists(), "domain glossary must exist")
    return normalize_doc_text(glossary.read_text(encoding="utf-8"))


def normalize_doc_text(text: str) -> str:
    return " ".join(text.split()).lower()


def expect_terms(text: str, terms: tuple[str, ...], label: str) -> None:
    missing = [term for term in terms if term.lower() not in text]
    expect(not missing, f"{label}; missing: {', '.join(missing)}")


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def expect_money(actual: Any, expected: Decimal, label: str) -> None:
    try:
        normalized = money(Decimal(str(actual)))
    except Exception as exc:  # noqa: BLE001
        fail(f"{label} is not a decimal-compatible value: {actual!r} ({exc})")
    expect(normalized == money(expected), f"{label} expected {money(expected)}, got {normalized}")


def expect(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def fail(message: str) -> None:
    print(f"hidden oracle failure: {message}", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
