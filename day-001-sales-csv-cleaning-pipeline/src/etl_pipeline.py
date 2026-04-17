import logging
import os
from datetime import datetime

import pandas as pd

from config import (
    RAW_FILE_PATH,
    CLEAN_FILE_PATH,
    REPORT_FILE_PATH,
    LOG_FILE_PATH
)


def setup_logging():
    os.makedirs("output", exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def extract_data(file_path: str) -> pd.DataFrame:
    logging.info("Starting data extraction from %s", file_path)
    df = pd.read_csv(file_path)
    logging.info("Extracted %s rows", len(df))
    return df


def standardize_date(date_value):
    date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"]

    for fmt in date_formats:
        try:
            return datetime.strptime(str(date_value), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def transform_data(df: pd.DataFrame):
    logging.info("Starting data transformation")

    initial_row_count = len(df)

    df = df.copy()

    df["order_date"] = df["order_date"].apply(standardize_date)
    invalid_date_count = df["order_date"].isna().sum()

    required_columns = ["order_id", "order_date", "customer_name", "product", "quantity", "price"]
    missing_required_count = df[required_columns].isna().any(axis=1).sum()

    duplicate_count = df.duplicated().sum()

    df = df.drop_duplicates()

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    invalid_quantity_count = (df["quantity"].isna() | (df["quantity"] <= 0)).sum()
    invalid_price_count = (df["price"].isna() | (df["price"] <= 0)).sum()

    df = df.dropna(subset=required_columns)
    df = df[df["quantity"] > 0]
    df = df[df["price"] > 0]

    df["total_amount"] = df["quantity"] * df["price"]

    final_row_count = len(df)

    quality_metrics = {
        "initial_row_count": initial_row_count,
        "duplicate_rows_found": int(duplicate_count),
        "rows_with_missing_required_values": int(missing_required_count),
        "rows_with_invalid_dates": int(invalid_date_count),
        "rows_with_invalid_quantity": int(invalid_quantity_count),
        "rows_with_invalid_price": int(invalid_price_count),
        "final_row_count": final_row_count
    }

    logging.info("Transformation complete. Final row count: %s", final_row_count)

    return df, quality_metrics


def load_data(df: pd.DataFrame, file_path: str):
    logging.info("Loading clean data to %s", file_path)
    df.to_csv(file_path, index=False)
    logging.info("Clean data saved successfully")


def write_quality_report(metrics: dict, file_path: str):
    logging.info("Writing data quality report to %s", file_path)

    lines = [
        "DATA QUALITY REPORT",
        "=" * 30,
        f"Initial row count: {metrics['initial_row_count']}",
        f"Duplicate rows found: {metrics['duplicate_rows_found']}",
        f"Rows with missing required values: {metrics['rows_with_missing_required_values']}",
        f"Rows with invalid dates: {metrics['rows_with_invalid_dates']}",
        f"Rows with invalid quantity: {metrics['rows_with_invalid_quantity']}",
        f"Rows with invalid price: {metrics['rows_with_invalid_price']}",
        f"Final clean row count: {metrics['final_row_count']}"
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    logging.info("Data quality report created successfully")


def main():
    setup_logging()
    logging.info("ETL pipeline started")

    try:
        raw_df = extract_data(RAW_FILE_PATH)
        clean_df, metrics = transform_data(raw_df)
        load_data(clean_df, CLEAN_FILE_PATH)
        write_quality_report(metrics, REPORT_FILE_PATH)

        print("ETL pipeline completed successfully.")
        print(f"Clean file saved to: {CLEAN_FILE_PATH}")
        print(f"Quality report saved to: {REPORT_FILE_PATH}")

        logging.info("ETL pipeline finished successfully")

    except Exception as error:
        logging.exception("Pipeline failed due to error: %s", error)
        print(f"Pipeline failed: {error}")


if __name__ == "__main__":
    main()