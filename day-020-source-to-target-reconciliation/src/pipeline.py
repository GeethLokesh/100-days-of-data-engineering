import pandas as pd
import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = BASE_DIR / "data" / "source_orders.csv"
TARGET_FILE = BASE_DIR / "data" / "target_orders.csv"

OUTPUT_DIR = BASE_DIR / "output"
MATCHED_FILE = OUTPUT_DIR / "matched_records.csv"
MISMATCHED_FILE = OUTPUT_DIR / "mismatched_records.csv"
MISSING_IN_TARGET_FILE = OUTPUT_DIR / "missing_in_target.csv"
EXTRA_IN_TARGET_FILE = OUTPUT_DIR / "extra_in_target.csv"
REPORT_FILE = OUTPUT_DIR / "reconciliation_report.txt"
LOG_FILE = OUTPUT_DIR / "pipeline.log"


def setup_logging():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a"
    )


def read_data():
    logging.info("Reading source and target files")

    source_df = pd.read_csv(SOURCE_FILE)
    target_df = pd.read_csv(TARGET_FILE)

    logging.info(f"Source records loaded: {len(source_df)}")
    logging.info(f"Target records loaded: {len(target_df)}")

    return source_df, target_df


def validate_columns(source_df, target_df):
    logging.info("Validating source and target columns")

    source_columns = set(source_df.columns)
    target_columns = set(target_df.columns)

    if source_columns != target_columns:
        missing_columns = source_columns - target_columns
        extra_columns = target_columns - source_columns

        error_message = (
            f"Column validation failed. "
            f"Missing in target: {missing_columns}. "
            f"Extra in target: {extra_columns}."
        )

        logging.error(error_message)
        raise ValueError(error_message)

    logging.info("Column validation passed")


def reconcile_data(source_df, target_df):
    logging.info("Starting reconciliation process")

    key_column = "order_id"

    merged_df = source_df.merge(
        target_df,
        on=key_column,
        how="outer",
        suffixes=("_source", "_target"),
        indicator=True
    )

    missing_in_target = merged_df[merged_df["_merge"] == "left_only"]
    extra_in_target = merged_df[merged_df["_merge"] == "right_only"]
    common_records = merged_df[merged_df["_merge"] == "both"]

    comparison_columns = [
        "customer_name",
        "product_name",
        "quantity",
        "order_amount",
        "order_status"
    ]

    matched_records = []
    mismatched_records = []

    for _, row in common_records.iterrows():
        mismatch_details = []

        for column in comparison_columns:
            source_value = row[f"{column}_source"]
            target_value = row[f"{column}_target"]

            if source_value != target_value:
                mismatch_details.append(
                    f"{column}: source={source_value}, target={target_value}"
                )

        if mismatch_details:
            record = row.to_dict()
            record["mismatch_details"] = " | ".join(mismatch_details)
            mismatched_records.append(record)
        else:
            matched_records.append(row.to_dict())

    matched_df = pd.DataFrame(matched_records)
    mismatched_df = pd.DataFrame(mismatched_records)

    logging.info(f"Matched records: {len(matched_df)}")
    logging.info(f"Mismatched records: {len(mismatched_df)}")
    logging.info(f"Missing in target: {len(missing_in_target)}")
    logging.info(f"Extra in target: {len(extra_in_target)}")

    return matched_df, mismatched_df, missing_in_target, extra_in_target


def save_outputs(matched_df, mismatched_df, missing_in_target, extra_in_target):
    logging.info("Saving reconciliation output files")

    matched_df.to_csv(MATCHED_FILE, index=False)
    mismatched_df.to_csv(MISMATCHED_FILE, index=False)
    missing_in_target.to_csv(MISSING_IN_TARGET_FILE, index=False)
    extra_in_target.to_csv(EXTRA_IN_TARGET_FILE, index=False)

    logging.info("Output files saved successfully")


def create_report(source_df, target_df, matched_df, mismatched_df, missing_in_target, extra_in_target):
    logging.info("Creating reconciliation report")

    total_source_records = len(source_df)
    total_target_records = len(target_df)
    total_matched_records = len(matched_df)
    total_mismatched_records = len(mismatched_df)
    total_missing_in_target = len(missing_in_target)
    total_extra_in_target = len(extra_in_target)

    reconciliation_status = "PASSED"

    if (
        total_mismatched_records > 0
        or total_missing_in_target > 0
        or total_extra_in_target > 0
        or total_source_records != total_target_records
    ):
        reconciliation_status = "FAILED"

    report_content = f"""
Source-to-Target Reconciliation Report

Reconciliation Status: {reconciliation_status}

Record Count Summary
--------------------
Total Source Records: {total_source_records}
Total Target Records: {total_target_records}
Matched Records: {total_matched_records}
Mismatched Records: {total_mismatched_records}
Missing in Target: {total_missing_in_target}
Extra in Target: {total_extra_in_target}

Validation Checks
-----------------
1. Source and target columns match.
2. Source and target record counts compared.
3. Missing records in target identified.
4. Extra records in target identified.
5. Field-level mismatches identified.

Output Files
------------
matched_records.csv
mismatched_records.csv
missing_in_target.csv
extra_in_target.csv
pipeline.log
"""

    with open(REPORT_FILE, "w") as file:
        file.write(report_content)

    logging.info(f"Reconciliation status: {reconciliation_status}")
    logging.info("Reconciliation report created successfully")


def run_pipeline():
    setup_logging()

    logging.info("Pipeline started")

    source_df, target_df = read_data()

    validate_columns(source_df, target_df)

    matched_df, mismatched_df, missing_in_target, extra_in_target = reconcile_data(
        source_df,
        target_df
    )

    save_outputs(
        matched_df,
        mismatched_df,
        missing_in_target,
        extra_in_target
    )

    create_report(
        source_df,
        target_df,
        matched_df,
        mismatched_df,
        missing_in_target,
        extra_in_target
    )

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()