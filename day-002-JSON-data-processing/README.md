# Day 2: JSON Customer Orders ETL Pipeline

## Project Overview

This is a beginner-friendly data engineering project that processes raw customer order data stored in a JSON file. Such data commonly comes from APIs and web systems in real-world scenarios. The project implements an ETL pipeline to clean, validate, and transform the data into a structured format, producing a clean output file along with a data quality report and logging.

---

## Problem Statement

Raw data coming from APIs and web applications is often inconsistent and messy. It may contain missing values, incorrect formats, invalid numbers, or unexpected text values.

For a business to perform accurate reporting and analysis, this data needs to be cleaned and standardized before use.

This project solves that problem by building a simple ETL pipeline that converts raw JSON data into clean and reliable output.

---

## What This Project Does

* Reads raw order data from a JSON file
* Cleans and standardizes customer and product names
* Converts amount values into numeric format
* Standardizes date formats into `YYYY-MM-DD`
* Validates important fields and removes invalid records
* Standardizes order status values
* Generates:

  * Cleaned JSON output file
  * Data quality report
  * Pipeline execution logs

---

## Folder Structure

```bash
day-002-json-data-processing/
├── README.md
├── requirements.txt
├── src/
│   └── json_etl_pipeline.py
├── data/
│   └── raw_orders.json
├── output/
│   ├── cleaned_orders.json
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/
```

---

## Technologies Used

* Python
* JSON
* ETL (Extract, Transform, Load)
* Data Validation
* File Handling
* Logging

---

## Smart Enhancements

* Data validation to filter invalid records
* Data quality report to track valid and invalid records
* Logging to monitor pipeline execution, errors, and skipped records

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python src/json_etl_pipeline.py
```

---

## Expected Output

### Console Output

```bash
JSON ETL pipeline completed successfully.
Cleaned file saved to: output/cleaned_orders.json
Report saved to: output/data_quality_report.txt
```

---

### Output Files

* `output/cleaned_orders.json` → cleaned valid records
* `output/data_quality_report.txt` → summary of processing
* `output/pipeline.log` → detailed execution logs

---

## Sample Data Quality Report

```txt
JSON Data Quality Report
========================
Total records: 6
Valid records: 2
Invalid records: 4
```

---

## Sample Log Output

```txt
2026-04-16 12:00:01 - INFO - Pipeline started
2026-04-16 12:00:01 - INFO - Input file read successfully
2026-04-16 12:00:01 - INFO - Processing 6 records
2026-04-16 12:00:01 - WARNING - Invalid record skipped: {...}
2026-04-16 12:00:01 - INFO - Pipeline completed successfully
```

---

## Key Learning Outcomes

* Working with JSON data in Python
* Building a basic ETL pipeline
* Cleaning and validating semi-structured data
* Handling inconsistent formats like dates and numbers
* Generating data quality reports
* Implementing logging for pipeline monitoring

---

## Future Improvements

* Add detailed error reasons for rejected records
* Handle nested JSON structures
* Store cleaned data in a database (SQLite)
* Add configuration file for pipeline settings
* Introduce API-based data ingestion

