# Day 1: Sales Data Cleaning ETL Pipeline

## Project Overview

This is a beginner-friendly data engineering project that processes raw sales data from a CSV file. The pipeline follows an ETL process to clean the data, generate a structured output dataset, and create a data quality report along with logging.

---

## Problem Statement

Raw sales data often contains:

- Missing values  
- Duplicate records  
- Inconsistent date formats  
- Invalid values like zero or negative quantity and price  

This makes the data unreliable for analysis. The goal is to clean and validate the data before using it.

---

## What This Project Does

- Reads raw sales data from a CSV file  
- Standardizes date formats  
- Removes duplicate records  
- Filters invalid rows (missing values, zero or negative quantity/price)  
- Creates a clean dataset  
- Generates a data quality report  
- Logs pipeline activity  

---

## Folder Structure

day-001-sales-csv-cleaning-pipeline/
├── README.md
├── requirements.txt
├── src/
│   ├── etl_pipeline.py
│   └── config.py
├── data/
│   └── raw_sales.csv
├── output/
│   ├── clean_sales.csv
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/

---

## Tech Stack

- Python  
- Pandas  
- CSV Files  
- Logging  

---

## How to Run

1. Create virtual environment

Windows:
python -m venv venv
venv\Scripts\activate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

2. Install dependencies

pip install -r requirements.txt

3. Run the pipeline

python src/etl_pipeline.py

---

## Output

After running, check the `output/` folder:

- clean_sales.csv → cleaned data  
- data_quality_report.txt → summary of issues  
- pipeline.log → pipeline execution logs  

---

## Sample Output

order_id,order_date,customer_name,product,quantity,price,total_amount
1001,2026-04-01,Alice,Keyboard,2.0,45.5,91.0
1002,2026-04-02,Bob,Mouse,1.0,25.0,25.0
1003,2026-04-03,Charlie,Monitor,1.0,180.0,180.0
1006,2026-04-04,Frank,Keyboard,2.0,45.5,91.0
1009,2026-04-06,Helen,Headset,2.0,60.0,120.0

---

## Key Learnings

- Built a simple ETL pipeline  
- Cleaned messy real-world data  
- Applied data quality checks  
- Used logging for tracking  
- Organized project structure  

---

## Future Improvements

- Handle multiple files  
- Add JSON input  
- Load data into a database  
- Add automation and tests  