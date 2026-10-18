# Dashboard build guide (Power BI Desktop)

> Honest note: this repository is built and tested on Linux, where Power BI
> Desktop cannot run. The steps below are the exact build sequence for the
> dashboard; screenshots will be added once the report is published from a
> Windows machine. Everything up to the data layer is reproducible today via
> `data/generate_data.py` + `python/eda.py`.

All data is **synthetic**.

## 1. Prepare the data

1. Run `python data/generate_data.py` — produces the five CSVs in `data/`.
2. (Optional) Load them into PostgreSQL with `sql/schema.sql` via
   `COPY customers FROM 'data/customers.csv' CSV HEADER;` etc.

## 2. Load into Power BI

1. Power BI Desktop → **Get Data → Text/CSV**, load the five CSVs
   (or connect to PostgreSQL via Get Data → Database → PostgreSQL).
2. Create the `Date` table and relationships exactly as described in
   [`data_model.md`](data_model.md).
3. Set data types: `order_date`/`signup_date` → Date; `price`, `unit_price`,
   `cost`, `discount` → Decimal; `quantity` → Whole number.

## 3. Add the measures

Modeling tab → **New measure**, paste each block from
[`dax_measures.dax`](dax_measures.dax):
Total Revenue, Total Orders, Avg Order Value, MoM Revenue Growth %,
YTD Revenue, Return Rate %, Total Profit, Profit Margin %.

## 4. Build the pages

**Page 1 — Executive overview**
- KPI cards: Total Revenue, Total Orders, Avg Order Value, Return Rate %
- Line chart: Total Revenue by Month (add MoM Revenue Growth % as tooltip)
- Bar chart: Total Revenue by Category
- Donut: Orders by Payment Method

`[screenshot placeholder — executive overview]`

**Page 2 — Customers**
- KPI cards: Total Customers, Avg Customer Lifetime Value, New Customers
- Map or bar: Revenue by City
- Table: top 20 customers by lifetime value (from `sql/analysis.sql` Q3)
- Bar: customers by Segment

`[screenshot placeholder — customer page]`

**Page 3 — Product & returns**
- Bar: Return Rate % by Category
- Table: top 10 products by revenue with cumulative share (Q8)
- Slicers: Year, Category, Payment Method (sync across pages)

`[screenshot placeholder — product & returns page]`

## 5. Publish

File → Publish → Power BI Service, then share the link here and replace the
placeholders above with exported PNGs.
