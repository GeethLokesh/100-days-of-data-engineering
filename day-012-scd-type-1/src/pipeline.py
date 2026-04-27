import os
import sqlite3
import logging
from datetime import datetime

import pandas as pd


INPUT_FILE = "data/customer_updates.csv"
OUTPUT_DIR = "output"
DB_FILE = "output/customer_dimension.db"
REPORT_FILE = "output/data_quality_report.txt"
LOG_FILE = "output/pipeline.log"


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def create_connection():
    logging.info("Creating SQLite database connection")
    return sqlite3.connect(DB_FILE)


def create_customer_dimension_table(conn):
    logging.info("Creating customer dimension table if it does not exist")

    query = """
    CREATE TABLE IF NOT EXISTS dim_customer (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        email TEXT,
        city TEXT,
        phone TEXT,
        updated_at TEXT
    )
    """

    conn.execute(query)
    conn.commit()


def seed_existing_customers(conn):
    logging.info("Seeding existing customer records if table is empty")

    count_query = "SELECT COUNT(*) FROM dim_customer"
    existing_count = conn.execute(count_query).fetchone()[0]

    if existing_count > 0:
        logging.info("Customer dimension already has data. Skipping seed step.")
        return

    existing_customers = [
        (1, "John Smith", "john.old@example.com", "Austin", "999-999-9999", "2026-04-25 09:00:00"),
        (2, "Sarah Lee", "sarah@example.com", "Chicago", "222-333-4444", "2026-04-25 09:00:00"),
        (3, "Michael Brown", "michael@example.com", "Boston", "333-444-5555", "2026-04-25 09:00:00")
    ]

    insert_query = """
    INSERT INTO dim_customer (
        customer_id,
        customer_name,
        email,
        city,
        phone,
        updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """

    conn.executemany(insert_query, existing_customers)
    conn.commit()

    logging.info("Existing customer records inserted successfully")


def extract_data():
    logging.info("Reading incoming customer update file")
    return pd.read_csv(INPUT_FILE)


def validate_data(df):
    logging.info("Running data quality checks")

    total_records = len(df)
    missing_customer_id = df["customer_id"].isnull().sum()
    duplicate_customer_id = df["customer_id"].duplicated().sum()
    missing_email = df["email"].isnull().sum()

    valid_df = df.dropna(subset=["customer_id"])
    valid_df = valid_df.drop_duplicates(subset=["customer_id"], keep="last")

    report = f"""
Data Quality Report
Generated At: {datetime.now()}

Total Incoming Records: {total_records}
Missing Customer ID Records: {missing_customer_id}
Duplicate Customer ID Records: {duplicate_customer_id}
Missing Email Records: {missing_email}
Valid Records Loaded: {len(valid_df)}
"""

    with open(REPORT_FILE, "w") as file:
        file.write(report)

    logging.info("Data quality report created")
    return valid_df


def apply_scd_type_1(conn, df):
    logging.info("Applying SCD Type 1 logic")

    inserted_count = 0
    updated_count = 0

    for _, row in df.iterrows():
        customer_id = int(row["customer_id"])

        existing_query = """
        SELECT customer_id
        FROM dim_customer
        WHERE customer_id = ?
        """

        existing_record = conn.execute(existing_query, (customer_id,)).fetchone()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if existing_record:
            update_query = """
            UPDATE dim_customer
            SET
                customer_name = ?,
                email = ?,
                city = ?,
                phone = ?,
                updated_at = ?
            WHERE customer_id = ?
            """

            conn.execute(
                update_query,
                (
                    row["customer_name"],
                    row["email"],
                    row["city"],
                    row["phone"],
                    current_time,
                    customer_id
                )
            )

            updated_count += 1

        else:
            insert_query = """
            INSERT INTO dim_customer (
                customer_id,
                customer_name,
                email,
                city,
                phone,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """

            conn.execute(
                insert_query,
                (
                    customer_id,
                    row["customer_name"],
                    row["email"],
                    row["city"],
                    row["phone"],
                    current_time
                )
            )

            inserted_count += 1

    conn.commit()

    logging.info(f"SCD Type 1 completed. Inserted: {inserted_count}, Updated: {updated_count}")

    return inserted_count, updated_count


def export_final_dimension(conn):
    logging.info("Exporting final customer dimension table")

    query = """
    SELECT *
    FROM dim_customer
    ORDER BY customer_id
    """

    df = pd.read_sql_query(query, conn)
    df.to_csv("output/final_customer_dimension.csv", index=False)

    logging.info("Final customer dimension exported successfully")


def run_pipeline():
    setup_logging()
    logging.info("Pipeline started")

    conn = create_connection()

    try:
        create_customer_dimension_table(conn)
        seed_existing_customers(conn)

        raw_df = extract_data()
        valid_df = validate_data(raw_df)

        inserted_count, updated_count = apply_scd_type_1(conn, valid_df)

        export_final_dimension(conn)

        logging.info(f"Pipeline completed successfully. Inserted: {inserted_count}, Updated: {updated_count}")

    except Exception as error:
        logging.error(f"Pipeline failed: {error}")
        raise

    finally:
        conn.close()
        logging.info("Database connection closed")


if __name__ == "__main__":
    run_pipeline()