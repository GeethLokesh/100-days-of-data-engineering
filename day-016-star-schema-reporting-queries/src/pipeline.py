import os
import sqlite3
import logging
from datetime import datetime

import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DB_PATH = os.path.join(OUTPUT_DIR, "star_schema_sales.db")
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.log")
VALIDATION_REPORT = os.path.join(OUTPUT_DIR, "query_validation_report.txt")


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def create_sample_data():
    customers = pd.DataFrame(
        [
            [1, "C001", "John Smith", "New York", "East"],
            [2, "C002", "Maria Garcia", "Chicago", "Midwest"],
            [3, "C003", "David Lee", "Seattle", "West"],
            [4, "C004", "Priya Patel", "Austin", "South"],
        ],
        columns=["customer_key", "customer_id", "customer_name", "city", "region"],
    )

    products = pd.DataFrame(
        [
            [1, "P001", "Laptop", "Electronics"],
            [2, "P002", "Desk Chair", "Furniture"],
            [3, "P003", "Monitor", "Electronics"],
            [4, "P004", "Notebook", "Office Supplies"],
        ],
        columns=["product_key", "product_id", "product_name", "category"],
    )

    dates = pd.DataFrame(
        [
            [1, "2026-04-01", 2026, 4, "April"],
            [2, "2026-04-02", 2026, 4, "April"],
            [3, "2026-04-03", 2026, 4, "April"],
            [4, "2026-04-04", 2026, 4, "April"],
        ],
        columns=["date_key", "full_date", "year", "month", "month_name"],
    )

    sales = pd.DataFrame(
        [
            [1, 1, 1, 1, 2, 1200.00],
            [2, 2, 2, 1, 1, 250.00],
            [3, 3, 3, 2, 3, 900.00],
            [4, 4, 4, 3, 10, 50.00],
            [5, 1, 3, 3, 1, 300.00],
            [6, 2, 1, 4, 1, 1200.00],
            [7, 3, 2, 4, 2, 500.00],
        ],
        columns=[
            "sales_key",
            "customer_key",
            "product_key",
            "date_key",
            "quantity",
            "sales_amount",
        ],
    )

    logging.info("Sample dimension and fact data created")
    return customers, products, dates, sales


def load_data_to_sqlite(customers, products, dates, sales):
    conn = sqlite3.connect(DB_PATH)

    customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
    products.to_sql("dim_products", conn, if_exists="replace", index=False)
    dates.to_sql("dim_dates", conn, if_exists="replace", index=False)
    sales.to_sql("fact_sales", conn, if_exists="replace", index=False)

    logging.info("Data loaded into SQLite star schema tables")
    return conn


def run_reporting_queries(conn):
    queries = {
        "sales_by_region": """
            SELECT
                c.region,
                SUM(f.sales_amount) AS total_sales,
                SUM(f.quantity) AS total_quantity,
                COUNT(f.sales_key) AS total_orders
            FROM fact_sales f
            JOIN dim_customers c
                ON f.customer_key = c.customer_key
            GROUP BY c.region
            ORDER BY total_sales DESC;
        """,
        "sales_by_product_category": """
            SELECT
                p.category,
                SUM(f.sales_amount) AS total_sales,
                SUM(f.quantity) AS total_quantity
            FROM fact_sales f
            JOIN dim_products p
                ON f.product_key = p.product_key
            GROUP BY p.category
            ORDER BY total_sales DESC;
        """,
        "daily_sales_report": """
            SELECT
                d.full_date,
                SUM(f.sales_amount) AS daily_sales,
                SUM(f.quantity) AS daily_quantity
            FROM fact_sales f
            JOIN dim_dates d
                ON f.date_key = d.date_key
            GROUP BY d.full_date
            ORDER BY d.full_date;
        """,
        "top_customers": """
            SELECT
                c.customer_id,
                c.customer_name,
                c.region,
                SUM(f.sales_amount) AS total_sales
            FROM fact_sales f
            JOIN dim_customers c
                ON f.customer_key = c.customer_key
            GROUP BY c.customer_id, c.customer_name, c.region
            ORDER BY total_sales DESC
            LIMIT 5;
        """,
    }

    report_results = {}

    for report_name, query in queries.items():
        df = pd.read_sql_query(query, conn)
        output_file = os.path.join(OUTPUT_DIR, f"{report_name}.csv")
        df.to_csv(output_file, index=False)
        report_results[report_name] = df

        logging.info(f"Generated report: {report_name}")

    return report_results


def validate_reports(report_results):
    validation_messages = []

    for report_name, df in report_results.items():
        if df.empty:
            message = f"FAILED: {report_name} returned no records"
            logging.warning(message)
        else:
            message = f"PASSED: {report_name} returned {len(df)} records"
            logging.info(message)

        validation_messages.append(message)

    with open(VALIDATION_REPORT, "w") as file:
        file.write("Query Validation Report\n")
        file.write("=======================\n")
        file.write(f"Generated At: {datetime.now()}\n\n")

        for message in validation_messages:
            file.write(message + "\n")

    logging.info("Query validation report generated")


def run_pipeline():
    setup_logging()
    logging.info("Day 16 star schema reporting pipeline started")

    customers, products, dates, sales = create_sample_data()
    conn = load_data_to_sqlite(customers, products, dates, sales)

    report_results = run_reporting_queries(conn)
    validate_reports(report_results)

    conn.close()

    logging.info("Day 16 star schema reporting pipeline completed successfully")
    print("Pipeline completed successfully.")
    print(f"Reports created in: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_pipeline()