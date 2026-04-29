# Day 13: SCD Type 2 Customer History Tracking Pipeline

## Project Overview

This project introduces Slowly Changing Dimensions Type 2 (SCD Type 2), a key concept used in data warehousing.

Unlike simple updates where old data is overwritten, SCD Type 2 keeps a full history of changes by creating new records instead of modifying existing ones.

This allows businesses to track how data evolves over time.

---

## Problem Statement

Customer information does not remain constant.

Over time:
- Customers may move to a new city
- Email addresses may change
- Membership status may be upgraded or downgraded

If we overwrite this information, we lose valuable historical insights.

For example:
- Where did the customer live last year?
- When did they upgrade membership?
- What was their previous email?

To solve this, we use SCD Type 2.

---

## What This Project Does

This pipeline processes customer data and maintains historical records.

It:
- Reads existing customer history data
- Reads new incoming customer data
- Compares both datasets using `customer_id`
- Detects changes in key fields
- Closes old records when changes are found
- Inserts new records for updated data
- Adds completely new customers
- Keeps unchanged records untouched

---

## How SCD Type 2 Works

### 1. New Customer
If a customer does not exist in history:
- A new record is inserted

### 2. No Change
If customer data has not changed:
- No update is made

### 3. Change Detected
If any tracked field changes:
- Old record is closed (`end_date` is set)
- Old record is marked as inactive (`is_current = False`)
- New record is inserted with updated data
- New record becomes active (`is_current = True`)

---

## Key Columns Explained

- `customer_id` → Unique identifier for each customer  
- `start_date` → When the record became active  
- `end_date` → When the record was closed  
- `is_current` → Indicates active record (True/False)  

---

## Tracked Fields

The pipeline checks changes in:

- Customer name  
- Email  
- City  
- Membership status  

If any of these change, a new version is created.

---

## Folder Structure

day-013-scd-type-2-history-tracking/
├── README.md  
├── requirements.txt  
├── src/  
├── data/  
├── output/  
└── screenshots/  

---

## Input Data

### Existing Data
Contains historical records with active and inactive versions.

### Incoming Data
Contains the latest customer data that needs to be processed.

---

## Output Generated

After running the pipeline:

### 1. Customer History File
Contains:
- Old records (inactive)
- New records (active)

### 2. Data Quality Report
Summarizes:
- Validation checks
- Number of changes detected
- New records added
- Unchanged records

### 3. Log File
Tracks:
- Pipeline execution steps
- Changes detected
- Errors if any

---

## Smart Enhancement

This project includes basic data quality checks:

- Validates required columns
- Checks for empty datasets
- Detects duplicate customer IDs
- Generates a summary report

This helps simulate real-world pipeline monitoring.

---

## Expected Output

The output will contain full customer history.

Example:

- Old record is closed with an end date
- New record is inserted with updated values
- Only one record per customer remains active

---

## What I Learned

- What SCD Type 2 is and why it is important  
- How to track historical data instead of overwriting  
- How to detect changes in data pipelines  
- How to manage active and inactive records  
- How real-world data warehouses maintain history  

---

## Real-World Use Cases

SCD Type 2 is widely used in:

- Customer data tracking  
- Employee role changes  
- Product pricing history  
- Account status tracking  

It helps answer business questions like:

- What changed and when?  
- What was the previous value?  
- What is the current active record?  

---

## Final Summary

This project builds a complete SCD Type 2 pipeline using Python and Pandas.

Instead of overwriting data, it preserves full history, making it a critical step toward real-world data engineering and data warehouse design.