import os
import json
import logging
from datetime import datetime
import pandas as pd


CSV_FILE = "data/customer_products.csv"
JSON_FILE = "data/orders.json"
OUTPUT_DIR = "output"

MERGED_FILE = os.path.join(OUTPUT_DIR, "merged_output.csv")
REPORT_FILE = os.path.join(OUTPUT_DIR, "data_quality_report.txt")
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.log")


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def standardize_text(value):
    if pd.isna(value):
        return None
    return str(value).strip().lower()


def standardize_date(date_value):
    if pd.isna(date_value):
        return None

    date_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y"
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(str(date_value).strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def load_csv(file_path):
    logging.info("Loading CSV file")
    return pd.read_csv(file_path)


def load_json(file_path):
    logging.info("Loading JSON file")
    with open(file_path, "r") as file:
        data = json.load(file)
    return pd.DataFrame(data)


def clean_csv_data(df):
    logging.info("Cleaning CSV data")

    original_count = len(df)

    df.columns = df.columns.str.strip().str.lower()
    df = df.drop_duplicates()

    df["customer_id"] = df["customer_id"].apply(standardize_text)
    df["product_name"] = df["product_name"].apply(standardize_text)
    df["purchase_date"] = df["purchase_date"].apply(standardize_date)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df = df.dropna(subset=["customer_id", "product_name", "purchase_date", "quantity"])

    cleaned_count = len(df)
    dropped_count = original_count - cleaned_count

    return df, dropped_count


def clean_json_data(df):
    logging.info("Cleaning JSON data")

    original_count = len(df)

    df.columns = df.columns.str.strip().str.lower()
    df = df.drop_duplicates()

    df["customer_id"] = df["customer_id"].apply(standardize_text)
    df["product_name"] = df["product_name"].apply(standardize_text)
    df["order_date"] = df["order_date"].apply(standardize_date)

    df["order_amount"] = pd.to_numeric(df["order_amount"], errors="coerce")

    df = df.dropna(subset=["customer_id", "product_name", "order_date", "order_amount"])

    cleaned_count = len(df)
    dropped_count = original_count - cleaned_count

    return df, dropped_count


def merge_datasets(csv_df, json_df):
    logging.info("Merging CSV and JSON datasets")

    unmatched_csv = csv_df.merge(
        json_df,
        on=["customer_id", "product_name"],
        how="left",
        indicator=True
    )
    unmatched_csv_count = len(unmatched_csv[unmatched_csv["_merge"] == "left_only"])

    unmatched_json = json_df.merge(
        csv_df,
        on=["customer_id", "product_name"],
        how="left",
        indicator=True
    )
    unmatched_json_count = len(unmatched_json[unmatched_json["_merge"] == "left_only"])

    merged_df = pd.merge(
        csv_df,
        json_df,
        on=["customer_id", "product_name"],
        how="inner"
    )

    return merged_df, unmatched_csv_count, unmatched_json_count


def save_output(df, output_file):
    logging.info("Saving merged output file")
    df.to_csv(output_file, index=False)


def generate_data_quality_report(
    csv_input_count,
    json_input_count,
    csv_dropped_count,
    json_dropped_count,
    unmatched_csv_count,
    unmatched_json_count,
    merged_count
):
    logging.info("Generating data quality report")

    report_lines = [
        "DATA QUALITY REPORT",
        "-------------------",
        f"CSV input rows: {csv_input_count}",
        f"JSON input rows: {json_input_count}",
        f"CSV rows dropped during cleaning: {csv_dropped_count}",
        f"JSON rows dropped during cleaning: {json_dropped_count}",
        f"CSV rows without match in JSON: {unmatched_csv_count}",
        f"JSON rows without match in CSV: {unmatched_json_count}",
        f"Final merged rows: {merged_count}"
    ]

    with open(REPORT_FILE, "w") as file:
        file.write("\n".join(report_lines))


def main():
    setup_logging()
    logging.info("Pipeline started")

    csv_df = load_csv(CSV_FILE)
    json_df = load_json(JSON_FILE)

    csv_input_count = len(csv_df)
    json_input_count = len(json_df)

    cleaned_csv_df, csv_dropped_count = clean_csv_data(csv_df)
    cleaned_json_df, json_dropped_count = clean_json_data(json_df)

    merged_df, unmatched_csv_count, unmatched_json_count = merge_datasets(
        cleaned_csv_df,
        cleaned_json_df
    )

    save_output(merged_df, MERGED_FILE)

    generate_data_quality_report(
        csv_input_count,
        json_input_count,
        csv_dropped_count,
        json_dropped_count,
        unmatched_csv_count,
        unmatched_json_count,
        len(merged_df)
    )

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()