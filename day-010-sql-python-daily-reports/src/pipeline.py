import os
import sqlite3
import logging
from datetime import datetime

import pandas as pd


INPUT_FILE = "data/sales.csv"
OUTPUT_DIR = "output"
DATABASE_FILE = "output/sales.db"
DAILY_REPORT_FILE = "output/daily_sales_report.txt"
DATA_QUALITY_REPORT_FILE = "output/data_quality_report.txt"
REGION_REPORT_FILE = "output/sales_by_region.csv"


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=f"{OUTPUT_DIR}/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def extract_data():
    logging.info("Reading sales CSV file")

    if not os.path.exists(INPUT_FILE):
        logging.error("Input file not found")
        raise FileNotFoundError(f"{INPUT_FILE} does not exist")

    df = pd.read_csv(INPUT_FILE)
    logging.info(f"CSV file loaded successfully with {len(df)} records")

    return df


def validate_data(df):
    logging.info("Starting data quality checks")

    total_records = len(df)
    duplicate_orders = df.duplicated(subset=["order_id"]).sum()
    missing_values = df.isnull().sum().sum()

    invalid_quantity = len(df[df["quantity"] <= 0])
    invalid_unit_price = len(df[df["unit_price"] <= 0])

    with open(DATA_QUALITY_REPORT_FILE, "w") as file:
        file.write("Data Quality Report\n")
        file.write("===================\n\n")
        file.write(f"Report generated at: {datetime.now()}\n\n")
        file.write(f"Total records checked: {total_records}\n")
        file.write(f"Duplicate order IDs: {duplicate_orders}\n")
        file.write(f"Missing values: {missing_values}\n")
        file.write(f"Invalid quantity records: {invalid_quantity}\n")
        file.write(f"Invalid unit price records: {invalid_unit_price}\n")

    if duplicate_orders > 0 or missing_values > 0 or invalid_quantity > 0 or invalid_unit_price > 0:
        logging.warning("Data quality issues found")
    else:
        logging.info("Data quality checks passed")

    return df


def transform_data(df):
    logging.info("Adding calculated revenue column")

    df["revenue"] = df["quantity"] * df["unit_price"]

    return df


def load_to_sqlite(df):
    logging.info("Loading data into SQLite database")

    connection = sqlite3.connect(DATABASE_FILE)

    df.to_sql(
        "sales",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    logging.info("Data loaded into SQLite table: sales")


def generate_reports():
    logging.info("Generating SQL reports")

    connection = sqlite3.connect(DATABASE_FILE)

    summary_query = """
    SELECT
        COUNT(order_id) AS total_orders,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(AVG(revenue), 2) AS average_order_value
    FROM sales;
    """

    region_query = """
    SELECT
        region,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM sales
    GROUP BY region
    ORDER BY total_revenue DESC;
    """

    product_query = """
    SELECT
        product,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC;
    """

    summary_df = pd.read_sql_query(summary_query, connection)
    region_df = pd.read_sql_query(region_query, connection)
    product_df = pd.read_sql_query(product_query, connection)

    region_df.to_csv(REGION_REPORT_FILE, index=False)

    with open(DAILY_REPORT_FILE, "w") as file:
        file.write("Daily Sales Report\n")
        file.write("==================\n\n")
        file.write(f"Report generated at: {datetime.now()}\n\n")

        file.write("Business Summary\n")
        file.write("----------------\n")
        file.write(f"Total Orders: {summary_df.loc[0, 'total_orders']}\n")
        file.write(f"Total Revenue: ${summary_df.loc[0, 'total_revenue']}\n")
        file.write(f"Average Order Value: ${summary_df.loc[0, 'average_order_value']}\n\n")

        file.write("Sales by Region\n")
        file.write("----------------\n")
        file.write(region_df.to_string(index=False))
        file.write("\n\n")

        file.write("Sales by Product\n")
        file.write("----------------\n")
        file.write(product_df.to_string(index=False))
        file.write("\n")

    connection.close()

    logging.info("Daily sales report generated successfully")


def run_pipeline():
    logging.info("Pipeline started")

    df = extract_data()
    df = validate_data(df)
    df = transform_data(df)
    load_to_sqlite(df)
    generate_reports()

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    setup_logging()
    run_pipeline()