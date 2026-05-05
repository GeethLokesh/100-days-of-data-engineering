import os
import sqlite3
import logging
from datetime import datetime

import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(BASE_DIR, "data", "raw_sales.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DB_FILE = os.path.join(OUTPUT_DIR, "warehouse.db")
REPORT_FILE = os.path.join(OUTPUT_DIR, "sales_summary.csv")
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.log")


os.makedirs(OUTPUT_DIR, exist_ok=True)


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def connect_to_database():
    return sqlite3.connect(DB_FILE)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staging_sales (
            order_id INTEGER,
            customer_id TEXT,
            product TEXT,
            quantity INTEGER,
            price REAL,
            order_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warehouse_sales (
            order_id INTEGER PRIMARY KEY,
            customer_id TEXT,
            product TEXT,
            quantity INTEGER,
            price REAL,
            total_amount REAL,
            order_date TEXT,
            loaded_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_loads (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pipeline_name TEXT,
            start_time TEXT,
            end_time TEXT,
            status TEXT,
            extracted_rows INTEGER,
            loaded_rows INTEGER,
            rejected_rows INTEGER,
            error_message TEXT
        )
    """)

    conn.commit()


def start_audit_record(conn, pipeline_name):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_loads (
            pipeline_name,
            start_time,
            status,
            extracted_rows,
            loaded_rows,
            rejected_rows,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        pipeline_name,
        start_time,
        "RUNNING",
        0,
        0,
        0,
        None
    ))

    conn.commit()
    return cursor.lastrowid


def update_audit_record(
    conn,
    audit_id,
    status,
    extracted_rows,
    loaded_rows,
    rejected_rows,
    error_message=None
):
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE audit_loads
        SET
            end_time = ?,
            status = ?,
            extracted_rows = ?,
            loaded_rows = ?,
            rejected_rows = ?,
            error_message = ?
        WHERE audit_id = ?
    """, (
        end_time,
        status,
        extracted_rows,
        loaded_rows,
        rejected_rows,
        error_message,
        audit_id
    ))

    conn.commit()


def extract_data():
    logging.info("Extracting raw sales data")
    df = pd.read_csv(DATA_FILE)
    return df


def clean_and_validate_data(df):
    logging.info("Cleaning and validating sales data")

    extracted_rows = len(df)

    df = df.drop_duplicates()

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    valid_df = df.dropna(subset=[
        "order_id",
        "customer_id",
        "product",
        "quantity",
        "price",
        "order_date"
    ]).copy()

    valid_df["order_id"] = valid_df["order_id"].astype(int)
    valid_df["quantity"] = valid_df["quantity"].astype(int)
    valid_df["price"] = valid_df["price"].astype(float)
    valid_df["order_date"] = valid_df["order_date"].dt.strftime("%Y-%m-%d")

    rejected_rows = extracted_rows - len(valid_df)

    return valid_df, extracted_rows, rejected_rows


def load_to_staging(conn, df):
    logging.info("Loading clean data into staging_sales table")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM staging_sales")

    df.to_sql(
        "staging_sales",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()


def load_to_warehouse(conn):
    logging.info("Loading data from staging table into warehouse table")

    loaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO warehouse_sales (
            order_id,
            customer_id,
            product,
            quantity,
            price,
            total_amount,
            order_date,
            loaded_at
        )
        SELECT
            order_id,
            customer_id,
            product,
            quantity,
            price,
            quantity * price AS total_amount,
            order_date,
            ? AS loaded_at
        FROM staging_sales
    """, (loaded_at,))

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM staging_sales")
    loaded_rows = cursor.fetchone()[0]

    return loaded_rows


def generate_sales_summary(conn):
    logging.info("Generating sales summary report")

    query = """
        SELECT
            product,
            COUNT(order_id) AS total_orders,
            SUM(quantity) AS total_quantity,
            SUM(total_amount) AS total_sales
        FROM warehouse_sales
        GROUP BY product
        ORDER BY total_sales DESC
    """

    summary_df = pd.read_sql_query(query, conn)
    summary_df.to_csv(REPORT_FILE, index=False)


def run_pipeline():
    pipeline_name = "day_018_warehouse_etl_audit_load_tracking"
    conn = connect_to_database()

    create_tables(conn)
    audit_id = start_audit_record(conn, pipeline_name)

    extracted_rows = 0
    loaded_rows = 0
    rejected_rows = 0

    try:
        logging.info("Pipeline started")

        raw_df = extract_data()
        clean_df, extracted_rows, rejected_rows = clean_and_validate_data(raw_df)

        load_to_staging(conn, clean_df)
        loaded_rows = load_to_warehouse(conn)

        generate_sales_summary(conn)

        update_audit_record(
            conn=conn,
            audit_id=audit_id,
            status="SUCCESS",
            extracted_rows=extracted_rows,
            loaded_rows=loaded_rows,
            rejected_rows=rejected_rows
        )

        logging.info("Pipeline completed successfully")

    except Exception as error:
        logging.error(f"Pipeline failed: {error}")

        update_audit_record(
            conn=conn,
            audit_id=audit_id,
            status="FAILED",
            extracted_rows=extracted_rows,
            loaded_rows=loaded_rows,
            rejected_rows=rejected_rows,
            error_message=str(error)
        )

    finally:
        conn.close()


if __name__ == "__main__":
    run_pipeline()