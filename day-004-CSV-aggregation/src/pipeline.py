import pandas as pd
import os
import logging
from datetime import datetime


INPUT_FILE = "data/sales.csv"
OUTPUT_DIR = "output"


def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.basicConfig(
        filename=f"{OUTPUT_DIR}/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def standardize_date(date_value):
    if pd.isna(date_value) or str(date_value).strip() == "":
        return None

    date_value = str(date_value).strip()
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y"]

    for fmt in formats:
        try:
            return datetime.strptime(date_value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def standardize_product(product_value):
    if pd.isna(product_value) or str(product_value).strip() == "":
        return None

    product = str(product_value).strip().lower()

    product_mapping = {
        "laptop": "Laptop",
        "mouse": "Mouse",
        "keyboard": "Keyboard"
    }

    return product_mapping.get(product, None)


def extract_data(file_path):
    logging.info("Reading CSV file")
    return pd.read_csv(file_path)


def clean_row(row):
    try:
        order_id = int(row["order_id"])
    except (ValueError, TypeError):
        order_id = None

    order_date = standardize_date(row["order_date"])
    product = standardize_product(row["product"])

    try:
        quantity = int(row["quantity"])
    except (ValueError, TypeError):
        quantity = None

    try:
        price = float(row["price"])
    except (ValueError, TypeError):
        price = None

    return {
        "order_id": order_id,
        "order_date": order_date,
        "product": product,
        "quantity": quantity,
        "price": price
    }


def clean_data(df):
    logging.info("Cleaning data")

    df = df.drop_duplicates()

    cleaned_rows = []
    for _, row in df.iterrows():
        cleaned_rows.append(clean_row(row))

    cleaned_df = pd.DataFrame(cleaned_rows)

    cleaned_df = cleaned_df.dropna(
        subset=["order_id", "order_date", "product", "quantity", "price"]
    )

    return cleaned_df


def transform_data(df):
    logging.info("Transforming data")

    df["total"] = df["quantity"] * df["price"]

    sales_by_date = df.groupby("order_date")["total"].sum().reset_index()
    sales_by_product = df.groupby("product")["total"].sum().reset_index()

    return sales_by_date, sales_by_product


def data_quality_check(df, agg_date, agg_product):
    logging.info("Running data quality checks")

    original_total = df["quantity"].mul(df["price"]).sum()
    aggregated_total = agg_date["total"].sum()

    if original_total != aggregated_total:
        logging.warning("Data mismatch detected!")
    else:
        logging.info("Data quality check passed")


def load_data(sales_by_date, sales_by_product):
    logging.info("Saving aggregated data")

    sales_by_date.to_csv(f"{OUTPUT_DIR}/sales_by_date.csv", index=False)
    sales_by_product.to_csv(f"{OUTPUT_DIR}/sales_by_product.csv", index=False)


def run_pipeline():
    setup_logging()

    df = extract_data(INPUT_FILE)
    cleaned_df = clean_data(df)

    sales_by_date, sales_by_product = transform_data(cleaned_df)

    data_quality_check(cleaned_df, sales_by_date, sales_by_product)

    load_data(sales_by_date, sales_by_product)

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()