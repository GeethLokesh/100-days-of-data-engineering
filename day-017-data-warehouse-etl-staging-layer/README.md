# Day 17: Data Warehouse ETL Pipeline with Staging Layer

## Project Overview

This project builds a simple data warehouse ETL pipeline using Python and SQLite.

The main goal is to understand how real data engineering pipelines use a staging layer before loading clean data into warehouse tables.

In real companies, raw data is usually not loaded directly into final reporting tables. It first lands in a staging area. From there, data engineers validate, clean, transform, and then load trusted data into warehouse tables.

---

# Problem Statement

A retail company receives raw sales data from different source systems. The data may contain duplicates, missing values, invalid dates, or incorrect prices.

The company wants to first load the raw data into a staging table, perform validation checks, and then load only clean records into warehouse tables used for reporting.

---

# What This Project Builds

This project creates an ETL pipeline that:

1. Reads raw sales data from a CSV file
2. Loads raw data into a staging table
3. Performs validation and cleaning
4. Removes duplicate and invalid records
5. Loads clean data into warehouse tables
6. Creates dimension and fact tables
7. Generates a data quality report
8. Creates a pipeline log file

---

# Folder Structure

```text
day-017-data-warehouse-etl-staging-layer/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── raw_sales.csv
├── output/
│   ├── warehouse.db
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/
```

---

# Tools Used

- Python
- Pandas
- SQLite
- VS Code
- Git and GitHub

---

# Why We Use a Staging Layer

The staging layer acts as a temporary landing area for raw data.

Instead of directly loading raw data into final reporting tables, we first store it in a staging table.

This helps us:

- Preserve raw source data
- Debug pipeline issues
- Validate data before warehouse loading
- Separate raw data from trusted reporting data
- Build cleaner warehouse pipelines

---

# Warehouse Tables Created

## 1. staging_sales

This table stores the raw data exactly as received from the CSV file.

---

## 2. dim_customer

This dimension table stores customer details.

### Columns

| Column Name | Description |
|---|---|
| customer_id | Unique customer ID |
| customer_name | Customer full name |

---

## 3. dim_product

This dimension table stores product details.

### Columns

| Column Name | Description |
|---|---|
| product_id | Unique product ID |
| product_name | Product name |
| unit_price | Product price |

---

## 4. fact_sales

This fact table stores sales transactions.

It connects customers and products using IDs and stores measurable business values like quantity and total amount.

### Columns

| Column Name | Description |
|---|---|
| order_id | Unique order ID |
| customer_id | Customer reference |
| product_id | Product reference |
| quantity | Number of products sold |
| unit_price | Price per product |
| total_amount | Quantity × Unit Price |
| order_date | Date of sale |

---

# ETL Pipeline Flow

## Step 1: Extract

The pipeline reads raw sales data from the CSV file.

Example:

```python
df = pd.read_csv(DATA_FILE)
```

Purpose:

- Collect source data
- Begin ETL workflow
- Load raw records into memory

---

## Step 2: Load into Staging Layer

The raw data is loaded into the `staging_sales` table.

Purpose:

- Preserve original raw data
- Allow debugging and auditing
- Prevent raw data from directly entering warehouse tables

---

## Step 3: Validate and Clean Data

The pipeline performs several validation checks.

### Validation Checks Performed

| Validation | Purpose |
|---|---|
| Duplicate detection | Prevent duplicate business records |
| Missing quantity check | Ensure quantity exists |
| Invalid price detection | Prevent negative or zero prices |
| Invalid date detection | Ensure proper reporting dates |
| Null field checks | Prevent incomplete records |

---

## Step 4: Transform Data

The pipeline transforms the data before warehouse loading.

Transformations include:

- Converting quantity to integer
- Formatting dates
- Calculating total sales amount

Example:

```python
clean_df["total_amount"] = clean_df["quantity"] * clean_df["unit_price"]
```

---

## Step 5: Load Warehouse Tables

Clean records are loaded into:

- dim_customer
- dim_product
- fact_sales

Purpose:

- Organize reporting data
- Support analytics queries
- Simulate warehouse architecture

---

## Step 6: Generate Reports and Logs

The pipeline creates:

### 1. Data Quality Report

Contains:

- Total rows
- Duplicate rows
- Invalid rows
- Clean rows loaded
- Rejected rows

---

### 2. Pipeline Log File

Tracks:

- Pipeline execution steps
- Errors
- Validation progress
- Table loading status

---

# Smart Enhancement

This project includes a staging layer with validation and logging.

This is important because real data warehouse pipelines usually do not trust raw data immediately. They first stage it, inspect it, clean it, and then load it into final tables.

---

# How to Run This Project

## Step 1: Open the project in VS Code

```bash
cd day-017-data-warehouse-etl-staging-layer
```

---

## Step 2: Create a virtual environment

```bash
python -m venv venv
```

---

## Step 3: Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

---

## Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5: Run the pipeline

```bash
python src/pipeline.py
```

---

# Expected Output

After running the pipeline, the output folder will contain:

```text
warehouse.db
data_quality_report.txt
pipeline.log
```

The database will contain:

```text
staging_sales
dim_customer
dim_product
fact_sales
```

---

# Example Business Use Case

Imagine a retail company receives sales data from multiple systems daily.

Some records may contain:

- Missing quantities
- Invalid prices
- Duplicate sales
- Incorrect dates

Instead of directly loading this raw data into dashboards, the company first stages the data, validates it, and only loads trusted records into reporting tables.

This prevents incorrect business reporting and improves data reliability.

---

# Real-World Technologies That Use Similar Architecture

This same architecture is used in:

- Snowflake
- Azure Synapse
- Amazon Redshift
- Google BigQuery
- PostgreSQL Warehouses
- Databricks Lakehouse

---

# What I Learned

In this project, I learned:

- How staging layers work in warehouse pipelines
- Why raw data should not directly enter reporting tables
- How to create staging, dimension, and fact tables
- How ETL pipelines validate data
- How to generate data quality reports
- How logging helps monitor pipelines
- Basic warehouse-style architecture

---

# Tool Swaps (Very Important for Learning)

| Current Tool | Alternative Tool | Real-World Usage |
|---|---|---|
| SQLite | PostgreSQL | Production warehouse databases |
| Pandas | PySpark | Large-scale distributed processing |
| CSV | APIs / Kafka | Real-time ingestion |
| Python logging | Airflow Monitoring | Enterprise pipeline monitoring |
| SQLite warehouse | Snowflake | Cloud data warehouse |

---

# Future Improvements

Possible future enhancements:

- Add surrogate keys
- Add incremental loading
- Add audit tables
- Add slowly changing dimensions
- Move from SQLite to PostgreSQL
- Add Airflow scheduling
- Add cloud storage integration

---

# Final Summary

This project introduces an important real-world data engineering concept called the staging layer.

Instead of directly loading raw source data into reporting tables, the pipeline first stages the data, validates it, cleans it, and then loads trusted records into warehouse tables.

This design improves:

- Data reliability
- Reporting quality
- Pipeline debugging
- Data governance
- Warehouse architecture understanding

This project is a strong foundation for advanced warehouse engineering concepts that will come later in the 100 Days of Data Engineering journey.