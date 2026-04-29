import os
import logging
from datetime import datetime
import pandas as pd


EXISTING_FILE = "data/existing_customer_history.csv"
INCOMING_FILE = "data/incoming_customers.csv"

OUTPUT_DIR = "output"
FINAL_OUTPUT_FILE = "output/customer_history_scd_type_2.csv"
REPORT_FILE = "output/data_quality_report.txt"
LOG_FILE = "output/pipeline.log"


TRACKED_COLUMNS = [
    "customer_name",
    "email",
    "city",
    "membership_status"
]


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a"
    )


def read_csv_file(file_path):
    logging.info(f"Reading file: {file_path}")
    return pd.read_csv(file_path)


def validate_data(existing_df, incoming_df):
    issues = []

    if existing_df.empty:
        issues.append("Existing customer history file is empty.")

    if incoming_df.empty:
        issues.append("Incoming customer file is empty.")

    existing_required_columns = [
        "customer_id",
        "customer_name",
        "email",
        "city",
        "membership_status",
        "start_date",
        "end_date",
        "is_current"
    ]

    incoming_required_columns = [
        "customer_id",
        "customer_name",
        "email",
        "city",
        "membership_status"
    ]

    for column in existing_required_columns:
        if column not in existing_df.columns:
            issues.append(f"Missing column in existing file: {column}")

    for column in incoming_required_columns:
        if column not in incoming_df.columns:
            issues.append(f"Missing column in incoming file: {column}")

    duplicate_incoming_ids = incoming_df[incoming_df.duplicated(subset=["customer_id"], keep=False)]

    if not duplicate_incoming_ids.empty:
        issues.append("Duplicate customer_id values found in incoming data.")

    return issues


def normalize_boolean_column(df):
    df["is_current"] = df["is_current"].astype(str).str.strip().str.lower()
    df["is_current"] = df["is_current"].map({"true": True, "false": False})
    return df


def has_customer_changed(existing_row, incoming_row):
    for column in TRACKED_COLUMNS:
        existing_value = str(existing_row[column]).strip()
        incoming_value = str(incoming_row[column]).strip()

        if existing_value != incoming_value:
            return True

    return False


def apply_scd_type_2(existing_df, incoming_df):
    today = datetime.today().strftime("%Y-%m-%d")

    existing_df = normalize_boolean_column(existing_df)
    existing_df["end_date"] = existing_df["end_date"].fillna("").astype(str)
    existing_df["start_date"] = existing_df["start_date"].astype(str)

    final_records = existing_df.copy()

    current_records = existing_df[existing_df["is_current"] == True]

    inserted_count = 0
    updated_count = 0
    unchanged_count = 0
    new_customer_count = 0

    for _, incoming_row in incoming_df.iterrows():
        customer_id = incoming_row["customer_id"]

        matching_current_record = current_records[
            current_records["customer_id"] == customer_id
        ]

        if matching_current_record.empty:
            new_record = incoming_row.to_dict()
            new_record["start_date"] = today
            new_record["end_date"] = ""
            new_record["is_current"] = True

            final_records = pd.concat(
                [final_records, pd.DataFrame([new_record])],
                ignore_index=True
            )

            inserted_count += 1
            new_customer_count += 1
            logging.info(f"Inserted new customer record: {customer_id}")

        else:
            existing_row = matching_current_record.iloc[0]

            if has_customer_changed(existing_row, incoming_row):
                final_records.loc[
                    (final_records["customer_id"] == customer_id)
                    & (final_records["is_current"] == True),
                    ["end_date", "is_current"]
                ] = [today, False]

                new_record = incoming_row.to_dict()
                new_record["start_date"] = today
                new_record["end_date"] = ""
                new_record["is_current"] = True

                final_records = pd.concat(
                    [final_records, pd.DataFrame([new_record])],
                    ignore_index=True
                )

                updated_count += 1
                inserted_count += 1
                logging.info(f"SCD Type 2 change detected for customer: {customer_id}")

            else:
                unchanged_count += 1
                logging.info(f"No change found for customer: {customer_id}")

    summary = {
        "inserted_count": inserted_count,
        "updated_count": updated_count,
        "unchanged_count": unchanged_count,
        "new_customer_count": new_customer_count,
        "total_final_records": len(final_records)
    }

    return final_records, summary


def write_output(final_df):
    final_df.to_csv(FINAL_OUTPUT_FILE, index=False)
    logging.info(f"Final SCD Type 2 output written to: {FINAL_OUTPUT_FILE}")


def write_quality_report(validation_issues, summary):
    with open(REPORT_FILE, "w") as report:
        report.write("SCD Type 2 Data Quality Report\n")
        report.write("==============================\n\n")

        report.write("Validation Results:\n")

        if validation_issues:
            for issue in validation_issues:
                report.write(f"- {issue}\n")
        else:
            report.write("- No validation issues found.\n")

        report.write("\nPipeline Summary:\n")
        report.write(f"- New version records inserted: {summary['inserted_count']}\n")
        report.write(f"- Existing customers updated: {summary['updated_count']}\n")
        report.write(f"- Customers unchanged: {summary['unchanged_count']}\n")
        report.write(f"- Brand new customers added: {summary['new_customer_count']}\n")
        report.write(f"- Total final history records: {summary['total_final_records']}\n")

    logging.info(f"Data quality report written to: {REPORT_FILE}")


def run_pipeline():
    setup_logging()
    logging.info("SCD Type 2 pipeline started")

    existing_df = read_csv_file(EXISTING_FILE)
    incoming_df = read_csv_file(INCOMING_FILE)

    validation_issues = validate_data(existing_df, incoming_df)

    if validation_issues:
        logging.warning("Validation issues found")
        summary = {
            "inserted_count": 0,
            "updated_count": 0,
            "unchanged_count": 0,
            "new_customer_count": 0,
            "total_final_records": 0
        }
        write_quality_report(validation_issues, summary)
        return

    final_df, summary = apply_scd_type_2(existing_df, incoming_df)

    write_output(final_df)
    write_quality_report(validation_issues, summary)

    logging.info("SCD Type 2 pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()