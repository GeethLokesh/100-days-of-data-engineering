import os
import sqlite3
import logging
from datetime import datetime

import pandas as pd


INPUT_FILE = "data/orders.csv"
OUTPUT_DIR = "output"
DB_FILE = "output/incremental_load.db"
REPORT_FILE = "output/data_quality_report.txt"
LOG_FILE = "output/pipeline.log"


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a"
    )


def connect_database():
    return sqlite3.connect(DB_FILE)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            product TEXT,
            quantity INTEGER,
            price REAL,
            order_date TEXT,
            last_updated TEXT,
            loaded_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_watermark (
            pipeline_name TEXT PRIMARY KEY,
            last_loaded_timestamp TEXT
        )
    """)

    conn.commit()
    logging.info("Database tables created or already exist")


def get_last_watermark(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT last_loaded_timestamp
        FROM pipeline_watermark
        WHERE pipeline_name = 'orders_incremental_load'
    """)

    result = cursor.fetchone()

    if result:
        logging.info(f"Last watermark found: {result[0]}")
        return result[0]

    default_watermark = "1900-01-01 00:00:00"
    logging.info("No watermark found. Using default watermark")
    return default_watermark


def read_source_data():
    logging.info("Reading source CSV file")
    return pd.read_csv(INPUT_FILE)


def clean_data(df):
    logging.info("Cleaning source data")

    initial_count = len(df)

    df = df.drop_duplicates(subset=["order_id"])

    df["customer_name"] = df["customer_name"].astype(str).str.strip()
    df["product"] = df["product"].astype(str).str.strip()
    
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

    df = df.dropna(subset=[
        "order_id",
        "customer_name",
        "product",
        "quantity",
        "price",
        "order_date",
        "last_updated"
    ])

    df = df[(df["quantity"] > 0) & (df["price"] > 0)]

    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
    df["last_updated"] = df["last_updated"].dt.strftime("%Y-%m-%d %H:%M:%S")

    final_count = len(df)
    rejected_count = initial_count - final_count

    logging.info(f"Initial records: {initial_count}")
    logging.info(f"Clean records: {final_count}")
    logging.info(f"Rejected records: {rejected_count}")

    return df, initial_count, final_count, rejected_count


def filter_incremental_records(df, last_watermark):
    logging.info("Filtering records for incremental load")

    df["last_updated_datetime"] = pd.to_datetime(df["last_updated"])
    watermark_datetime = pd.to_datetime(last_watermark)

    incremental_df = df[df["last_updated_datetime"] > watermark_datetime].copy()

    incremental_df = incremental_df.drop(columns=["last_updated_datetime"])

    logging.info(f"New records found: {len(incremental_df)}")

    return incremental_df


def load_incremental_data(conn, df):
    if df.empty:
        logging.info("No new records to load")
        return 0

    df["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    records = []

    for _, row in df.iterrows():
        records.append((
            int(row["order_id"]),
            str(row["customer_name"]),
            str(row["product"]),
            int(row["quantity"]),
            float(row["price"]),
            str(row["order_date"]),
            str(row["last_updated"]),
            str(row["loaded_at"])
        ))

    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO orders (
            order_id,
            customer_name,
            product,
            quantity,
            price,
            order_date,
            last_updated,
            loaded_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    conn.commit()

    loaded_count = cursor.rowcount
    logging.info(f"Records loaded into database: {loaded_count}")

    return loaded_count


def update_watermark(conn, df):
    if df.empty:
        logging.info("Watermark not updated because no new records were loaded")
        return

    new_watermark = df["last_updated"].max()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pipeline_watermark (
            pipeline_name,
            last_loaded_timestamp
        )
        VALUES (?, ?)
        ON CONFLICT(pipeline_name)
        DO UPDATE SET last_loaded_timestamp = excluded.last_loaded_timestamp
    """, ("orders_incremental_load", new_watermark))

    conn.commit()

    logging.info(f"Watermark updated to: {new_watermark}")


def write_data_quality_report(initial_count, clean_count, rejected_count, new_records_count, loaded_count):
    with open(REPORT_FILE, "w") as report:
        report.write("Data Quality Report\n")
        report.write("===================\n\n")
        report.write(f"Report generated at: {datetime.now()}\n\n")
        report.write(f"Source records read: {initial_count}\n")
        report.write(f"Clean records after validation: {clean_count}\n")
        report.write(f"Rejected records: {rejected_count}\n")
        report.write(f"New records identified for incremental load: {new_records_count}\n")
        report.write(f"Records loaded into database: {loaded_count}\n\n")

        if rejected_count == 0:
            report.write("Data quality status: PASSED\n")
        else:
            report.write("Data quality status: REVIEW NEEDED\n")

    logging.info("Data quality report generated")


def run_pipeline():
    setup_logging()
    logging.info("Incremental data loading pipeline started")

    conn = connect_database()

    try:
        create_tables(conn)

        last_watermark = get_last_watermark(conn)

        source_df = read_source_data()

        clean_df, initial_count, clean_count, rejected_count = clean_data(source_df)

        incremental_df = filter_incremental_records(clean_df, last_watermark)

        loaded_count = load_incremental_data(conn, incremental_df)

        update_watermark(conn, incremental_df)

        write_data_quality_report(
            initial_count,
            clean_count,
            rejected_count,
            len(incremental_df),
            loaded_count
        )

        logging.info("Incremental data loading pipeline completed successfully")

    except Exception as error:
        logging.error(f"Pipeline failed: {error}")
        raise

    finally:
        conn.close()
        logging.info("Database connection closed")


if __name__ == "__main__":
    run_pipeline()