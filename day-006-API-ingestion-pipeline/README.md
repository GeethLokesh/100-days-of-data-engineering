# Day 6: API Data Ingestion Pipeline

## Project Title

API Data Ingestion Pipeline Using Python

---

## Project Overview

This project builds a simple data engineering pipeline that fetches raw data from an external API, processes it, cleans it, and stores it in a structured CSV format.

It also generates a data quality report and logs the pipeline execution for monitoring and debugging.

This is the first project where the data source is an API instead of local files.

---

## Problem Statement

In real-world systems, data is often received from APIs instead of static files. API data can contain missing values, duplicate records, and inconsistent formats.

The goal of this project is to:

* fetch raw data from an API
* clean and standardize the data
* store it in a usable format
* generate a data quality report
* track execution using logs

---

## What We Are Building

We are building a mini ETL pipeline:

API → Raw JSON → Clean Data → CSV Output → Data Quality Report → Logs

---

## Folder Structure

day-006-api-data-ingestion/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── raw_api_data.json
├── output/
│   ├── cleaned_data.csv
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/

---

## Tech Stack

* Python
* Pandas
* Requests
* JSON
* Logging

---

## Input Source

API used in this project:

https://jsonplaceholder.typicode.com/posts

This API returns sample post data in JSON format.

---

## Pipeline Steps

### 1. Fetch Data from API

The pipeline sends a request to the API and retrieves raw JSON data.

### 2. Save Raw Data

The API response is saved in:
data/raw_api_data.json

This ensures we always have the original data.

---

### 3. Convert JSON to Table

The raw JSON is converted into a Pandas DataFrame for processing.

---

### 4. Rename Columns

Columns are renamed to clear and consistent names:

* userId → user_id
* id → post_id
* title → post_title
* body → post_description

---

### 5. Handle Missing Values

Missing values in important fields are replaced with:

unknown

---

### 6. Add created_at Column

A new column is added to store when the data was processed.

---

### 7. Remove Duplicates

Duplicate rows are removed to improve data quality.

---

### 8. Save Cleaned Data

The final cleaned data is saved as:

output/cleaned_data.csv

---

### 9. Generate Data Quality Report

A report is created with:

* total row count
* null values per column

Saved as:
output/data_quality_report.txt

---

### 10. Logging

All pipeline steps are logged into:

output/pipeline.log

This helps in debugging and monitoring.

---

## How to Run the Project

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Pipeline

```bash
python src/pipeline.py
```

---

## Expected Output

### Files Created

data/raw_api_data.json
output/cleaned_data.csv
output/data_quality_report.txt
output/pipeline.log

---

## Example Data Quality Report

```
Total Rows: 100

Null Counts:
user_id: 0
post_id: 0
post_title: 0
post_description: 0
created_at: 0
```

---

## Smart Enhancement (Important)

### Logging + Error Handling

The pipeline:

* handles API failures
* logs errors instead of crashing
* safely exits when data is missing

This makes it closer to a real production pipeline.

---

## Learning Outcomes

By completing this project, you learned:

* how APIs work in data engineering
* how to fetch JSON data
* how to convert JSON into structured data
* how to clean and standardize data
* how to build a basic ETL pipeline
* how to implement logging
* how to create data quality reports

---

## Future Improvements

* Add API authentication
* Handle pagination
* Add retry logic
* Load data into a database
* Schedule pipeline execution
* Add configuration file

---

## Git Commands

```bash
git init
git add .
git commit -m "Day 6 - API Data Ingestion Pipeline"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

---

## Final Summary

This project introduces API-based data ingestion, which is a core part of real-world data engineering. It shows how raw data from external systems can be collected, cleaned, validated, and stored for downstream use.
