import requests
import pandas as pd
import logging
import os
import json
from datetime import datetime


API_URL = "https://jsonplaceholder.typicode.com/posts"

RAW_FILE = "data/raw_api_data.json"
OUTPUT_FILE = "output/cleaned_data.csv"
REPORT_FILE = "output/data_quality_report.txt"


def setup_logging():
    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    logging.basicConfig(
        filename="output/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


# STEP 1: FETCH DATA FROM API
def fetch_api_data(url):
    logging.info("Fetching data from API")

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Save raw data
            with open(RAW_FILE, "w") as file:
                json.dump(data, file, indent=4)

            return data

        else:
            logging.error(f"API failed with status: {response.status_code}")
            return []

    except Exception as e:
        logging.error(f"API error: {e}")
        return []


# STEP 2: STANDARDIZE DATE
def standardize_date(date_value):
    if not date_value:
        return None

    formats = ["%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"]

    for fmt in formats:
        try:
            return datetime.strptime(str(date_value), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


# STEP 3: CLEAN DATA
def clean_data(data):
    logging.info("Cleaning data")

    df = pd.DataFrame(data)

    if df.empty:
        return df

    # Rename columns to clear English names
    df.rename(columns={
        "userId": "user_id",
        "id": "post_id",
        "title": "post_title",
        "body": "post_description"
    }, inplace=True)

    # Handle missing values
    df["post_title"] = df["post_title"].fillna("unknown")
    df["post_description"] = df["post_description"].fillna("unknown")

    # Add ingestion timestamp
    df["created_at"] = datetime.now().strftime("%Y-%m-%d")
    df["created_at"] = df["created_at"].apply(standardize_date)

    # Remove duplicates
    df = df.drop_duplicates()

    return df


# STEP 4: DATA QUALITY REPORT
def data_quality_report(df):
    logging.info("Generating data quality report")

    total_rows = len(df)
    null_counts = df.isnull().sum()

    with open(REPORT_FILE, "w") as file:
        file.write(f"Total Rows: {total_rows}\n\n")
        file.write("Null Counts:\n")

        for column, count in null_counts.items():
            file.write(f"{column}: {count}\n")


# STEP 5: SAVE CLEAN DATA
def save_data(df):
    logging.info("Saving cleaned data")
    df.to_csv(OUTPUT_FILE, index=False)


# MAIN PIPELINE
def run_pipeline():
    setup_logging()

    raw_data = fetch_api_data(API_URL)

    if not raw_data:
        logging.error("No data fetched. Exiting.")
        return

    cleaned_df = clean_data(raw_data)

    if cleaned_df.empty:
        logging.error("Cleaned data is empty. Exiting.")
        return

    save_data(cleaned_df)
    data_quality_report(cleaned_df)

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()