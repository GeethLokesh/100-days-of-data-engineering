import csv
import json
import logging
import os
from datetime import datetime


INPUT_FILE = "data/sales.csv"
OUTPUT_FILE = "output/sales.json"
REPORT_FILE = "output/data_quality_report.txt"


def setup_logging():
    os.makedirs("output", exist_ok=True)

    logging.basicConfig(
        filename="output/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def standardize_date(date_value):
    if not date_value:
        return None

    formats = ["%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"]

    for fmt in formats:
        try:
            return datetime.strptime(date_value, fmt).strftime("%Y-%m-%d")
        except:
            continue

    return None


def clean_row(row):
    return {
        "order_id": int(row["order_id"]),
        "customer_name": row["customer_name"] or "unknown",
        "order_date": standardize_date(row["order_date"]),
        "amount": float(row["amount"]) if row["amount"] else 0,
        "status": row["status"].lower()
    }


def process_data():
    cleaned_data = []

    total_rows = 0
    missing_names = 0
    invalid_dates = 0

    with open(INPUT_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1

            if not row["customer_name"]:
                missing_names += 1

            if not standardize_date(row["order_date"]):
                invalid_dates += 1

            cleaned_data.append(clean_row(row))

    return cleaned_data, total_rows, missing_names, invalid_dates


def write_json(data):
    with open(OUTPUT_FILE, "w") as file:
        json.dump(data, file, indent=4)


def write_report(total, missing_names, invalid_dates):
    with open(REPORT_FILE, "w") as file:
        file.write("DATA QUALITY REPORT\n")
        file.write(f"Total Rows: {total}\n")
        file.write(f"Missing Customer Names: {missing_names}\n")
        file.write(f"Invalid Dates: {invalid_dates}\n")


def run_pipeline():
    try:
        setup_logging()

        data, total, missing, invalid = process_data()

        write_json(data)
        write_report(total, missing, invalid)

        logging.info("CSV to JSON pipeline completed successfully")

        print("CSV to JSON conversion completed successfully.")
        print(f"Cleaned file saved to: {OUTPUT_FILE}")
        print(f"Report saved to: {REPORT_FILE}")

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        print("Pipeline failed. Check logs for details.")


if __name__ == "__main__":
    run_pipeline()