import os
import sqlite3
import logging
from datetime import datetime
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(BASE_DIR, "data", "daily_sales.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DB_FILE = os.path.join(OUTPUT_DIR, "sales_warehouse.db")
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.log")
REPORT_FILE = os.path.join(OUTPUT_DIR, "data_quality_report.txt")


os.makedirs(OUTPUT_DIR, exist_ok=True)


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def create_batch_id():
    return datetime.now().strftime("BATCH_%Y%m%d_%H%M%S")


def connect_database():
    return sqlite3.connect(DB_FILE)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_fact (
            sale_id TEXT PRIMARY KEY,
            customer_id TEXT,
            product_name TEXT,
            sale_amount REAL,
            sale_date TEXT,
            batch_id TEXT,
            loaded_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batch_audit (
            batch_id TEXT PRIMARY KEY,
            source_file TEXT,
            records_received INTEGER,
            duplicates_in_batch INTEGER,
            records_loaded INTEGER,
            records_skipped INTEGER,
            status TEXT,
            started_at TEXT,
            completed_at TEXT
        )
    """)

    conn.commit()


def extract_data():
    logging.info("Extracting data from CSV file")

    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Input file not found: {DATA_FILE}")

    return pd.read_csv(DATA_FILE)


def clean_data(df):
    logging.info("Cleaning data")

    df = df.copy()

    df["sale_id"] = df["sale_id"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["sale_amount"] = pd.to_numeric(df["sale_amount"], errors="coerce")
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    df = df.dropna(subset=["sale_id", "customer_id", "product_name", "sale_amount", "sale_date"])

    return df


def remove_batch_duplicates(df):
    logging.info("Removing duplicate records from incoming batch")

    records_before = len(df)

    df = df.drop_duplicates(subset=["sale_id"], keep="first")

    records_after = len(df)
    duplicate_count = records_before - records_after

    return df, duplicate_count


def get_existing_sale_ids(conn):
    query = "SELECT sale_id FROM sales_fact"
    existing_df = pd.read_sql_query(query, conn)

    if existing_df.empty:
        return set()

    return set(existing_df["sale_id"].tolist())


def load_incremental_data(conn, df, batch_id):
    logging.info("Loading only new records into sales_fact table")

    existing_sale_ids = get_existing_sale_ids(conn)

    new_records_df = df[~df["sale_id"].isin(existing_sale_ids)].copy()
    skipped_records = len(df) - len(new_records_df)

    if not new_records_df.empty:
        new_records_df["batch_id"] = batch_id
        new_records_df["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_records_df.to_sql(
            "sales_fact",
            conn,
            if_exists="append",
            index=False
        )

    conn.commit()

    return len(new_records_df), skipped_records


def insert_batch_audit(
    conn,
    batch_id,
    records_received,
    duplicates_in_batch,
    records_loaded,
    records_skipped,
    status,
    started_at,
    completed_at
):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO batch_audit (
            batch_id,
            source_file,
            records_received,
            duplicates_in_batch,
            records_loaded,
            records_skipped,
            status,
            started_at,
            completed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        batch_id,
        DATA_FILE,
        records_received,
        duplicates_in_batch,
        records_loaded,
        records_skipped,
        status,
        started_at,
        completed_at
    ))

    conn.commit()


def generate_quality_report(
    batch_id,
    records_received,
    duplicates_in_batch,
    records_loaded,
    records_skipped,
    status
):
    logging.info("Generating data quality report")

    with open(REPORT_FILE, "w") as file:
        file.write("Day 19 Data Quality Report\n")
        file.write("==========================\n\n")
        file.write(f"Batch ID: {batch_id}\n")
        file.write(f"Records received: {records_received}\n")
        file.write(f"Duplicates found inside batch: {duplicates_in_batch}\n")
        file.write(f"New records loaded: {records_loaded}\n")
        file.write(f"Existing records skipped: {records_skipped}\n")
        file.write(f"Pipeline status: {status}\n")


def run_pipeline():
    batch_id = create_batch_id()
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = None

    try:
        logging.info(f"Pipeline started with batch_id: {batch_id}")

        conn = connect_database()
        create_tables(conn)

        raw_df = extract_data()
        records_received = len(raw_df)

        cleaned_df = clean_data(raw_df)

        deduped_df, duplicates_in_batch = remove_batch_duplicates(cleaned_df)

        records_loaded, records_skipped = load_incremental_data(conn, deduped_df, batch_id)

        status = "SUCCESS"
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_batch_audit(
            conn,
            batch_id,
            records_received,
            duplicates_in_batch,
            records_loaded,
            records_skipped,
            status,
            started_at,
            completed_at
        )

        generate_quality_report(
            batch_id,
            records_received,
            duplicates_in_batch,
            records_loaded,
            records_skipped,
            status
        )

        logging.info(f"Pipeline completed successfully for batch_id: {batch_id}")

    except Exception as error:
        status = "FAILED"
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logging.error(f"Pipeline failed for batch_id {batch_id}: {error}")

        if conn:
            insert_batch_audit(
                conn,
                batch_id,
                0,
                0,
                0,
                0,
                status,
                started_at,
                completed_at
            )

        raise

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    run_pipeline()