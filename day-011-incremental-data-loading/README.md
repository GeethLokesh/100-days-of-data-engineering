# 🚀 Day 11: Incremental Data Loading Pipeline

## 📌 Project Title
Incremental Data Loading Using Python and SQLite (Avoid Reprocessing Data)

---

## 📖 Project Overview

This project demonstrates how to build a production-style incremental data pipeline that loads only new data instead of reprocessing the entire dataset every time.

In real-world systems, data keeps growing daily. Reprocessing everything wastes time, increases cost, and can create duplicates. This project solves that using a watermark-based approach.

---

## ❗ Problem Statement

A company receives daily order data. Running a full load every time causes:

- Duplicate records
- Increased processing time
- Inefficient pipelines

We need a system that:

✔ Loads only new data  
✔ Tracks previously processed data  
✔ Ensures no duplicates  
✔ Maintains pipeline reliability  

---

## 🛠️ What We Are Building

We are building a Python + SQLite pipeline that:

1. Reads raw order data from CSV
2. Cleans and validates data
3. Tracks last processed timestamp (watermark)
4. Filters only new records
5. Loads new records into SQLite
6. Updates watermark after load
7. Generates data quality report
8. Logs pipeline activity

---

## 💡 Smart Enhancement

### ✅ Watermark-Based Incremental Loading

A **watermark** stores the latest processed timestamp.

On each run:
- Pipeline reads last watermark
- Loads only records where:
  
  ```
  last_updated > watermark
  ```

This avoids reprocessing old data.

---

## 🧱 Folder Structure

```
day-011-incremental-data-loading/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── orders.csv
├── output/
│   ├── incremental_load.db
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/
```

---

## 📊 Sample Input Data

`data/orders.csv`

```
order_id,customer_name,product,quantity,price,order_date,last_updated
101,John Smith,Laptop,1,900,2026-04-20,2026-04-20 10:00:00
102,Emily Davis,Mouse,2,25,2026-04-21,2026-04-21 09:30:00
103,Michael Brown,Keyboard,1,75,2026-04-22,2026-04-22 14:15:00
104,Sarah Wilson,Monitor,1,250,2026-04-23,2026-04-23 16:45:00
105,David Lee,USB Cable,3,10,2026-04-24,2026-04-24 11:20:00
```

---

## ⚙️ How the Pipeline Works

### 1. Read Data
Reads CSV file into Pandas DataFrame.

---

### 2. Clean Data
- Removes duplicates
- Converts datatypes
- Validates numeric fields
- Standardizes dates
- Removes invalid records

---

### 3. Read Watermark

Stored in SQLite table:

```
pipeline_watermark
```

If first run:

```
1900-01-01 00:00:00
```

---

### 4. Filter Incremental Data

```
SELECT records WHERE last_updated > watermark
```

Only new records are processed.

---

### 5. Load Data into SQLite

Table:

```
orders
```

Key features:
- `order_id` as PRIMARY KEY
- `INSERT OR IGNORE` prevents duplicates

---

### 6. Update Watermark

After successful load:

```
watermark = MAX(last_updated)
```

---

### 7. Generate Outputs

- Data Quality Report
- Pipeline Logs

## 🔁 How to Test Incremental Logic

### First Run

```
New records: 5
Loaded records: 5
```

---

### Second Run (No Changes)

```
New records: 0
Loaded records: 0
```

---

### Add New Record

Append to CSV:

```
106,Anna Taylor,Webcam,1,80,2026-04-25,2026-04-25 13:10:00
```

---

### Third Run

```
New records: 1
Loaded records: 1
```

---

## 📦 Output Files

```
output/
├── incremental_load.db
├── data_quality_report.txt
└── pipeline.log
```

---

## 📄 Sample Data Quality Report

```
Data Quality Report
===================

Source records read: 5
Clean records: 5
Rejected records: 0
New records: 5
Loaded records: 5

Data quality status: PASSED
```

---

## 🧠 What You Learned

- Incremental vs Full Load
- Watermark concept
- SQLite integration in pipelines
- Data validation and cleaning
- Logging and monitoring
- Preventing duplicate loads

---

## 🌍 Real-World Use Cases

This pattern is used in:

- Daily transaction pipelines
- Banking systems (new transactions)
- Healthcare claim updates
- E-commerce order ingestion
- Log/event processing systems

---

## 🔄 Tool Swap Ideas (Important for Learning)

| Current Tool | Alternative |
|-------------|------------|
| SQLite | PostgreSQL |
| Pandas | PySpark |
| CSV | API / JSON |
| Python Script | Airflow DAG |

---

## 📌 Summary

This project introduces incremental data loading using a watermark strategy. It ensures efficient processing by loading only new data, preventing duplication, and improving pipeline performance.
