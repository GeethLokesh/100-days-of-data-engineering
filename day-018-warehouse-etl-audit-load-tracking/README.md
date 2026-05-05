# Day 18: Data Warehouse ETL Pipeline with Audit Table and Load Tracking

## Project Title
Data Warehouse ETL Pipeline with Audit Table and Load Tracking

---

## Project Overview
This project builds a warehouse-style ETL pipeline using Python, Pandas, and SQLite.

The pipeline reads raw sales data from a CSV file, cleans and validates it, loads it into staging and warehouse tables, and generates a sales summary report.

Additionally, this project introduces an audit table, which tracks every pipeline run with execution details such as status, row counts, and timestamps.

---

## Problem Statement
In real-world data systems, loading data is not enough. Teams must also track:

- whether the pipeline ran successfully
- how many records were processed
- how many records failed validation
- when the pipeline started and ended

Without this visibility, debugging and monitoring pipelines becomes very difficult.

This project solves that by implementing audit-based load tracking.

---

## What We Are Building
We are building a warehouse ETL pipeline:

CSV → Clean Data → Staging Table → Warehouse Table → Report → Audit Table → Logs

---

## Folder Structure
day-018-warehouse-etl-audit-load-tracking/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── raw_sales.csv
├── output/
│   ├── warehouse.db
│   ├── sales_summary.csv
│   └── pipeline.log
└── screenshots/

---

## Tech Stack
- Python
- Pandas
- SQLite
- Logging

---

## Input Source
Local CSV file:
data/raw_sales.csv

This file contains:
- valid records
- duplicate records
- missing values
- invalid dates

---

## Pipeline Steps

1. Extract Data
Reads raw data from CSV file.

2. Clean and Validate Data
- removes duplicate records
- converts data types
- removes invalid rows
- standardizes date format

3. Load into Staging Table
Clean data is first loaded into staging_sales.
This acts as a temporary layer before final load.

4. Load into Warehouse Table
Data is moved into warehouse_sales.

Enhancements:
- adds calculated column → total_amount
- adds loaded timestamp

5. Generate Sales Summary Report
Creates aggregated report:
output/sales_summary.csv

Includes:
- total orders
- total quantity
- total sales per product

6. Audit Table (New Concept)
Tracks pipeline execution in audit_loads.

Stores:
- pipeline name
- start time
- end time
- status (SUCCESS / FAILED)
- extracted rows
- loaded rows
- rejected rows
- error message

7. Logging
All pipeline steps are logged in:
output/pipeline.log

Used for debugging and monitoring.

---

## Database Tables

staging_sales
Temporary cleaned data

warehouse_sales
Final reporting data
Includes:
- total_amount column
- loaded_at timestamp

audit_loads
Pipeline tracking table

---

## Data Quality Rules
The pipeline rejects rows if:
- missing quantity
- missing price
- invalid date
- missing key fields

Duplicates are removed.

---

## Expected Output

Files Created:
- output/warehouse.db
- output/sales_summary.csv
- output/pipeline.log

---

## Example Sales Summary
product,total_orders,total_quantity,total_sales
Laptop,3,3,2700
Monitor,1,1,250
Keyboard,1,1,75
Mouse,1,2,50

---

## Example Audit Table Record
pipeline_name: day_018_warehouse_etl
status: SUCCESS
extracted_rows: 10
loaded_rows: 6
rejected_rows: 4

---

## Smart Enhancement (Important)
Audit Table + Load Tracking

This project introduces production-level tracking:
- tracks pipeline success/failure
- tracks row counts
- stores execution history
- helps debugging and monitoring

This is widely used in real-world ETL systems.

---

## Learning Outcomes
By completing this project, you learned:
- how warehouse ETL pipelines work
- how staging layers are used
- how to build audit tables
- how to track pipeline execution
- how to validate and clean data
- how to generate reports from warehouse tables
- how logging and auditing work together

---

## Future Improvements
- Add batch IDs
- Track historical loads
- Add incremental loading
- Move to PostgreSQL
- Add scheduling (Airflow)
- Add alerting system

---

## Final Summary
This project moves beyond basic ETL and introduces audit tracking, which is a critical concept in real data engineering systems.

It ensures pipelines are not only running, but are also monitored, validated, and traceable.