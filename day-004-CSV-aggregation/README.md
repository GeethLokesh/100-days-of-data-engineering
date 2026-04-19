# Day 4: Sales Data Cleaning and Aggregation Pipeline

## Project Overview
This project builds a Python ETL pipeline to process messy sales data from a CSV file, clean and standardize it, and generate aggregated business insights. It simulates how real-world raw data is prepared before being used in dashboards and reports.

## Problem Statement
Raw sales data coming from multiple systems often contains inconsistent date formats, incorrect or messy product names, missing values, invalid numeric values, and duplicate records. Using this data directly can lead to incorrect business reports and poor decision-making.

## What We Are Building
This pipeline performs:
- Extract → Read messy CSV data
- Clean → Fix formats, standardize values, remove invalid rows
- Transform → Create total sales column
- Aggregate → Generate sales by date and sales by product
- Load → Save results to output files
- Logging → Track pipeline execution

## Folder Structure
day-004-sales-data-cleaning-aggregation/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── sales.csv
├── output/
│   ├── sales_by_date.csv
│   ├── sales_by_product.csv
│   └── pipeline.log
└── screenshots/

## Input Data (Messy Example)
order_id,order_date,product,quantity,price
1,04/01/2026,Laptop,1,1000
2,2026-04-01,Mouse,2,25
3,2026/04/02,laptop ,1,1000
4,04-02-2026,Keyboard,1,75
5,2026-04-02,Mouse,,25
6,2026-04-02,,3,25
7,2026-04-02,Mouse,3,twenty five
8,,Laptop,1,1000
9,2026-04-03,Mouse,2,25
9,2026-04-03,Mouse,2,25

## Pipeline Steps

### Extract
Reads the CSV file into a Pandas DataFrame.

### Clean
- Removes duplicate rows
- Standardizes date formats to YYYY-MM-DD
- Cleans product names by trimming spaces and fixing casing
- Converts quantity and price to numeric values safely
- Drops rows with missing or invalid critical fields

### Transform
Creates a new column:
total = quantity * price

### Aggregate
- Calculates total sales per date
- Calculates total sales per product

### Load
Saves output files:
- output/sales_by_date.csv
- output/sales_by_product.csv

### Logging
Logs all pipeline steps into output/pipeline.log.

## Smart Enhancement
Includes a data quality check that compares total sales from cleaned data and aggregated output to ensure no data loss or duplication.

## Tech Stack
Python, Pandas, Logging

## How to Run
1. Open project in VS Code
2. Install dependencies:
pip install -r requirements.txt
3. Run pipeline:
python src/pipeline.py

## Expected Output

sales_by_date.csv
order_date,total
2026-04-01,1050.0
2026-04-02,1075.0
2026-04-03,50.0

sales_by_product.csv
product,total
Keyboard,75.0
Laptop,2000.0
Mouse,125.0

## What I Learned
- Handling messy real-world data
- Difference between cleaning and transformation
- Importance of removing invalid data before aggregation
- Building a simple ETL pipeline
- Ensuring data quality before reporting

## Why This Project Matters
In real-world data engineering, raw data is rarely clean. This project demonstrates how to transform messy operational data into reliable business insights through proper cleaning, validation, and aggregation.

## Git Commands
git init
git add day-004-sales-data-cleaning-aggregation
git commit -m "Day 4 - Sales data cleaning and aggregation pipeline"
git push origin main

## 2-Line Summary
Built a Python ETL pipeline to clean messy sales data and generate aggregated reports by date and product.
Demonstrates real-world data preparation with cleaning, validation, and logging.