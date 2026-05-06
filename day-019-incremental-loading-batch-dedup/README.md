# Day 19: Incremental Data Loading with Batch ID and Deduplication Strategy

## Project Overview

This project demonstrates an incremental data loading pipeline using Python, Pandas, and SQLite.

In real data engineering projects, pipelines often receive daily files from source systems. Sometimes the same file may be sent again, or the same record may appear multiple times because of retries or reruns.

This project solves that problem by using:

- Batch ID tracking
- Duplicate removal inside the incoming file
- Incremental loading into a database
- Audit table tracking
- Logging
- Data quality reporting

## Problem Statement

A retail company receives daily sales files from different store systems. The company wants to load only new sales records into its warehouse and avoid duplicate records caused by reruns or repeated source files.

The pipeline must also track each run using a batch ID so the data engineering team can debug and monitor every load.

## What This Project Builds

This project builds a small warehouse-style pipeline that:

1. Reads raw sales data from a CSV file
2. Creates a unique batch ID for each run
3. Cleans the incoming data
4. Removes duplicate records inside the same batch
5. Checks which records already exist in the database
6. Loads only new records into the `sales_fact` table
7. Stores batch-level audit details in the `batch_audit` table
8. Creates a data quality report
9. Writes pipeline logs

## Folder Structure

```text
day-019-incremental-loading-batch-dedup/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── daily_sales.csv
├── output/
│   ├── sales_warehouse.db
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/
```

## Tools Used

- Python
- Pandas
- SQLite
- VS Code
- Git and GitHub

## Key Concepts Learned

## Incremental Loading

Incremental loading means loading only new or changed data instead of loading the full dataset every time.

This is useful because real-world datasets can be large. Reloading everything again and again wastes time, storage, and compute resources.

In this project, we use `sale_id` to check whether a record already exists in the database.

If the `sale_id` is already present, the pipeline skips it.

## Batch ID

A batch ID is a unique identifier for a pipeline run.

Example:

```text
BATCH_20260505_143015
```

This helps us answer questions like:

- Which records were loaded in this run?
- How many records came in?
- How many records were skipped?
- Did the pipeline succeed or fail?
- When did the pipeline start and finish?

## Deduplication Strategy

Deduplication means removing repeated records.

In this project, duplicate records are checked in two places:

1. Inside the incoming CSV file
2. Against records already loaded in the database

This prevents duplicate data from entering the warehouse.

## Audit Table

The audit table stores pipeline run information.

The `batch_audit` table stores:

- Batch ID
- Source file path
- Records received
- Duplicates found
- Records loaded
- Records skipped
- Pipeline status
- Start time
- Completion time

This is useful for debugging, monitoring, and explaining what happened during each pipeline run.

## Data Quality Enhancement

The smart enhancement in this project is the combination of:

- Batch ID tracking
- Duplicate detection
- Audit logging
- Data quality report

This makes the pipeline more realistic and production-style.

## Input Data

The input file is stored at:

```text
data/daily_sales.csv
```

Sample data:

```csv
sale_id,customer_id,product_name,sale_amount,sale_date
S001,C001,Laptop,1200,2026-05-01
S002,C002,Mouse,25,2026-05-01
S003,C003,Keyboard,75,2026-05-02
S004,C004,Monitor,300,2026-05-02
S002,C002,Mouse,25,2026-05-01
S005,C005,Desk Chair,180,2026-05-03
S006,C006,USB Cable,15,2026-05-03
S006,C006,USB Cable,15,2026-05-03
```

## Database Tables

## sales_fact

This table stores the final loaded sales records.

Columns:

```text
sale_id
customer_id
product_name
sale_amount
sale_date
batch_id
loaded_at
```

## batch_audit

This table stores information about every pipeline run.

Columns:

```text
batch_id
source_file
records_received
duplicates_in_batch
records_loaded
records_skipped
status
started_at
completed_at
```

## How to Run This Project

Open the project folder in VS Code.

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python src/pipeline.py
```
## First Run Behavior

On the first run, the pipeline loads new records into the database.

Example result:

```text
Records received: 8
Duplicates found inside batch: 2
New records loaded: 6
Existing records skipped: 0
Pipeline status: SUCCESS
```

## Second Run Behavior

If you run the same pipeline again, the records already exist in the database.

The pipeline will skip them.

Example result:

```text
Records received: 8
Duplicates found inside batch: 2
New records loaded: 0
Existing records skipped: 6
Pipeline status: SUCCESS
```

This proves that the incremental loading logic is working.

## Why This Matters in Real Data Engineering

In real projects, pipelines may fail, rerun, or receive the same data again.

Without deduplication and batch tracking, duplicate records can enter reporting tables and create incorrect business metrics.

For example:

- Sales revenue may be counted twice
- Customer orders may appear multiple times
- Reports may show wrong totals
- Business teams may lose trust in the data

This project teaches how to make a pipeline safer and easier to monitor.

## What I Learned

In this project, I learned how to:

- Build an incremental loading pipeline
- Use a batch ID to track each pipeline run
- Remove duplicate records from incoming data
- Skip records that already exist in the database
- Create an audit table for pipeline monitoring
- Generate a data quality report
- Use logging for debugging

## Tool Swaps

The same project can be built using other tools.

### SQLite to PostgreSQL

SQLite is good for local learning.

In production, PostgreSQL can be used to support larger datasets, multiple users, stronger constraints, and better database management.

### Pandas to PySpark

Pandas is good for small and medium files.

For very large datasets, PySpark can process data across multiple machines.

### Python Script to Airflow DAG

Today we run the pipeline manually using Python.

Later, this same logic can be scheduled using Airflow so it runs daily automatically.

### Local CSV to Cloud Storage

Today the file is stored in the local `data` folder.

In real projects, files may come from cloud storage such as S3, ADLS, or Google Cloud Storage.


## Project Summary

Day 19 introduces a very important real-world data engineering concept: safe incremental loading.

This project shows how to load only new records, avoid duplicates, track every pipeline run, and create audit information for monitoring.

This is a strong portfolio project because it shows that the pipeline is not just moving data, but also protecting data quality and reliability.