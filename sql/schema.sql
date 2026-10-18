-- ============================================================================
-- E-commerce analytics warehouse schema
-- PostgreSQL-compatible. For MySQL: replace SERIAL with AUTO_INCREMENT,
--   TIMESTAMPTZ/DATE stay the same, and NUMERIC(12,2) works in both engines.
-- All data loaded here is SYNTHETIC (see data/generate_data.py).
-- ============================================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(10)  PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    city        VARCHAR(50)  NOT NULL,
    signup_date DATE         NOT NULL,
    segment     VARCHAR(20)  NOT NULL
        CHECK (segment IN ('New', 'Regular', 'Loyal', 'At-Risk'))
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(10)   PRIMARY KEY,
    name       VARCHAR(100)  NOT NULL,
    category   VARCHAR(50)   NOT NULL,
    price      NUMERIC(12,2) NOT NULL CHECK (price > 0),
    cost       NUMERIC(12,2) NOT NULL CHECK (cost >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id       VARCHAR(10)  PRIMARY KEY,
    customer_id    VARCHAR(10)  NOT NULL REFERENCES customers(customer_id),
    order_date     DATE         NOT NULL,
    status         VARCHAR(20)  NOT NULL
        CHECK (status IN ('Delivered', 'Shipped', 'Processing', 'Cancelled')),
    payment_method VARCHAR(20)  NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id   VARCHAR(10)   NOT NULL REFERENCES orders(order_id),
    product_id VARCHAR(10)   NOT NULL REFERENCES products(product_id),
    quantity   INTEGER       NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price > 0),
    discount   NUMERIC(4,2)  NOT NULL DEFAULT 0 CHECK (discount BETWEEN 0 AND 1),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS returns (
    order_id      VARCHAR(10)  NOT NULL REFERENCES orders(order_id),
    product_id    VARCHAR(10)  NOT NULL REFERENCES products(product_id),
    return_reason VARCHAR(50)  NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

-- Helpful indexes for the analytical queries in analysis.sql
CREATE INDEX IF NOT EXISTS idx_orders_date       ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer   ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_items_order       ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_items_product     ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
