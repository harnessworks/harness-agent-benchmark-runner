#!/usr/bin/env python3
from __future__ import annotations

import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        fail("usage: flask_hidden_oracle.py <task-id>")

    checks = {
        "hidden-effect-stock-risk": check_stock_risk,
        "hidden-effect-supplier-readiness": check_supplier_readiness,
        "hidden-effect-bundle-quote": check_bundle_quote,
        "hidden-effect-reservation-preview": check_reservation_preview,
    }
    task_id = argv[1]
    if task_id not in checks:
        fail(f"unknown hidden task id: {task_id}")

    checks[task_id]()
    print(f"{task_id}: hidden oracle passed")
    return 0


def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


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
    expect("stock risk report endpoint" in glossary, "glossary must mention stock risk report endpoint")
    expect("critical" in glossary and "watch" in glossary and "healthy" in glossary, "glossary must define risk bands")


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
    expect("reservation preview endpoint" in glossary, "glossary must mention reservation preview endpoint")
    expect("safety stock" in glossary, "glossary must mention safety stock")
    expect("2" in glossary, "glossary must document safety stock value 2")


def assert_status(response: Any, expected_status: int) -> None:
    expect(
        response.status_code == expected_status,
        f"expected status {expected_status}, got {response.status_code}: {response.get_data(as_text=True)}",
    )


def json_payload(response: Any) -> dict[str, Any]:
    payload = response.get_json(silent=True)
    expect(isinstance(payload, dict), f"response was not a JSON object: {response.get_data(as_text=True)}")
    return payload


def docs_text(relative_dir: str) -> str:
    directory = ROOT / relative_dir
    expect(directory.exists(), f"missing documentation directory: {relative_dir}")
    files = sorted(path for path in directory.glob("*.md") if path.name != "README.md")
    expect(bool(files), f"no documentation records found under {relative_dir}")
    return "\n".join(path.read_text(encoding="utf-8") for path in files)


def glossary_text() -> str:
    glossary = ROOT / "docs" / "domain" / "glossary.md"
    expect(glossary.exists(), "domain glossary must exist")
    return " ".join(glossary.read_text(encoding="utf-8").split()).lower()


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
