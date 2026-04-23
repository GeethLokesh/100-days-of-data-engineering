# Day 8: Query + Transform SQLite Data Using SQL

---

## Project Overview

This project demonstrates how to query and transform data stored in a SQLite database using SQL inside a Python pipeline.

The pipeline takes raw post data, validates it, applies SQL transformations, and produces an analytics-ready dataset along with a CSV export and data quality report.

In real-world data engineering, raw data is not directly used for reporting. Instead, it is transformed into structured and business-friendly formats. This project simulates that process.

---

## Problem Statement

A business team has raw post data stored in a SQLite database, but the raw table is not suitable for reporting.

They need:
- clean and valid records
- derived columns for analysis
- categorized data
- a structured dataset for reporting

This project solves that by transforming raw data into a new analytics table using SQL.

---

## What We Are Building

We are building a mini data pipeline that:

- creates a raw SQLite table (`posts`)
- loads sample data
- performs data quality checks
- transforms data using SQL
- creates a new table (`analytics_posts`)
- exports transformed data to CSV
- generates a data quality report
- logs all pipeline activity

---

## Folder Structure

day-008-sqlite-query-transform/
│
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
├── output/
│   ├── transformed_posts.db
│   ├── analytics_posts.csv
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/

---

## Technologies Used

- Python
- SQLite
- SQL
- CSV
- Logging

---

## Smart Enhancement

This project includes data quality validation before transformation.

Checks performed:
- total number of records
- null or empty titles
- null or empty bodies
- duplicate ids

This ensures only valid data moves into the analytics layer.

---

## End-to-End Workflow

Step 1: Setup Logging  
Creates output folder and initializes logging.

Step 2: Connect to SQLite  
Establishes connection to the database file.

Step 3: Create Raw Table  
Creates a table called `posts` if it does not exist.

Step 4: Load Data  
Inserts sample data only if the table is empty.

Step 5: Data Quality Checks  
Validates missing values and duplicates, and creates a report.

Step 6: SQL Transformation  
Creates a new table `analytics_posts`.

Step 7: Export Data  
Writes transformed data to CSV.

Step 8: Summary Output  
Displays category-level counts.

---

## Database Design

Raw Table: posts

- id → unique identifier  
- user_id → user reference  
- title → post title  
- body → post content  

Transformed Table: analytics_posts

- id  
- user_id  
- title  
- body  
- title_length  
- body_length  
- title_category  

---

## SQL Transformation Logic

CREATE TABLE analytics_posts AS
SELECT
    id,
    user_id,
    title,
    body,
    LENGTH(title) AS title_length,
    LENGTH(body) AS body_length,
    CASE
        WHEN LENGTH(title) < 20 THEN 'short'
        WHEN LENGTH(title) BETWEEN 20 AND 50 THEN 'medium'
        ELSE 'long'
    END AS title_category
FROM posts
WHERE title IS NOT NULL
  AND TRIM(title) != ''
  AND body IS NOT NULL
  AND TRIM(body) != '';

---

## Transformation Explanation

- LENGTH(title) → calculates title size  
- LENGTH(body) → calculates body size  
- CASE WHEN → categorizes title into short, medium, long  
- WHERE → removes invalid records  

---

## How to Run the Project in VS Code

Step 1: Open the project folder  
Open `day-008-sqlite-query-transform` in VS Code.

Step 2: Create virtual environment  

python -m venv venv

Step 3: Activate environment  

Windows:
venv\Scripts\activate

Step 4: Install requirements  

pip install -r requirements.txt

(No external libraries required)

Step 5: Run the pipeline  

python src/pipeline.py

---

## Expected Output

Terminal Output:

Transformed Data Summary  
========================  
Category: medium | Records: X  
Category: short | Records: X  
Category: long | Records: X  

Pipeline completed successfully.

---

## Output Files

Database:
output/transformed_posts.db  
Contains raw and transformed tables.

CSV:
output/analytics_posts.csv  
Contains transformed dataset.

Data Quality Report:
output/data_quality_report.txt  

Example:
Total raw records: 10  
Null titles: 0  
Null bodies: 0  
Duplicate ids: 0  

Logs:
output/pipeline.log  
Tracks pipeline execution.

---

## Key Learning Outcomes

- how to connect Python with SQLite  
- how to use SQL inside Python  
- how to transform raw data using SQL  
- how to create analytics-ready tables  
- how to perform data quality checks  
- how to export SQL results to CSV  
- how to build a simple ETL pipeline  
- how to design rerun-safe workflows  

---

## Tool Swaps (For Learning)

PostgreSQL → for larger datasets and real production systems  

Pandas → for transformation using Python instead of SQL  

DuckDB → for analytics-focused local queries  

dbt → for managing SQL transformations professionally  

---

## Final Outcome

This project converts raw SQLite data into a structured analytics dataset using SQL transformations.

It shows how data engineers move from raw data storage to business-ready reporting tables.

---

## 2-Line Summary

Day 8 focuses on transforming raw SQLite data into an analytics-ready table using SQL.  
It introduces SQL-based transformation, validation, and reporting within a pipeline.