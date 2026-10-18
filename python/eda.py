#!/usr/bin/env python3
"""Exploratory data analysis for the synthetic e-commerce dataset.

Loads the CSVs produced by data/generate_data.py, computes KPIs, and saves
charts to reports/figures/. All data is SYNTHETIC.

Usage:
    python python/eda.py [--data data] [--out reports]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless backend — no display needed
import matplotlib.pyplot as plt
import pandas as pd

pd.options.display.float_format = "{:,.2f}".format


def load(data_dir: Path) -> dict[str, pd.DataFrame]:
    frames = {}
    for name in ("customers", "products", "orders", "order_items", "returns"):
        frames[name] = pd.read_csv(data_dir / f"{name}.csv")
    frames["orders"]["order_date"] = pd.to_datetime(frames["orders"]["order_date"])
    frames["customers"]["signup_date"] = pd.to_datetime(frames["customers"]["signup_date"])
    return frames


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data")
    parser.add_argument("--out", default="reports")
    args = parser.parse_args()

    data_dir = Path(args.data)
    out = Path(args.out)
    figs = out / "figures"
    figs.mkdir(parents=True, exist_ok=True)

    d = load(data_dir)
    customers, products, orders = d["customers"], d["products"], d["orders"]
    items, returns = d["order_items"], d["returns"]

    valid = orders[orders["status"] != "Cancelled"]
    items_v = items[items["order_id"].isin(valid["order_id"])]
    items_v = items_v.copy()
    items_v["line_revenue"] = items_v["quantity"] * items_v["unit_price"] * (1 - items_v["discount"])

    # ---- KPIs ----
    total_revenue = items_v["line_revenue"].sum()
    total_orders = valid["order_id"].nunique()
    aov = total_revenue / total_orders
    total_customers = customers["customer_id"].nunique()
    delivered = valid[valid["status"] == "Delivered"]
    return_rate = len(returns) / len(items[items["order_id"].isin(delivered["order_id"])]) * 100

    print("=== KPI SUMMARY (synthetic data) ===")
    print(f"Total revenue      : Rs {total_revenue:,.2f}")
    print(f"Total orders       : {total_orders:,}")
    print(f"Average order value: Rs {aov:,.2f}")
    print(f"Total customers    : {total_customers:,}")
    print(f"Line-item return % : {return_rate:.2f}%")

    # ---- monthly revenue ----
    monthly = (items_v.assign(order_date=items_v["order_id"].map(
                    valid.set_index("order_id")["order_date"]))
               .assign(month=lambda x: x["order_date"].dt.to_period("M").astype(str))
               .groupby("month")["line_revenue"].sum())
    print("\n=== MONTHLY REVENUE (first 6 months) ===")
    print(monthly.head(6).to_string())

    fig, ax = plt.subplots(figsize=(10, 4))
    monthly.plot(ax=ax, marker="o")
    ax.set_title("Monthly Revenue Trend (synthetic)")
    ax.set_ylabel("Revenue (Rs)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(figs / "monthly_revenue.png", dpi=120)
    plt.close(fig)

    # ---- revenue by category ----
    cat_rev = (items_v.merge(products[["product_id", "category"]], on="product_id")
               .groupby("category")["line_revenue"].sum().sort_values(ascending=False))
    print("\n=== REVENUE BY CATEGORY ===")
    print(cat_rev.to_string())

    fig, ax = plt.subplots(figsize=(8, 4))
    cat_rev.plot.bar(ax=ax)
    ax.set_title("Revenue by Category (synthetic)")
    ax.set_ylabel("Revenue (Rs)")
    fig.tight_layout()
    fig.savefig(figs / "revenue_by_category.png", dpi=120)
    plt.close(fig)

    # ---- payment method mix ----
    pay = valid["payment_method"].value_counts()
    print("\n=== PAYMENT METHOD MIX ===")
    print((pay / pay.sum() * 100).round(1).to_string())

    fig, ax = plt.subplots(figsize=(6, 6))
    pay.plot.pie(ax=ax, autopct="%1.1f%%", startangle=90)
    ax.set_title("Payment Method Mix (synthetic)")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(figs / "payment_mix.png", dpi=120)
    plt.close(fig)

    # ---- customer LTV distribution ----
    cust_rev = items_v.assign(
        customer_id=items_v["order_id"].map(valid.set_index("order_id")["customer_id"])
    ).groupby("customer_id")["line_revenue"].sum()
    print("\n=== CUSTOMER LIFETIME VALUE ===")
    print(cust_rev.describe().to_string())

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(cust_rev, bins=40, edgecolor="white")
    ax.set_title("Customer Lifetime Value Distribution (synthetic)")
    ax.set_xlabel("Lifetime revenue (Rs)")
    ax.set_ylabel("Customers")
    fig.tight_layout()
    fig.savefig(figs / "ltv_distribution.png", dpi=120)
    plt.close(fig)

    print(f"\ncharts saved to {figs}/")


if __name__ == "__main__":
    main()
