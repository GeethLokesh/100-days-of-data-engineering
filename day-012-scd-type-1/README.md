# 🚀 Day 12: Customer Dimension Update Pipeline using SCD Type 1

## 📌 Project Overview

This project demonstrates **Slowly Changing Dimension Type 1 (SCD Type 1)** using Python and SQLite.

In data engineering, dimension tables store descriptive data such as customer, product, or employee information. These values can change over time.

SCD Type 1 is used when:

* Only the **latest data matters**
* Old data is **overwritten**
* No historical tracking is required

---

## ❗ Problem Statement

A company receives daily customer updates.

Some customers already exist but their details change:

* Email
* City
* Phone number

Some customers are new.

The business requirement:

* Keep only the **latest customer data**
* Do not store historical versions

---

## 🛠️ What We Are Building

A complete ETL pipeline that:

1. Reads incoming customer data from CSV
2. Loads existing customer data into SQLite
3. Applies **SCD Type 1 logic**
4. Updates existing customers
5. Inserts new customers
6. Generates:

   * Final dimension table
   * Data quality report
   * Pipeline logs

---

## 📁 Folder Structure

```
day-012-scd-type-1/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── customer_updates.csv
├── output/
└── screenshots/
```

---

## 📥 Input Data

File: `data/customer_updates.csv`

```csv
customer_id,customer_name,email,city,phone
1,John Smith,john.new@example.com,Dallas,111-222-3333
2,Sarah Lee,sarah@example.com,Chicago,222-333-4444
3,Michael Brown,michael@example.com,New York,333-444-5555
4,Emma Wilson,emma@example.com,Seattle,444-555-6666
```

---

## ⚙️ SCD Type 1 Logic

For each incoming record:

### If customer exists

→ Update existing record with new values

### If customer does not exist

→ Insert new record

---

## 🔄 Example

### Before Update

```
customer_id = 1
email = john.old@example.com
city = Austin
phone = 999-999-9999
```

### Incoming Data

```
customer_id = 1
email = john.new@example.com
city = Dallas
phone = 111-222-3333
```

### After SCD Type 1

```
customer_id = 1
email = john.new@example.com
city = Dallas
phone = 111-222-3333
```

Old data is overwritten.

---

## 🧠 Smart Enhancement

This project includes:

* Data quality checks
* Duplicate handling
* Missing value validation
* Logging
* Final data export

---

## 📊 Data Quality Checks

The pipeline validates:

* Total records
* Missing customer IDs
* Duplicate customer IDs
* Missing emails
* Valid records count

Output file:

```
output/data_quality_report.txt
```

---

## 📤 Output Files

After running:

```
output/
├── customer_dimension.db
├── final_customer_dimension.csv
├── data_quality_report.txt
└── pipeline.log
```

---

## 📈 Final Output Example

```csv
customer_id,customer_name,email,city,phone,updated_at
1,John Smith,john.new@example.com,Dallas,111-222-3333,...
2,Sarah Lee,sarah@example.com,Chicago,222-333-4444,...
3,Michael Brown,michael@example.com,New York,333-444-5555,...
4,Emma Wilson,emma@example.com,Seattle,444-555-6666,...
```

* Existing customers are updated
* New customers are inserted

---

## 🧰 Tools Used

* Python
* Pandas
* SQLite
* VS Code
* Git

---

## ❓ Why SQLite

SQLite is:

* Lightweight
* Easy to use
* No server setup required

In real-world systems, this would be replaced with:

* PostgreSQL
* Snowflake
* Databricks

---

## ▶️ How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run pipeline

```bash
python src/pipeline.py
```

OR

```bash
python day-012-scd-type-1/src/pipeline.py
```

---

## 💡 What You Learned

* Dimension tables
* SCD Type 1 concept
* Insert vs Update logic
* Data validation
* Logging in pipelines
* SQLite integration with Python

---

## 🌍 Real-World Use Cases

SCD Type 1 is used when history is not required:

* Customer contact updates
* Address corrections
* Product data fixes
* Employee detail updates

---

## 🔁 Tool Swaps (Important)

* SQLite → PostgreSQL (multi-user systems)
* SQLite → Snowflake (use MERGE)
* Pandas → PySpark (large datasets)
* Local files → Cloud storage (S3, ADLS)

---

## 🧾 Summary

This project builds a **customer dimension pipeline** using SCD Type 1.

* Reads data
* Validates records
* Updates existing customers
* Inserts new customers
* Exports final dataset

This is a **core data warehousing concept** used in real-world pipelines.

