# Day 20: Source-to-Target Data Reconciliation with Validation and Mismatch Reporting

## Project Overview

This project compares source data and target data to verify whether the target system has loaded the correct records.

In real data engineering work, data is often extracted from a source system and loaded into a target system such as a database, data warehouse, or reporting layer. After the load is complete, data engineers perform reconciliation to confirm that the target data matches the source data.

This project uses two CSV files:

- Source orders data
- Target orders data

The pipeline compares both files and creates reconciliation output files showing matched records, mismatched records, missing records, and extra records.

---

## Problem Statement

A company loads order data from a source system into a target reporting system. The data engineering team needs to verify whether the target data matches the source data.

The team wants to know:

- Did all source records reach the target?
- Are there any missing records in the target?
- Are there any extra records in the target?
- Did any field values change during loading?
- Is the reconciliation passed or failed?

---

## What This Project Builds

This project builds a Python reconciliation pipeline that:

1. Reads source and target CSV files
2. Validates whether both files have matching columns
3. Compares source and target record counts
4. Identifies records missing in the target
5. Identifies extra records in the target
6. Compares field-level values for common records
7. Generates mismatch reports
8. Creates a reconciliation summary report
9. Writes pipeline execution logs

---

## Folder Structure

day-020-source-to-target-reconciliation/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   ├── source_orders.csv
│   └── target_orders.csv
├── output/
│   ├── matched_records.csv
│   ├── mismatched_records.csv
│   ├── missing_in_target.csv
│   ├── extra_in_target.csv
│   ├── reconciliation_report.txt
│   └── pipeline.log
└── screenshots/

---

## Files Used

### source_orders.csv
This file represents the original source data.

### target_orders.csv
This file represents the data loaded into the target system.

---

## Key Concept: Source-to-Target Reconciliation

Source-to-target reconciliation means comparing data from the original source system with data loaded into the target system.

The goal is to confirm that the target data is complete, accurate, and consistent.

Example:

Source System → Target System → Reconciliation Check

If the data matches, reconciliation passes.

If records are missing, extra, or changed, reconciliation fails.

---

## Why Reconciliation Is Important

Reconciliation is important because data pipelines can fail silently.

A pipeline may run successfully but still produce incorrect data due to:

- Missing records
- Duplicate records
- Partial loads
- Changed values
- Source system issues
- Transformation mistakes
- Incorrect joins
- Manual file changes

Without reconciliation, incorrect data may reach dashboards, reports, or business users.

---

## Smart Enhancement Added

Validation summary + mismatch reporting

The pipeline does not just compare record counts. It also identifies exact records and exact fields where mismatches happened.

---

## Validation Checks Performed

The pipeline performs these checks:

1. Column validation
2. Source record count check
3. Target record count check
4. Missing records check
5. Extra records check
6. Field-level mismatch check
7. Final reconciliation status check

---

## Technologies Used

- Python
- Pandas
- CSV files
- Logging
- File-based reconciliation reports

---

## How the Pipeline Works

### Step 1: Read Source and Target Data
The pipeline reads both CSV files from the data folder.

### Step 2: Validate Columns
Checks whether both files have the same columns before comparison.

### Step 3: Merge Data
Uses order_id as the key and performs an outer join.

### Step 4: Identify Missing Records
Records in source but not in target → missing_in_target.csv

### Step 5: Identify Extra Records
Records in target but not in source → extra_in_target.csv

### Step 6: Identify Field-Level Mismatches
Compares values column by column and stores mismatches.

### Step 7: Save Matched Records
Perfectly matching records are saved.

### Step 8: Generate Report
Creates reconciliation_report.txt with summary.

---

## How To Run This Project

### Step 1: Open Folder in VS Code
Open the project folder.

### Step 2: Create Virtual Environment
python -m venv venv

### Step 3: Activate Environment
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

### Step 4: Install Requirements
pip install -r requirements.txt

### Step 5: Run Pipeline
python src/pipeline.py

---

## Expected Output

Output folder will contain:

- matched_records.csv
- mismatched_records.csv
- missing_in_target.csv
- extra_in_target.csv
- reconciliation_report.txt
- pipeline.log

---

## Expected Reconciliation Summary

Reconciliation Status: FAILED

Total Source Records: 6  
Total Target Records: 5  
Matched Records: 2  
Mismatched Records: 2  
Missing in Target: 2  
Extra in Target: 1  

---

## Why the Reconciliation Failed

- Order 1002 has different order_amount
- Order 1004 has different order_status
- Orders 1005 and 1006 are missing in target
- Order 1007 is extra in target

---

## Output File Explanation

matched_records.csv → perfectly matching records  
mismatched_records.csv → same records but different values  
missing_in_target.csv → records missing in target  
extra_in_target.csv → extra records in target  
reconciliation_report.txt → summary report  
pipeline.log → execution logs  

---

## Real-World Use Case

Used in:

- Source to data warehouse validation
- ETL pipeline verification
- Finance reporting checks
- Healthcare reporting systems
- Data migration validation
- Dashboard data accuracy checks

This ensures business users always see correct and trusted data.

---

## What I Learned

- How to compare source and target datasets
- How to validate schema consistency
- How to detect missing and extra records
- How to identify field-level mismatches
- How to build reconciliation reports
- How to implement logging in pipelines
- How real-world data validation works in production systems

---

