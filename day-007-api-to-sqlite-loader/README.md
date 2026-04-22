# Day 7: API to SQLite Data Loader

## Project Overview

This project is a beginner-friendly data engineering pipeline that extracts data from a public API, validates it, and loads it into a SQLite database.

Instead of storing API data only in files like CSV or JSON, this project demonstrates how to store structured data inside a database for easier querying and analysis.

---

## Problem Statement

Organizations often receive data from external APIs, but raw API responses are not directly usable for analytics or reporting. The data may contain missing or inconsistent fields and is not stored in a structured format.

This project solves that problem by:

* Fetching data from an API
* Validating required fields
* Cleaning the data
* Storing valid records in a database
* Generating logs and a data quality report

---

## What This Project Builds

* Extract data from a public API
* Validate records before loading
* Transform data into structured format
* Create a SQLite database
* Create a database table
* Load clean records into the table
* Generate a data quality report
* Generate pipeline logs

---

## Folder Structure

```
day-007-api-to-sqlite-loader/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
├── output/
│   ├── api_data.db
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/
```

---

## Tools & Technologies Used

* Python
* Requests (API calls)
* SQLite (Database)
* Logging

---

## Smart Enhancement

This project includes a **data quality validation step** before loading data into the database.

Validation checks:

* Missing `id`
* Missing `userId`
* Missing `title`
* Missing `body`

Invalid records are skipped and documented in a report.

---

## Data Source

Public API used:

```
https://jsonplaceholder.typicode.com/posts
```

Each record contains:

* userId
* id
* title
* body

---

## ETL Pipeline Flow

### 1. Extract

* Fetch data from API
* Convert JSON response into Python objects

### 2. Transform

* Validate required fields
* Clean and standardize data
* Separate valid and invalid records

### 3. Load

* Create SQLite database
* Create `posts` table
* Insert valid records into the table

### 4. Monitor

* Write logs for each step
* Generate data quality report

---

## SQLite Table Schema

```
CREATE TABLE IF NOT EXISTS posts (
    post_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL
);
```

---

## How to Run the Project

### Step 1: Create Virtual Environment

```
python -m venv venv
```

### Step 2: Activate Virtual Environment

Windows:

```
venv\Scripts\activate
```

---

### Step 3: Install Dependencies

```
pip install -r requirements.txt
```

---

### Step 4: Run the Pipeline

```
python src/pipeline.py
```

---

## Expected Output

### Terminal Output

```
Pipeline executed successfully.
Database created at: output/api_data.db
Report created at: output/data_quality_report.txt
Log created at: output/pipeline.log
```

---

## Output Files

After running the pipeline, the following files are generated in the `output/` folder:

* `api_data.db` → SQLite database file
* `data_quality_report.txt` → Validation report
* `pipeline.log` → Execution logs

---

## Sample Data Quality Report

```
Data Quality Report
===================

Total valid records: 100
Total invalid records: 0
```

---

## How to View Database

Do NOT open `.db` file directly.

Use VS Code extension:

* Install: SQLite (by alexcvzz)

Steps:

1. Press `Ctrl + Shift + P`
2. Select `SQLite: Open Database`
3. Choose `output/api_data.db`
4. View `posts` table

---

## Key Learning Outcomes

* How to fetch data from APIs using Python
* How to validate and clean incoming data
* How to create and use SQLite databases
* How to create tables using SQL
* How to insert data into a database
* How to implement logging in pipelines
* How to generate data quality reports
* Understanding end-to-end ETL pipeline flow

---

## Real-World Use Case

This project simulates a real data engineering scenario where:

* APIs act as data sources
* Data needs validation before storage
* Clean data is stored in a database for analytics

This pattern is widely used in:

* Finance systems
* Healthcare data pipelines
* SaaS data ingestion
* Reporting platforms

---

## Future Improvements

* Add timestamps for each load
* Implement incremental data loading
* Prevent duplicate processing more robustly
* Add SQL queries for analysis
* Move configuration into a config file
* Add logging rotation

---

## Important Notes

* Logs are appended on every run (this is normal)
* Database uses `INSERT OR REPLACE` to avoid duplicates
* Virtual environment should NOT be pushed to GitHub

Add this to `.gitignore`:

```
venv/
```

---

## Git Commands

```
git init
git add .
git commit -m "Add Day 7 API to SQLite data loader"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

If repo already exists:

```
git add .
git commit -m "Add Day 7 project"
git push
```

---

## Project Summary (2 Lines)

This project builds a complete ETL pipeline that extracts data from an API, validates it, and loads it into a SQLite database.

It introduces database loading, data validation, and logging, which are core concepts in real-world data engineering.
