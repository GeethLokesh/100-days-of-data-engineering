import os
import sqlite3
import logging
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CUSTOMERS_FILE = os.path.join(BASE_DIR, "data", "customers.csv")
PRODUCTS_FILE = os.path.join(BASE_DIR, "data", "products.csv")
SALES_FILE = os.path.join(BASE_DIR, "data", "sales.csv")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DATABASE_FILE = os.path.join(OUTPUT_DIR, "warehouse.db")
REPORT_FILE = os.path.join(OUTPUT_DIR, "data_quality_report.txt")
LOG_FILE = os.path.join(OUTPUT_DIR, "pipeline.log")

OUTPUT_DIR = "output"
DATABASE_FILE = "output/warehouse.db"
REPORT_FILE = "output/data_quality_report.txt"
LOG_FILE = "output/pipeline.log"


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def extract_data():
    logging.info("Reading source CSV files")

    customers_df = pd.read_csv(CUSTOMERS_FILE)
    products_df = pd.read_csv(PRODUCTS_FILE)
    sales_df = pd.read_csv(SALES_FILE)

    return customers_df, products_df, sales_df


def create_customer_dimension(customers_df):
    logging.info("Creating customer dimension table")

    dim_customer = customers_df.drop_duplicates(subset=["customer_id"]).copy()
    dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))

    return dim_customer


def create_product_dimension(products_df):
    logging.info("Creating product dimension table")

    dim_product = products_df.drop_duplicates(subset=["product_id"]).copy()
    dim_product.insert(0, "product_key", range(1, len(dim_product) + 1))

    return dim_product


def create_fact_sales(sales_df, dim_customer, dim_product):
    logging.info("Creating fact sales table using dimension joins")

    fact_sales = sales_df.merge(
        dim_customer[["customer_key", "customer_id"]],
        on="customer_id",
        how="left"
    )

    fact_sales = fact_sales.merge(
        dim_product[["product_key", "product_id", "unit_price"]],
        on="product_id",
        how="left"
    )

    fact_sales["total_amount"] = fact_sales["quantity"] * fact_sales["unit_price"]

    fact_sales = fact_sales[
        [
            "sale_id",
            "customer_key",
            "product_key",
            "sale_date",
            "quantity",
            "unit_price",
            "total_amount",
            "customer_id",
            "product_id"
        ]
    ]

    return fact_sales


def validate_fact_table(fact_sales):
    logging.info("Validating fact sales table")

    total_records = len(fact_sales)

    missing_customer_keys = fact_sales["customer_key"].isna().sum()
    missing_product_keys = fact_sales["product_key"].isna().sum()
    missing_total_amount = fact_sales["total_amount"].isna().sum()

    valid_fact_sales = fact_sales.dropna(
        subset=["customer_key", "product_key", "total_amount"]
    ).copy()

    rejected_records = total_records - len(valid_fact_sales)

    validation_results = {
        "total_sales_records": total_records,
        "valid_fact_records": len(valid_fact_sales),
        "rejected_records": rejected_records,
        "missing_customer_keys": int(missing_customer_keys),
        "missing_product_keys": int(missing_product_keys),
        "missing_total_amount": int(missing_total_amount)
    }

    valid_fact_sales["customer_key"] = valid_fact_sales["customer_key"].astype(int)
    valid_fact_sales["product_key"] = valid_fact_sales["product_key"].astype(int)

    return valid_fact_sales, validation_results


def load_to_sqlite(dim_customer, dim_product, fact_sales):
    logging.info("Loading dimension and fact tables into SQLite database")

    conn = sqlite3.connect(DATABASE_FILE)

    dim_customer.to_sql("dim_customer", conn, if_exists="replace", index=False)
    dim_product.to_sql("dim_product", conn, if_exists="replace", index=False)
    fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)

    conn.close()


def generate_report(validation_results):
    logging.info("Generating data quality report")

    with open(REPORT_FILE, "w") as report:
        report.write("Day 15 Data Quality Report\n")
        report.write("==========================\n\n")
        report.write(f"Total sales records: {validation_results['total_sales_records']}\n")
        report.write(f"Valid fact records loaded: {validation_results['valid_fact_records']}\n")
        report.write(f"Rejected records: {validation_results['rejected_records']}\n")
        report.write(f"Missing customer keys: {validation_results['missing_customer_keys']}\n")
        report.write(f"Missing product keys: {validation_results['missing_product_keys']}\n")
        report.write(f"Missing total amount values: {validation_results['missing_total_amount']}\n")


def run_pipeline():
    setup_logging()

    logging.info("Pipeline started")

    customers_df, products_df, sales_df = extract_data()

    dim_customer = create_customer_dimension(customers_df)
    dim_product = create_product_dimension(products_df)

    fact_sales = create_fact_sales(sales_df, dim_customer, dim_product)

    valid_fact_sales, validation_results = validate_fact_table(fact_sales)

    load_to_sqlite(dim_customer, dim_product, valid_fact_sales)

    generate_report(validation_results)

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()