# Day 5: Multi-Source Customer Orders Merge Pipeline

## Project Overview

This project builds a data engineering pipeline that integrates data from two different sources (CSV and JSON), cleans messy data, standardizes formats, and merges them into a single analytics-ready dataset.

It also includes logging and a data quality report to track pipeline health and data issues.

---

## Problem Statement

In real-world systems, data is often spread across multiple sources.

* Customer product data may come from CSV exports
* Order transaction data may come from APIs in JSON format

These datasets are often messy, with:

* inconsistent formats
* missing values
* duplicate records
* mismatched keys

To enable accurate reporting, we need to clean, validate, and merge these datasets into one reliable dataset.

---

## What We Are Building

We are building a Python-based ETL pipeline that:

* reads data from CSV and JSON sources
* cleans and standardizes messy data
* handles inconsistent date formats
* removes invalid and duplicate records
* merges datasets using:

  * `customer_id`
  * `product_name`
* tracks unmatched records
* generates a final merged dataset
* creates a data quality report
* logs all pipeline steps

---

## Folder Structure

day-005-multi-source-merge-pipeline/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   ├── customer_products.csv
│   └── orders.json
├── output/
│   ├── merged_output.csv
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/

---

## Tech Stack

* Python
* Pandas
* JSON
* Logging module

---

## Input Data

### CSV File: `customer_products.csv`

Contains customer product data:

* customer_id
* product_name
* purchase_date
* quantity

### JSON File: `orders.json`

Contains order transaction data:

* customer_id
* product_name
* order_date
* order_amount

---

## Data Cleaning Rules

### Common Cleaning Steps

* remove duplicate rows
* standardize column names to lowercase
* trim extra spaces
* convert text to lowercase for consistency

---

### Customer CSV Cleaning

* remove rows with missing:

  * customer_id
  * product_name
  * purchase_date
  * quantity
* convert quantity to numeric
* standardize purchase_date format

---

### Orders JSON Cleaning

* remove rows with missing:

  * customer_id
  * product_name
  * order_date
  * order_amount
* convert order_amount to numeric
* standardize order_date format

---

## Date Standardization

This pipeline supports multiple date formats such as:

* 2026-04-10
* 04/11/2026
* 2026/04/12
* 12-04-2026
* 18/04/2026

All dates are converted into a standard format:

YYYY-MM-DD

---

## Merge Logic

Datasets are merged using:

* customer_id
* product_name

### Join Type

INNER JOIN is used:

* only matching records from both datasets are included
* unmatched records are excluded from final output

---

## Smart Enhancement

This project includes data quality tracking:

* rows dropped during cleaning
* unmatched records from each dataset
* final merged row count

This simulates real-world data validation and monitoring.

---

## How to Run the Project

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the pipeline

```bash
python src/pipeline.py
```

---

## Output Files

After running the pipeline, the following files will be created:

### 1. merged_output.csv

Final cleaned and merged dataset.

### 2. data_quality_report.txt

Contains:

* input row counts
* rows dropped during cleaning
* unmatched records
* final row count

### 3. pipeline.log

Contains execution logs such as:

* pipeline start and end
* data loading
* cleaning steps
* merging process

---

## Expected Output Example

### merged_output.csv

customer_id,product_name,purchase_date,quantity,order_date,order_amount
101,laptop,2026-04-10,2,2026-04-10,1200
102,mouse,2026-04-11,1,2026-04-11,25
103,keyboard,2026-04-12,1,2026-04-12,80

---

### data_quality_report.txt

## DATA QUALITY REPORT

CSV input rows: 6
JSON input rows: 5
CSV rows dropped during cleaning: 2
JSON rows dropped during cleaning: 1
CSV rows without match in JSON: 1
JSON rows without match in CSV: 1
Final merged rows: 3

---

## Key Learnings

* reading data from multiple sources (CSV + JSON)
* handling messy real-world data
* standardizing text and dates
* merging datasets using multiple keys
* identifying unmatched records
* implementing logging in pipelines
* generating data quality reports

---

## Conclusion

This project introduces a core data engineering concept:

combining multiple data sources into a single clean dataset.

It also demonstrates how to handle messy data, ensure consistency, and build trust in data through validation and reporting.

---
