"""
seed_database.py
----------------
Drops and recreates all tables defined in model.py, then bulk-inserts
the Olist e-commerce CSV datasets into MySQL.

Usage:
    python seed_database.py
"""

import os
import pandas as pd
from dotenv import load_dotenv

from database import engine
from model import Base

load_dotenv()

DATASETS_DIR = "datasets"


def load_and_insert(csv_filename: str, table_name: str, dtype=None, parse_dates=None):
    """Load a CSV file and insert its rows into the given MySQL table."""
    path = os.path.join(DATASETS_DIR, csv_filename)
    df = pd.read_csv(path, dtype=dtype, parse_dates=parse_dates or [])
    inserted = df.to_sql(
        table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=500,
    )
    print(f"✔ {table_name}: inserted {inserted}/{len(df)} rows")


def seed():
    """Drop all tables, recreate them, and populate from CSV files."""
    # Recreate all tables so schema + constraints are correct
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # -------------------------------------------------------
    # 1. Customers (no FK dependency)
    # -------------------------------------------------------
    load_and_insert(
        "olist_customers_dataset.csv",
        "customers",
        dtype={
            "customer_id": str,
            "customer_unique_id": str,
            "customer_zip_code_prefix": str,
        },
    )

    # -------------------------------------------------------
    # 2. Geolocation (no FK dependency)
    # -------------------------------------------------------
    geo_df = pd.read_csv(
        os.path.join(DATASETS_DIR, "olist_geolocation_dataset.csv"),
        dtype={"geolocation_zip_code_prefix": str},
    )
    geo_inserted = geo_df.to_sql(
        "geolocation",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=500,
    )
    print(f"✔ geolocation: inserted {geo_inserted}/{len(geo_df)} rows")

    # -------------------------------------------------------
    # 3. Sellers (no FK dependency)
    # -------------------------------------------------------
    load_and_insert(
        "olist_sellers_dataset.csv",
        "sellers",
        dtype={
            "seller_id": str,
            "seller_zip_code_prefix": str,
        },
    )

    # -------------------------------------------------------
    # 4. Products (no FK dependency)
    # -------------------------------------------------------
    load_and_insert(
        "olist_products_dataset.csv",
        "products",
        dtype={"product_id": str},
    )

    # -------------------------------------------------------
    # 5. Product Category Translation (no FK dependency)
    # -------------------------------------------------------
    load_and_insert(
        "product_category_name_translation.csv",
        "product_category_name_translation",
    )

    # -------------------------------------------------------
    # 6. Orders (depends on customers)
    # -------------------------------------------------------
    load_and_insert(
        "olist_orders_dataset.csv",
        "orders",
        dtype={"order_id": str, "customer_id": str},
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    # -------------------------------------------------------
    # 7. Order Items (depends on orders, products, sellers)
    # -------------------------------------------------------
    load_and_insert(
        "olist_order_items_dataset.csv",
        "order_items",
        dtype={
            "order_id": str,
            "product_id": str,
            "seller_id": str,
        },
        parse_dates=["shipping_limit_date"],
    )

    # -------------------------------------------------------
    # 8. Order Payments (depends on orders)
    # -------------------------------------------------------
    load_and_insert(
        "olist_order_payments_dataset.csv",
        "order_payments",
        dtype={"order_id": str},
    )

    # -------------------------------------------------------
    # 9. Order Reviews (depends on orders)
    # -------------------------------------------------------
    load_and_insert(
        "olist_order_reviews_dataset.csv",
        "order_reviews",
        dtype={
            "review_id": str,
            "order_id": str,
        },
        parse_dates=[
            "review_creation_date",
            "review_answer_timestamp",
        ],
    )

    print("\n🎉 All datasets loaded successfully!")


if __name__ == "__main__":
    seed()
