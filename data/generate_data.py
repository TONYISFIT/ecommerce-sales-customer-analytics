#!/usr/bin/env python3
"""Generate synthetic e-commerce datasets for analytics practice.

ALL DATA IN THIS PROJECT IS SYNTHETIC — generated with a seeded RNG for
reproducibility. It does not represent any real company, customer, or order.

Tables:
    customers.csv   ~1,200 rows
    products.csv      ~80 rows
    orders.csv      ~5,000 rows
    order_items.csv ~12,000 rows
    returns.csv       ~400 rows

Referential integrity is enforced: every customer_id / product_id / order_id
referenced by a child table exists in its parent table.

Usage:
    python data/generate_data.py [--out data] [--seed 42]
"""
from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
START = date(2023, 1, 1)
END = date(2024, 12, 31)

FIRST_NAMES = [
    "Aarav", "Aditi", "Arjun", "Ananya", "Diya", "Ishaan", "Kabir", "Meera",
    "Nikhil", "Priya", "Rahul", "Riya", "Rohan", "Sanya", "Varun", "Zara",
    "Aisha", "Dev", "Kavya", "Manav", "Neha", "Om", "Pooja", "Raj",
]
LAST_NAMES = [
    "Sharma", "Patel", "Reddy", "Iyer", "Khan", "Gupta", "Mehta", "Nair",
    "Singh", "Joshi", "Das", "Kulkarni", "Chopra", "Bose", "Agarwal", "Rao",
]
CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Pune",
    "Kolkata", "Ahmedabad", "Jaipur", "Lucknow", "Kochi", "Indore",
]
CATEGORIES = {
    "Electronics": ["Wireless Headphones", "Smartwatch", "Bluetooth Speaker",
                    "USB-C Charger", "Laptop Stand", "Mechanical Keyboard",
                    "Webcam HD", "Power Bank 20000mAh", "Noise-Cancelling Earbuds",
                    "Smart LED Bulb", "Tablet 10-inch", "Portable SSD 1TB",
                    "Gaming Mouse", "USB Hub", "Monitor Light Bar", "Phone Gimbal"],
    "Fashion": ["Cotton T-Shirt", "Denim Jeans", "Running Shoes", "Hoodie",
                "Leather Wallet", "Sunglasses", "Backpack", "Wrist Watch",
                "Kurta", "Sneakers", "Denim Jacket", "Formal Shirt",
                "Sports Shorts", "Handbag", "Leather Belt", "Socks (Pack of 5)"],
    "Home & Kitchen": ["Non-stick Cookware Set", "Air Fryer", "Bedsheet Set",
                       "Table Lamp", "Storage Organizer", "Coffee Maker",
                       "Wall Clock", "Curtain Set", "Mixer Grinder", "Dinner Set",
                       "Vacuum Cleaner", "Electric Kettle", "Throw Pillows",
                       "Laundry Basket", "Knife Set", "Bathroom Organizer"],
    "Beauty": ["Face Wash", "Moisturizer", "Sunscreen SPF50", "Hair Serum",
               "Lipstick Set", "Perfume", "Face Serum", "Body Lotion",
               "Hair Dryer", "Makeup Brush Set", "Nail Polish Set",
               "Face Mask Pack", "Shaving Kit", "Toner"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Cricket Bat", "Football",
               "Badminton Racket", "Gym Gloves", "Skipping Rope", "Water Bottle",
               "Resistance Bands", "Tennis Racket", "Cycling Gloves",
               "Swimming Goggles", "Camping Tent", "Trekking Backpack"],
    "Books": ["Bestseller Fiction", "Data Science Handbook", "Cookbook",
              "Children's Storybook", "Biography", "Self-Help Guide",
              "Mystery Thriller", "History of India", "Poetry Collection",
              "Business Strategy"],
}
PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "COD", "Wallet"]
ORDER_STATUSES = ["Delivered", "Delivered", "Delivered", "Delivered",
                  "Shipped", "Cancelled", "Processing"]
RETURN_REASONS = ["Defective item", "Wrong size", "Not as described",
                  "Changed mind", "Damaged in transit", "Late delivery"]
SEGMENTS = ["New", "Regular", "Loyal", "At-Risk"]


def random_date(rng: random.Random, start: date, end: date) -> date:
    return start + timedelta(days=rng.randint(0, (end - start).days))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic e-commerce data")
    parser.add_argument("--out", default="data", help="output directory")
    parser.add_argument("--seed", type=int, default=SEED, help="RNG seed")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # ---- customers ----
    customers = []
    for i in range(1, 1201):
        customers.append({
            "customer_id": f"C{i:05d}",
            "name": f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}",
            "city": rng.choice(CITIES),
            "signup_date": random_date(rng, START, END).isoformat(),
            "segment": rng.choices(SEGMENTS, weights=[25, 40, 20, 15])[0],
        })

    # ---- products ----
    products = []
    pid = 1
    for category, names in CATEGORIES.items():
        for name in names:
            price = round(rng.uniform(199, 9999), 2)
            cost = round(price * rng.uniform(0.45, 0.75), 2)
            products.append({
                "product_id": f"P{pid:04d}",
                "name": name,
                "category": category,
                "price": price,
                "cost": cost,
            })
            pid += 1

    # ---- orders ----
    orders = []
    for i in range(1, 5001):
        cust = rng.choice(customers)
        order_date = random_date(rng, START, END)
        orders.append({
            "order_id": f"O{i:06d}",
            "customer_id": cust["customer_id"],
            "order_date": order_date.isoformat(),
            "status": rng.choice(ORDER_STATUSES),
            "payment_method": rng.choice(PAYMENT_METHODS),
        })

    # ---- order_items ----
    order_items = []
    for order in orders:
        if order["status"] == "Cancelled":
            continue  # cancelled orders carry no line items
        # sample without replacement so (order_id, product_id) stays unique
        for prod in rng.sample(products, k=rng.randint(1, 4)):
            qty = rng.randint(1, 3)
            discount = round(rng.choice([0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20]), 2)
            order_items.append({
                "order_id": order["order_id"],
                "product_id": prod["product_id"],
                "quantity": qty,
                "unit_price": prod["price"],
                "discount": discount,
            })

    # ---- returns ----
    delivered = [o for o in orders if o["status"] == "Delivered"]
    returns = []
    sampled = rng.sample(delivered, k=min(400, len(delivered)))
    for order in sampled:
        items = [it for it in order_items if it["order_id"] == order["order_id"]]
        if not items:
            continue
        item = rng.choice(items)
        returns.append({
            "order_id": order["order_id"],
            "product_id": item["product_id"],
            "return_reason": rng.choice(RETURN_REASONS),
        })

    datasets = {
        "customers.csv": customers,
        "products.csv": products,
        "orders.csv": orders,
        "order_items.csv": order_items,
        "returns.csv": returns,
    }
    for fname, rows in datasets.items():
        path = out / fname
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {path} ({len(rows)} rows)")

    # ---- integrity self-check ----
    cust_ids = {c["customer_id"] for c in customers}
    prod_ids = {p["product_id"] for p in products}
    order_ids = {o["order_id"] for o in orders}
    assert all(o["customer_id"] in cust_ids for o in orders), "orders FK broken"
    assert all(i["order_id"] in order_ids and i["product_id"] in prod_ids
               for i in order_items), "order_items FK broken"
    assert all(r["order_id"] in order_ids and r["product_id"] in prod_ids
               for r in returns), "returns FK broken"
    print("referential integrity OK")


if __name__ == "__main__":
    main()
