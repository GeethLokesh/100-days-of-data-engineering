# Day 10: SQL + Python Data Pipeline with Automated Daily Reports

---

## Project Overview

This project builds a complete data pipeline that combines Python and SQL to generate automated daily business reports from raw sales data.

The pipeline reads a CSV file, performs data quality checks, calculates business metrics, stores data in SQLite, and generates a daily report along with logs.

This simulates a real-world reporting workflow where business teams depend on daily metrics.

---

## Problem Statement

Business teams receive daily sales data in CSV format. Manually calculating metrics like total revenue, total orders, and region-wise sales is time-consuming and error-prone.

The goal is to automate this process using a data pipeline that ensures accuracy, consistency, and traceability.

---

## What This Project Builds

This pipeline performs:

1. Data extraction from CSV
2. Data validation and quality checks
3. Data transformation (revenue calculation)
4. Loading data into SQLite
5. Running SQL queries for reporting
6. Generating daily reports automatically
7. Logging every pipeline step

---

## Tools Used

* Python
* Pandas
* SQLite
* SQL
* VS Code
* Logging

---

## Folder Structure

```text
day-010-sql-python-daily-reports/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── sales.csv
├── output/
├── screenshots/
```

---

## Input Data

The pipeline uses a CSV file:

```text
data/sales.csv
```

It contains:

* order_id
* order_date
* customer_id
* region
* product
* quantity
* unit_price

---

## Pipeline Flow

### 1. Extract

Reads the CSV file using pandas.

* Validates if file exists
* Logs number of records loaded

---

### 2. Data Validation

Performs quality checks:

* Duplicate order IDs
* Missing values
* Invalid quantity (<= 0)
* Invalid unit price (<= 0)

Creates:

```text
output/data_quality_report.txt
```

---

### 3. Transform

Creates a new column:

```text
revenue = quantity * unit_price
```

---

### 4. Load

Loads processed data into SQLite:

```text
output/sales.db
```

Table created:

```text
sales
```

---

### 5. Reporting (SQL)

Runs SQL queries to generate:

* Total Orders
* Total Revenue
* Average Order Value
* Sales by Region
* Sales by Product

Outputs:

```text
output/daily_sales_report.txt
output/sales_by_region.csv
```

---

### 6. Logging (Smart Enhancement)

The pipeline logs:

* Start and end of each step
* Record counts
* Data issues
* Errors if pipeline fails

Log file:

```text
output/pipeline.log
```

Logging levels used:

* INFO
* WARNING
* ERROR

Each step logs:

```text
STEP START: Extract Data
STEP END: Extract Data | Records Loaded: 12
```

Pipeline is wrapped in try/except to capture failures.

---

## How to Run the Project

### Step 1: Open Project in VS Code

```text
day-010-sql-python-daily-reports
```

---

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

---

### Step 3: Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5: Run Pipeline

```bash
python src/pipeline.py
```

---

## Expected Output

```text
output/
├── sales.db
├── daily_sales_report.txt
├── data_quality_report.txt
├── sales_by_region.csv
├── pipeline.log
```

---

## Sample Daily Report

```text
Daily Sales Report
==================

Business Summary
----------------
Total Orders: 12
Total Revenue: $3645
Average Order Value: $303.75

Sales by Region
----------------
region  total_orders  total_revenue
East             4         1330.0
West             3         1045.0
North            2         1030.0
South            3          640.0

Sales by Product
----------------
product   total_orders  total_revenue
Laptop             3         2770.0
Monitor            3          730.0
Keyboard           3          175.0
Mouse              3          170.0
```

---

## Data Quality Report

```text
Total records checked: 12
Duplicate order IDs: 0
Missing values: 0
Invalid quantity records: 0
Invalid unit price records: 0
```

---

## Key Learning

Python handles:

* File ingestion
* Validation
* Automation
* Logging

SQL handles:

* Aggregations
* Business logic
* Reporting

---

## Real-World Use Case

This pattern is used in real pipelines where:

* Daily data is ingested
* Stored in a database
* Queried using SQL
* Report generated for stakeholders

---

## Tool Swaps (Important)

SQLite → PostgreSQL
Used for multi-user and larger datasets

SQLite → Snowflake
Used for cloud data warehousing

CSV → API
Used for real-time or external data ingestion

Script → Airflow
Used for scheduling pipelines

---

## Smart Enhancement

Logging + automated daily report generation

This ensures:

* Traceability
* Debugging
* Reliability
* Automation

---

## Portfolio Summary

Built a SQL and Python data pipeline that loads sales data into SQLite and generates automated daily reports.

Implemented data quality checks, structured logging, and SQL-based business metrics for reporting.

---
