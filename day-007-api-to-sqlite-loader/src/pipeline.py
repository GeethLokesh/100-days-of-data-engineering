import os
import requests
import sqlite3
import logging

API_URL = "https://jsonplaceholder.typicode.com/posts"
OUTPUT_DIR = "output"
DB_FILE = os.path.join(OUTPUT_DIR, "api_data.db")
REPORT_FILE = os.path.join(OUTPUT_DIR, "data_quality_report.txt")
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.logging")


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok = True)

    logging.basicConfig(
        filename = LOG_FILE,
        level = logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def fetch_api_data(url):
    logging.info("Fetching data from API")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    logging.info(f"Fetched {len(data)} records from API")
    return data

def validate_record(record):
    errors = []

    if record.get("id") is None:
        errors.append("Missing id")

    if record.get("userId") is None:
        errors.append("Missing userId")

    title = str(record.get("title", "")).strip()
    if not title:
        errors.append("Missing title")

    body = str(record.get("body", "")).strip()
    if not body:
        errors.append("Missing body")

    return errors


def clean_data(records):
    valid_records = []
    invalid_records = []

    for record in records:
        errors = validate_record(record)

        if errors:
            invalid_records.append({
                "record": record,
                "errors": errors
            })
        else:
            cleaned_record = {
                "post_id": int(record["id"]),
                "user_id": int(record["userId"]),
                "title": str(record["title"]).strip(),
                "body": str(record["body"]).strip()
            }
            valid_records.append(cleaned_record)

    logging.info(f"Valid records: {len(valid_records)}")
    logging.info(f"Invalid records: {len(invalid_records)}")

    return valid_records, invalid_records


def create_connection(db_file):
    logging.info("Creating SQLite database connection")
    return sqlite3.connect(db_file)


def create_table(connection):
    logging.info("Creating posts table if it does not exist")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS posts (
        post_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL
    )
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()

def load_data_to_sqlite(connection, records):
    logging.info("Loading data into SQLite table")

    insert_query = """
    INSERT OR REPLACE INTO posts (post_id, user_id, title, body)
    VALUES (?, ?, ?, ?)
    """

    data_to_insert = [
        (record["post_id"], record["user_id"], record["title"], record["body"])
        for record in records
    ]

    cursor = connection.cursor()
    cursor.executemany(insert_query, data_to_insert)
    connection.commit()

    logging.info(f"Inserted or updated {len(records)} records into posts table")


def write_data_quality_report(valid_records, invalid_records):
    logging.info("Writing data quality report")

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("Data Quality Report\n")
        file.write("===================\n\n")
        file.write(f"Total valid records: {len(valid_records)}\n")
        file.write(f"Total invalid records: {len(invalid_records)}\n\n")

        if invalid_records:
            file.write("Invalid Record Details:\n")
            file.write("-----------------------\n")
            for index, item in enumerate(invalid_records, start=1):
                file.write(f"\nRecord {index}:\n")
                file.write(f"Data: {item['record']}\n")
                file.write(f"Errors: {', '.join(item['errors'])}\n")


def main():
    setup_logging()
    logging.info("Pipeline started")

    try:
        raw_data = fetch_api_data(API_URL)
        valid_records, invalid_records = clean_data(raw_data)

        connection = create_connection(DB_FILE)
        create_table(connection)
        load_data_to_sqlite(connection, valid_records)
        write_data_quality_report(valid_records, invalid_records)

        connection.close()

        logging.info("Pipeline completed successfully")
        print("Pipeline executed successfully.")
        print(f"Database created at: {DB_FILE}")
        print(f"Report created at: {REPORT_FILE}")
        print(f"Log created at: {LOG_FILE}")

    except requests.exceptions.RequestException as api_error:
        logging.error(f"API request failed: {api_error}")
        print(f"API request failed: {api_error}")

    except sqlite3.Error as db_error:
        logging.error(f"Database error: {db_error}")
        print(f"Database error: {db_error}")

    except Exception as error:
        logging.error(f"Unexpected error: {error}")
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()

