import os
import sqlite3
import logging
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(BASE_DIR, "data", "raw_sales.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DB_FILE = os.path.join(OUTPUT_DIR, "warehouse.db")
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.log")
DQ_REPORT_FILE = os.path.join(OUTPUT_DIR, "data_quality_report.txt")


os.makedirs(OUTPUT_DIR, exist_ok=True)


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_data():
    logging.info("Extracting raw sales data from CSV")
    df = pd.read_csv(DATA_FILE)
    logging.info(f"Extracted {len(df)} rows")
    return df


def connect_database():
    logging.info("Connecting to SQLite warehouse database")
    conn = sqlite3.connect(DB_FILE)
    return conn


def create_tables(conn):
    logging.info("Creating staging and warehouse tables")

    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS staging_sales;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staging_sales (
            order_id TEXT,
            customer_id TEXT,
            customer_name TEXT,
            product_id TEXT,
            product_name TEXT,
            quantity TEXT,
            unit_price TEXT,
            order_date TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id TEXT PRIMARY KEY,
            product_name TEXT,
            unit_price REAL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_sales (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_amount REAL,
            order_date TEXT
        );
    """)

    conn.commit()


def load_staging_table(conn, df):
    logging.info("Loading raw data into staging_sales table")
    df.to_sql("staging_sales", conn, if_exists="append", index=False)
    logging.info("Raw data loaded into staging layer")


def validate_and_clean_data(df):
    logging.info("Starting data validation and cleaning")

    total_rows = len(df)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    duplicate_rows = df.duplicated().sum()
    missing_quantity = df["quantity"].isna().sum()
    invalid_price = (df["unit_price"] <= 0).sum()
    invalid_dates = df["order_date"].isna().sum()

    clean_df = df.drop_duplicates()

    clean_df = clean_df.dropna(subset=[
        "order_id",
        "customer_id",
        "customer_name",
        "product_id",
        "product_name",
        "quantity",
        "unit_price",
        "order_date"
    ])

    clean_df = clean_df[
        (clean_df["quantity"] > 0) &
        (clean_df["unit_price"] > 0)
    ]

    clean_df["quantity"] = clean_df["quantity"].astype(int)
    clean_df["order_date"] = clean_df["order_date"].dt.strftime("%Y-%m-%d")
    clean_df["total_amount"] = clean_df["quantity"] * clean_df["unit_price"]

    rejected_rows = total_rows - len(clean_df)

    dq_summary = {
        "total_rows": total_rows,
        "duplicate_rows": int(duplicate_rows),
        "missing_quantity": int(missing_quantity),
        "invalid_price_rows": int(invalid_price),
        "invalid_date_rows": int(invalid_dates),
        "clean_rows_loaded": len(clean_df),
        "rejected_rows": rejected_rows
    }

    logging.info(f"Validation completed. Clean rows: {len(clean_df)}, Rejected rows: {rejected_rows}")

    return clean_df, dq_summary


def load_warehouse_tables(conn, clean_df):
    logging.info("Loading clean data into warehouse tables")

    customers_df = clean_df[["customer_id", "customer_name"]].drop_duplicates()
    products_df = clean_df[["product_id", "product_name", "unit_price"]].drop_duplicates()
    fact_sales_df = clean_df[[
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "unit_price",
        "total_amount",
        "order_date"
    ]]

    customers_df.to_sql("dim_customer", conn, if_exists="append", index=False)
    products_df.to_sql("dim_product", conn, if_exists="append", index=False)
    fact_sales_df.to_sql("fact_sales", conn, if_exists="append", index=False)

    logging.info("Warehouse tables loaded successfully")


def generate_quality_report(dq_summary):
    logging.info("Generating data quality report")

    with open(DQ_REPORT_FILE, "w") as file:
        file.write("Day 17 Data Quality Report\n")
        file.write("==========================\n\n")
        file.write(f"Total raw rows: {dq_summary['total_rows']}\n")
        file.write(f"Duplicate rows found: {dq_summary['duplicate_rows']}\n")
        file.write(f"Rows with missing quantity: {dq_summary['missing_quantity']}\n")
        file.write(f"Rows with invalid price: {dq_summary['invalid_price_rows']}\n")
        file.write(f"Rows with invalid date: {dq_summary['invalid_date_rows']}\n")
        file.write(f"Clean rows loaded to warehouse: {dq_summary['clean_rows_loaded']}\n")
        file.write(f"Rejected rows: {dq_summary['rejected_rows']}\n")

    logging.info("Data quality report generated")


def run_pipeline():
    logging.info("Pipeline started")

    df = extract_data()
    conn = connect_database()

    create_tables(conn)
    load_staging_table(conn, df)

    clean_df, dq_summary = validate_and_clean_data(df)

    load_warehouse_tables(conn, clean_df)
    generate_quality_report(dq_summary)

    conn.close()

    logging.info("Pipeline completed successfully")
    print("Pipeline completed successfully.")
    print(f"Database created at: {DB_FILE}")
    print(f"Data quality report created at: {DQ_REPORT_FILE}")
    print(f"Log file created at: {LOG_FILE}")


if __name__ == "__main__":
    run_pipeline()