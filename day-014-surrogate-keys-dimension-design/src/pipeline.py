import os
import sqlite3
import logging
import pandas as pd
from datetime import datetime


INPUT_FILE = "data/customers.csv"
OUTPUT_DIR = "output"
DATABASE_FILE = "output/warehouse.db"
DIM_CUSTOMER_FILE = "output/dim_customer.csv"
DATA_QUALITY_REPORT = "output/data_quality_report.txt"
LOG_FILE = "output/pipeline.log"


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def extract_data(file_path):
    logging.info("Reading customer source data")
    return pd.read_csv(file_path)


def clean_data(df):
    logging.info("Cleaning customer data")

    original_count = len(df)

    df = df.drop_duplicates()

    df["first_name"] = df["first_name"].str.strip().str.title()
    df["last_name"] = df["last_name"].str.strip().str.title()
    df["city"] = df["city"].fillna("Unknown").str.strip().str.title()
    df["state"] = df["state"].fillna("Unknown").str.strip().str.upper()
    df["email"] = df["email"].fillna("unknown@email.com").str.strip().str.lower()

    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")

    cleaned_count = len(df)
    duplicates_removed = original_count - cleaned_count

    return df, duplicates_removed


def validate_data(df):
    logging.info("Validating customer data")

    issues = []

    if df["customer_id"].isnull().any():
        issues.append("Missing customer_id found")

    if df["email"].isnull().any():
        issues.append("Missing email found")

    if df["signup_date"].isnull().any():
        issues.append("Invalid signup_date found")

    if df["customer_id"].duplicated().any():
        issues.append("Duplicate customer_id found after cleaning")

    return issues


def create_customer_dimension(df):
    logging.info("Creating customer dimension table")

    dim_customer = df.copy()

    dim_customer = dim_customer.sort_values(by="customer_id").reset_index(drop=True)

    dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))

    dim_customer["full_name"] = (
        dim_customer["first_name"] + " " + dim_customer["last_name"]
    )

    dim_customer["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dim_customer = dim_customer[
        [
            "customer_key",
            "customer_id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "city",
            "state",
            "signup_date",
            "created_at"
        ]
    ]

    return dim_customer


def load_to_sqlite(dim_customer):
    logging.info("Loading customer dimension table into SQLite")

    conn = sqlite3.connect(DATABASE_FILE)

    dim_customer.to_sql(
        "dim_customer",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()


def save_outputs(dim_customer):
    logging.info("Saving dimension table as CSV")
    dim_customer.to_csv(DIM_CUSTOMER_FILE, index=False)


def create_data_quality_report(source_count, final_count, duplicates_removed, issues):
    logging.info("Creating data quality report")

    with open(DATA_QUALITY_REPORT, "w") as report:
        report.write("Day 14 Data Quality Report\n")
        report.write("==========================\n\n")
        report.write(f"Source record count: {source_count}\n")
        report.write(f"Final dimension record count: {final_count}\n")
        report.write(f"Duplicates removed: {duplicates_removed}\n\n")

        report.write("Validation Issues:\n")

        if issues:
            for issue in issues:
                report.write(f"- {issue}\n")
        else:
            report.write("- No major validation issues found\n")


def run_pipeline():
    setup_logging()

    logging.info("Pipeline started")

    df = extract_data(INPUT_FILE)
    source_count = len(df)

    cleaned_df, duplicates_removed = clean_data(df)
    issues = validate_data(cleaned_df)

    dim_customer = create_customer_dimension(cleaned_df)

    save_outputs(dim_customer)
    load_to_sqlite(dim_customer)

    create_data_quality_report(
        source_count,
        len(dim_customer),
        duplicates_removed,
        issues
    )

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()