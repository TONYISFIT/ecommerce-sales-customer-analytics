# E-commerce Sales & Customer Analytics

End-to-end analytics project on a **synthetic** e-commerce dataset:
data generation → SQL modeling → Python EDA → Power BI dashboard.

> **All data in this project is synthetic.** It was generated with a seeded
> random number generator (`data/generate_data.py`, seed 42) and does not
> represent any real company, customer, or order.

## What this covers

| Layer | Contents |
|---|---|
| Data generation | `data/generate_data.py` — 1,200 customers, 86 products, 5,000 orders, ~10.8k line items, 400 returns, with enforced referential integrity |
| SQL warehouse | `sql/schema.sql` — star-schema DDL (PostgreSQL; MySQL notes included) |
| SQL analytics | `sql/analysis.sql` — 8 commented queries: monthly revenue + MoM growth, category P&L, customer LTV, RFM segmentation (NTILE), return rate by category, new vs returning customers, payment mix, top products with running totals |
| Python EDA | `python/eda.py` — pandas KPIs + matplotlib charts |
| Power BI | `powerbi/` — DAX measures, star-schema data model doc, step-by-step dashboard build guide |
| Tests | `tests/test_data.py` — 6 pytest checks (row counts, PK uniqueness, FK integrity, value ranges) |

## Quickstart

```bash
pip install -r requirements.txt

# 1. Generate the synthetic dataset (seeded, reproducible)
python data/generate_data.py

# 2. Run the data-quality tests
pytest

# 3. Run the exploratory analysis (prints KPIs, saves charts to reports/figures/)
python python/eda.py
```

Load into PostgreSQL with `sql/schema.sql`, then run the analytical queries in
`sql/analysis.sql`. Build the Power BI report by following
`powerbi/dashboard_build_guide.md`.

## Key findings (computed from the synthetic data, seed 42)

| KPI | Value |
|---|---|
| Total revenue | ₹9,92,44,956.78 |
| Total orders (non-cancelled) | 4,295 |
| Average order value | ₹23,107.09 |
| Customers | 1,200 (1,162 with at least one completed order) |
| Line-item return rate | 5.44% |
| Mean customer lifetime value | ₹85,408.74 |

- **Top category by revenue:** Fashion (₹2.24 Cr), followed by Home & Kitchen (₹2.11 Cr) and Electronics (₹1.77 Cr).
- **Payment mix is evenly split** — no method dominates (Wallets 17.3%, COD 17.1%, Net Banking 17.0%, UPI 16.7%, Credit Card 16.6%, Debit Card 15.3%).
- **LTV is right-skewed:** median ₹79,239 vs max ₹3,21,169 — a small set of high-value customers drives a disproportionate share of revenue.

## Project structure

```
├── data/            # generate_data.py + generated CSVs (synthetic)
├── sql/             # schema.sql, analysis.sql
├── python/          # eda.py
├── powerbi/         # dax_measures.dax, data_model.md, dashboard_build_guide.md
├── tests/           # test_data.py
├── reports/figures/ # charts produced by eda.py (generated locally, not committed)
├── requirements.txt
└── LICENSE (MIT)
```

## Notes & limitations

- The dataset is synthetic and intentionally simple (no seasonality, no
  marketing channels, no inventory) — it exists to demonstrate analytics
  technique, not to model a real business.
- The Power BI dashboard guide lists exact build steps; screenshots will be
  added after publishing from Power BI Desktop (this repo was built on Linux,
  where Power BI Desktop doesn't run).
- SQL is written for PostgreSQL; `schema.sql` notes the small MySQL adjustments.
