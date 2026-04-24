import os
import sqlite3
import pandas as pd
import logging

DB_FILE = "output/sales.db"
OUTPUT_DIR = "output"
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.log")
QUALITY_REPORT_FILE = os.path.join(OUTPUT_DIR, "data_quality_report.txt")


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def run_query(conn, query):
    return pd.read_sql_query(query, conn)


def save_report(df, file_name):
    file_path = os.path.join(OUTPUT_DIR, file_name)
    df.to_csv(file_path, index=False)
    logging.info(f"Saved report: {file_name}")
    print(f"Saved report: {file_path}")


def generate_kpi_summary(conn):
    logging.info("Generating KPI summary report")
    query = """
    SELECT
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS total_customers,
        SUM(quantity) AS total_items_sold,
        ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
        ROUND(AVG(quantity * unit_price), 2) AS average_order_value
    FROM sales;
    """
    return run_query(conn, query)


def generate_revenue_by_category(conn):
    logging.info("Generating revenue by category report")
    query = """
    SELECT
        category,
        SUM(quantity) AS total_quantity_sold,
        ROUND(SUM(quantity * unit_price), 2) AS total_revenue
    FROM sales
    GROUP BY category
    ORDER BY total_revenue DESC;
    """
    return run_query(conn, query)


def generate_top_products(conn):
    logging.info("Generating top products report")
    query = """
    SELECT
        product_name,
        SUM(quantity) AS total_quantity_sold,
        ROUND(SUM(quantity * unit_price), 2) AS total_revenue
    FROM sales
    GROUP BY product_name
    ORDER BY total_revenue DESC
    LIMIT 5;
    """
    return run_query(conn, query)


def generate_sales_by_payment_method(conn):
    logging.info("Generating sales by payment method report")
    query = """
    SELECT
        payment_method,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(quantity * unit_price), 2) AS total_revenue
    FROM sales
    GROUP BY payment_method
    ORDER BY total_revenue DESC;
    """
    return run_query(conn, query)


def generate_data_quality_report(conn):
    logging.info("Starting data quality checks")

    checks = []

    null_query = """
    SELECT COUNT(*) AS null_count
    FROM sales
    WHERE order_id IS NULL
       OR order_date IS NULL
       OR customer_id IS NULL
       OR product_name IS NULL
       OR category IS NULL
       OR quantity IS NULL
       OR unit_price IS NULL
       OR payment_method IS NULL;
    """

    duplicate_query = """
    SELECT COUNT(*) AS duplicate_count
    FROM (
        SELECT order_id, COUNT(*) AS cnt
        FROM sales
        GROUP BY order_id
        HAVING COUNT(*) > 1
    );
    """

    invalid_quantity_query = """
    SELECT COUNT(*) AS invalid_quantity_count
    FROM sales
    WHERE quantity <= 0;
    """

    invalid_price_query = """
    SELECT COUNT(*) AS invalid_price_count
    FROM sales
    WHERE unit_price <= 0;
    """

    null_count = run_query(conn, null_query).iloc[0]["null_count"]
    duplicate_count = run_query(conn, duplicate_query).iloc[0]["duplicate_count"]
    invalid_quantity_count = run_query(conn, invalid_quantity_query).iloc[0]["invalid_quantity_count"]
    invalid_price_count = run_query(conn, invalid_price_query).iloc[0]["invalid_price_count"]

    checks.append("DAY 9 DATA QUALITY REPORT")
    checks.append("-" * 30)
    checks.append(f"Null rows count: {null_count}")
    checks.append(f"Duplicate order_id groups: {duplicate_count}")
    checks.append(f"Rows with invalid quantity: {invalid_quantity_count}")
    checks.append(f"Rows with invalid unit price: {invalid_price_count}")

    if (
        null_count == 0
        and duplicate_count == 0
        and invalid_quantity_count == 0
        and invalid_price_count == 0
    ):
        checks.append("Overall status: PASS")
    else:
        checks.append("Overall status: FAIL")

    with open(QUALITY_REPORT_FILE, "w") as file:
        file.write("\n".join(checks))

    logging.info("Data quality checks completed")
    print(f"Saved report: {QUALITY_REPORT_FILE}")


def main():
    setup_logging()
    logging.info("Day 9 reporting pipeline started")

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        logging.info("Connecting to SQLite database")
        conn = sqlite3.connect(DB_FILE)

        kpi_summary = generate_kpi_summary(conn)
        revenue_by_category = generate_revenue_by_category(conn)
        top_products = generate_top_products(conn)
        sales_by_payment_method = generate_sales_by_payment_method(conn)

        save_report(kpi_summary, "kpi_summary.csv")
        save_report(revenue_by_category, "revenue_by_category.csv")
        save_report(top_products, "top_products.csv")
        save_report(sales_by_payment_method, "sales_by_payment_method.csv")

        generate_data_quality_report(conn)

        conn.close()
        logging.info("Database connection closed")
        logging.info("Day 9 reporting pipeline completed successfully")
        print("Business reporting completed successfully.")

    except Exception as error:
        logging.error(f"Pipeline failed: {error}")
        print(f"Pipeline failed: {error}")


if __name__ == "__main__":
    main()