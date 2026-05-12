import json
import logging
import time
from pathlib import Path

import pandas as pd
import requests


BASE_URL = "https://jsonplaceholder.typicode.com/posts"
PAGE_SIZE = 25
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

RAW_OUTPUT_FILE = Path("output/raw_api_posts.json")
CLEAN_OUTPUT_FILE = Path("output/clean_posts.csv")
QUALITY_REPORT_FILE = Path("output/data_quality_report.txt")
LOG_FILE = Path("output/pipeline.log")


def setup_logging():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def fetch_page(start, limit):
    params = {
        "_start": start,
        "_limit": limit
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Fetching records from start={start}, limit={limit}")

            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as error:
            logging.error(f"Attempt {attempt} failed: {error}")

            if attempt < MAX_RETRIES:
                logging.info(f"Retrying after {RETRY_DELAY_SECONDS} seconds")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logging.error("Maximum retry attempts reached")
                raise


def fetch_all_posts():
    all_posts = []
    start = 0

    while True:
        page_data = fetch_page(start, PAGE_SIZE)

        if not page_data:
            logging.info("No more records found. Pagination completed.")
            break

        all_posts.extend(page_data)
        logging.info(f"Fetched {len(page_data)} records")

        start += PAGE_SIZE

    return all_posts


def save_raw_data(posts):
    RAW_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(RAW_OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4)

    logging.info(f"Raw data saved to {RAW_OUTPUT_FILE}")


def clean_and_validate_data(posts):
    df = pd.DataFrame(posts)

    total_records = len(df)

    required_columns = ["userId", "id", "title", "body"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    duplicate_count = df.duplicated(subset=["id"]).sum()

    missing_user_id = df["userId"].isna().sum()
    missing_id = df["id"].isna().sum()
    missing_title = df["title"].isna().sum()
    missing_body = df["body"].isna().sum()

    df = df.drop_duplicates(subset=["id"])
    df = df.dropna(subset=required_columns)

    df["title"] = df["title"].str.strip()
    df["body"] = df["body"].str.strip()

    clean_records = len(df)

    quality_summary = {
        "total_records_received": total_records,
        "duplicate_records_removed": int(duplicate_count),
        "missing_userId_count": int(missing_user_id),
        "missing_id_count": int(missing_id),
        "missing_title_count": int(missing_title),
        "missing_body_count": int(missing_body),
        "clean_records_saved": clean_records
    }

    return df, quality_summary


def save_clean_data(df):
    df.to_csv(CLEAN_OUTPUT_FILE, index=False)
    logging.info(f"Clean data saved to {CLEAN_OUTPUT_FILE}")


def save_quality_report(summary):
    with open(QUALITY_REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("Day 21 Data Quality Report\n")
        file.write("==========================\n\n")

        for key, value in summary.items():
            file.write(f"{key}: {value}\n")

    logging.info(f"Data quality report saved to {QUALITY_REPORT_FILE}")


def run_pipeline():
    setup_logging()

    logging.info("Pipeline started")

    posts = fetch_all_posts()
    save_raw_data(posts)

    clean_df, quality_summary = clean_and_validate_data(posts)

    save_clean_data(clean_df)
    save_quality_report(quality_summary)

    logging.info("Pipeline completed successfully")

    print("Pipeline completed successfully")
    print(f"Raw data saved to: {RAW_OUTPUT_FILE}")
    print(f"Clean data saved to: {CLEAN_OUTPUT_FILE}")
    print(f"Data quality report saved to: {QUALITY_REPORT_FILE}")


if __name__ == "__main__":
    run_pipeline()