"""Data-quality tests for the synthetic e-commerce CSVs.

Run from the repo root:  pytest
"""
from pathlib import Path

import pandas as pd
import pytest

DATA = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture(scope="module")
def frames():
    out = {}
    for name in ("customers", "products", "orders", "order_items", "returns"):
        out[name] = pd.read_csv(DATA / f"{name}.csv")
    return out


def test_row_counts(frames):
    assert len(frames["customers"]) == 1200
    assert 80 <= len(frames["products"]) <= 90
    assert len(frames["orders"]) == 5000
    # 1-4 items per non-cancelled order
    assert 4000 <= len(frames["order_items"]) <= 20000
    assert 1 <= len(frames["returns"]) <= 400


def test_primary_keys_unique(frames):
    assert frames["customers"]["customer_id"].is_unique
    assert frames["products"]["product_id"].is_unique
    assert frames["orders"]["order_id"].is_unique
    assert not frames["order_items"][["order_id", "product_id"]].duplicated().any()


def test_no_null_primary_keys(frames):
    for name, key in (("customers", "customer_id"), ("products", "product_id"),
                      ("orders", "order_id")):
        assert frames[name][key].notna().all(), f"null PK in {name}"


def test_foreign_keys_valid(frames):
    cust = set(frames["customers"]["customer_id"])
    prod = set(frames["products"]["product_id"])
    ords = set(frames["orders"]["order_id"])
    assert set(frames["orders"]["customer_id"]) <= cust
    assert set(frames["order_items"]["order_id"]) <= ords
    assert set(frames["order_items"]["product_id"]) <= prod
    assert set(frames["returns"]["order_id"]) <= ords
    assert set(frames["returns"]["product_id"]) <= prod


def test_cancelled_orders_have_no_items(frames):
    cancelled = set(frames["orders"].query("status == 'Cancelled'")["order_id"])
    assert not set(frames["order_items"]["order_id"]) & cancelled


def test_value_ranges(frames):
    items = frames["order_items"]
    assert (items["quantity"] > 0).all()
    assert (items["unit_price"] > 0).all()
    assert ((items["discount"] >= 0) & (items["discount"] <= 1)).all()
    assert (frames["products"]["price"] > 0).all()
    assert set(frames["orders"]["status"]) <= {
        "Delivered", "Shipped", "Processing", "Cancelled"}
