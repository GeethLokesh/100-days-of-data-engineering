# Day 14: Surrogate Keys + Dimension Table Design (Warehouse Modeling)

---

## Project Overview

This project introduces one of the most important concepts in data warehousing: **dimension tables and surrogate keys**.

In real-world systems, data comes from multiple source systems, each with its own identifiers. These identifiers are not always reliable for analytics. To solve this, data warehouses generate their own internal identifiers called **surrogate keys**.

In this project, we build a complete mini pipeline that creates a **customer dimension table** using surrogate keys, along with cleaning, validation, logging, and reporting.

---

## Problem Statement

Customer data from source systems usually includes identifiers like:

customer_id = C001

These are called natural keys.

However, relying on them creates problems:

- IDs may change over time  
- Different systems may reuse the same IDs  
- Data integration becomes difficult  
- Historical tracking becomes unreliable  
- Joins between tables may break  

To solve this, warehouses use surrogate keys, which are system-generated unique identifiers.

---

## What We Are Building

We are building a pipeline that:

- Reads raw customer data from CSV  
- Cleans and standardizes the data  
- Removes duplicates  
- Handles missing values  
- Validates data quality  
- Creates a dimension table (dim_customer)  
- Generates a surrogate key (customer_key)  
- Saves output as CSV  
- Loads data into SQLite  
- Generates a data quality report  
- Logs the pipeline execution  

---

## Folder Structure

day-014-surrogate-keys-dimension-design/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
│   └── customers.csv
├── output/
│   ├── warehouse.db
│   ├── dim_customer.csv
│   ├── data_quality_report.txt
│   └── pipeline.log
└── screenshots/

---

## Tools Used

- Python  
- Pandas  
- SQLite  
- VS Code  
- Git  

---

## Key Concepts

### Natural Key

A natural key comes from the source system:

customer_id = C001

It has business meaning but is not fully reliable.

---

### Surrogate Key

A surrogate key is generated inside the warehouse:

customer_key = 1

It is:

- Unique  
- Stable  
- System-generated  
- Used for joins  

---

### Dimension Table

A dimension table stores descriptive data about an entity.

In this project:

dim_customer

Stores customer-related attributes like name, email, and location.

---

### Why Surrogate Keys Are Important

- Provide stable joins  
- Support historical tracking  
- Avoid dependency on source systems  
- Improve warehouse design  
- Enable scalable analytics  

---

## Input Data

Location:

data/customers.csv

Sample:

customer_id,first_name,last_name,email,city,state,signup_date
C001,John,Smith,john.smith@email.com,Dallas,TX,2024-01-10
C002,Sarah,Johnson,sarah.johnson@email.com,Austin,TX,2024-01-15
C002,Sarah,Johnson,sarah.johnson@email.com,Austin,TX,2024-01-15
C006,Lisa,Miller,,Denver,CO,2024-03-20

Data issues present:

- Duplicate rows  
- Missing email  
- Missing city/state  
- Inconsistent formatting  

---

## Pipeline Flow

### Step 1: Extract

- Read CSV using Pandas  
- Load into DataFrame  

---

### Step 2: Clean Data

- Remove duplicates  
- Standardize names (title case)  
- Fill missing values:
  - email → default value  
  - city/state → "Unknown"  
- Convert signup_date to standard format  

---

### Step 3: Validate Data

Checks:

- Missing customer_id  
- Missing email  
- Invalid dates  
- Duplicate IDs  

Issues are captured in the report.

---

### Step 4: Create Dimension Table

- Sort by customer_id  
- Generate surrogate key:

customer_key = 1, 2, 3...

- Create full_name column  
- Add created_at timestamp  

Final structure:

customer_key
customer_id
first_name
last_name
full_name
email
city
state
signup_date
created_at

---

### Step 5: Save Outputs

- Save as CSV  
- Load into SQLite database  

---

### Step 6: Data Quality Report

Includes:

- Source record count  
- Final record count  
- Duplicates removed  
- Validation issues  

---

### Step 7: Logging

Logs:

- Pipeline start and end  
- Each step execution  
- Errors if any  

Stored in:

output/pipeline.log

---

## Output Files

output/
├── warehouse.db
├── dim_customer.csv
├── data_quality_report.txt
└── pipeline.log

---

## Sample Output

customer_key,customer_id,first_name,last_name,full_name,email,city,state,signup_date,created_at
1,C001,John,Smith,John Smith,john.smith@email.com,Dallas,TX,2024-01-10,...
2,C002,Sarah,Johnson,Sarah Johnson,sarah.johnson@email.com,Austin,TX,2024-01-15,...

---

## Smart Enhancement

This project includes a **data quality report**.

This helps:

- Detect bad data early  
- Improve trust in data  
- Monitor pipeline health  
- Simulate real-world pipelines  

---

## How to Run (VS Code)

Step 1: Open folder

day-014-surrogate-keys-dimension-design

Step 2: Create environment

python -m venv venv

Step 3: Activate

venv\Scripts\activate

Step 4: Install dependencies

pip install -r requirements.txt

Step 5: Run pipeline

python src/pipeline.py

---

## Expected Result

- Cleaned dataset  
- Surrogate keys generated  
- Dimension table created  
- Data stored in SQLite  
- Data quality report generated  
- Logs created  

---

## Real-World Use Case

In real companies:

- Data comes from multiple systems  
- IDs are inconsistent  
- Reporting needs stable joins  

Solution:

- Create dimension tables  
- Use surrogate keys  
- Build clean warehouse layers  

---

## What You Learned

- Natural vs surrogate keys  
- Dimension table design  
- Data cleaning and validation  
- Pipeline structuring  
- Logging and monitoring  
- Warehouse fundamentals  

---

