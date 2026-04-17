import json
import logging
import os
from datetime import datetime


INPUT_FILE = "data/raw_orders.json"
CLEANED_OUTPUT_FILE = "output/cleaned_orders.json"
REPORT_FILE = "output/data_quality_report.txt"


def setup_logging():
    os.makedirs("output", exist_ok=True)

    logging.basicConfig(
        filename="output/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def standardize_date(date_value):
    date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"]

    for fmt in date_formats:
        try:
            return datetime.strptime(str(date_value), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def standardize_status(status_value):
    if not status_value:
        return "unknown"

    status = str(status_value).strip().lower()

    allowed_statuses = {
        "completed": "completed",
        "pending": "pending",
        "cancelled": "cancelled"
    }

    return allowed_statuses.get(status, "unknown")


def clean_text(value):
    if value is None:
        return None

    cleaned = str(value).strip()

    if cleaned == "":
        return None

    return cleaned.title()


def clean_amount(amount_value):
    try:
        amount = float(amount_value)
        if amount < 0:
            return None
        return round(amount, 2)
    except (ValueError, TypeError):
        return None


def process_orders(raw_orders):
    cleaned_orders = []

    total_records = len(raw_orders)
    valid_records = 0
    invalid_records = 0

    logging.info(f"Processing {total_records} records")

    for order in raw_orders:
        cleaned_order = {
            "order_id": str(order.get("order_id", "")).strip(),
            "customer_name": clean_text(order.get("customer_name")),
            "product": clean_text(order.get("product")),
            "amount": clean_amount(order.get("amount")),
            "order_date": standardize_date(order.get("order_date")),
            "status": standardize_status(order.get("status"))
        }

        if (
            cleaned_order["order_id"]
            and cleaned_order["customer_name"]
            and cleaned_order["product"]
            and cleaned_order["amount"] is not None
            and cleaned_order["order_date"]
        ):
            cleaned_orders.append(cleaned_order)
            valid_records += 1
        else:
            invalid_records += 1
            logging.warning(f"Invalid record skipped: {order}")

    logging.info(f"Valid records: {valid_records}")
    logging.info(f"Invalid records: {invalid_records}")

    report = {
        "total_records": total_records,
        "valid_records": valid_records,
        "invalid_records": invalid_records
    }

    return cleaned_orders, report


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    logging.info(f"Cleaned data saved to {file_path}")


def save_report(report, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("JSON Data Quality Report\n")
        file.write("========================\n")
        file.write(f"Total records: {report['total_records']}\n")
        file.write(f"Valid records: {report['valid_records']}\n")
        file.write(f"Invalid records: {report['invalid_records']}\n")

    logging.info(f"Report saved to {file_path}")


def main():
    setup_logging()

    try:
        logging.info("Pipeline started")

        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            raw_orders = json.load(file)

        logging.info("Input file read successfully")

        cleaned_orders, report = process_orders(raw_orders)

        save_json(cleaned_orders, CLEANED_OUTPUT_FILE)
        save_report(report, REPORT_FILE)

        logging.info("Pipeline completed successfully")

        print("JSON ETL pipeline completed successfully.")
        print(f"Cleaned file saved to: {CLEANED_OUTPUT_FILE}")
        print(f"Report saved to: {REPORT_FILE}")

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        print("Pipeline failed. Check logs for details.")


if __name__ == "__main__":
    main()