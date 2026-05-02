# Day 16: Star Schema Reporting Queries

## Project Title

Star Schema Reporting Queries

---

# Problem Statement

A business team wants to analyze sales performance by customer, product, region, and date. The data is already arranged into fact and dimension tables, but analysts need reporting queries that can answer business questions clearly.

---

# What This Project Builds

This project builds a small local reporting pipeline using Python, Pandas, SQLite, and SQL.

The pipeline creates a simple star schema with:

- Customer dimension
- Product dimension
- Date dimension
- Sales fact table

Then it runs reporting queries and exports the results as CSV files.

---

# Folder Structure

```text
day-016-star-schema-reporting-queries/
├── README.md
├── requirements.txt
├── src/
│   └── pipeline.py
├── data/
├── output/
└── screenshots/
```

---

# Tools Used

- Python
- Pandas
- SQLite
- SQL
- VS Code
- Logging

---

# Why Star Schema Matters

A star schema is commonly used in data warehouses because it separates business events from descriptive details.

In this project:

- `fact_sales` stores measurable business activity
- `dim_customers` stores customer details
- `dim_products` stores product details
- `dim_dates` stores date details

This makes reporting easier and cleaner.

---

# Reports Generated

The pipeline creates these reports:

1. Sales by region
2. Sales by product category
3. Daily sales report
4. Top customers by sales

---

# Smart Enhancement

This project includes a query validation report.

The validation report checks whether each reporting query returned data. This helps catch reporting issues where a SQL query runs but produces no useful output.

---

# Step-by-Step Pipeline Flow

## Step 1: Create Sample Dimension Tables

The pipeline first creates dimension tables:

### Customer Dimension
Stores customer details such as:
- customer name
- city
- region

### Product Dimension
Stores product information such as:
- product name
- category

### Date Dimension
Stores reporting-friendly date attributes such as:
- full date
- month
- year

These dimensions help organize reporting data cleanly.

---

## Step 2: Create Fact Table

The fact table stores measurable business transactions.

In this project:
- quantity sold
- sales amount
- foreign keys connecting dimensions

The fact table links to all dimensions using surrogate keys.

---

## Step 3: Load Data into SQLite

The pipeline loads all dimension and fact tables into SQLite.

Tables created:

```sql
dim_customers
dim_products
dim_dates
fact_sales
```

This simulates a small warehouse-style reporting database.

---

## Step 4: Run Reporting Queries

The pipeline executes SQL reporting queries using joins between the fact and dimension tables.

Example business reports:

### Sales by Region
Calculates:
- total sales
- total quantity
- total orders

Grouped by customer region.

### Sales by Product Category
Shows which product categories generate the most revenue.

### Daily Sales Report
Tracks sales day by day.

### Top Customers
Finds highest revenue customers.

---

# SQL Concepts Learned

This project teaches important SQL warehouse concepts:

- JOIN operations
- GROUP BY
- Aggregations
- SUM()
- COUNT()
- ORDER BY
- LIMIT
- Fact-to-dimension relationships

These are heavily used in real reporting systems.

---

# Why Fact and Dimension Tables Are Important

Instead of storing everything in one large messy table:

- Fact tables store measurements
- Dimension tables store descriptions

Benefits:
- easier reporting
- faster analytics
- cleaner schema
- reusable business logic
- scalable warehouse design

This is the foundation of Snowflake, Synapse, Redshift, and BigQuery warehouse modeling.

---

# Logging

The pipeline generates:

```text
pipeline.log
```

Logging tracks:
- pipeline start
- data loading
- report generation
- validation checks
- pipeline completion
- errors if any occur

Logging is extremely important in production pipelines because it helps engineers trace failures quickly.

---

# Query Validation Report

The pipeline creates:

```text
query_validation_report.txt
```

The validation report checks:
- whether reports returned rows
- whether reporting queries produced output

This simulates basic reporting quality monitoring used in real data platforms.

---

# Output Files Generated

After running the pipeline, the `output` folder will contain:

```text
star_schema_sales.db
sales_by_region.csv
sales_by_product_category.csv
daily_sales_report.csv
top_customers.csv
query_validation_report.txt
pipeline.log
```

---

# Example Reporting Logic

## Sales by Region

Example output:

| Region | Total Sales |
|---|---|
| East | 1200 |
| West | 900 |
| South | 500 |

This helps businesses understand which regions perform best.

---

## Top Customers Report

Example output:

| Customer | Total Sales |
|---|---|
| John Smith | 1500 |
| Maria Garcia | 1200 |

This helps identify high-value customers.

---

# Real-World Use Case

This project simulates how analytics teams generate reports from warehouse tables.

Real companies use similar reporting logic for:

- finance reporting
- sales dashboards
- KPI tracking
- customer analytics
- executive reporting
- operational analytics

Warehouse reporting is one of the most common responsibilities of data engineers.

---

# How to Run This Project

## Step 1: Open VS Code

Open your main:

```text
100-days-of-data-engineering
```

folder.

---

## Step 2: Move into Day 16 Folder

```bash
cd day-016-star-schema-reporting-queries
```

---

## Step 3: Activate Virtual Environment

```bash
..\venv\Scripts\activate
```

---

## Step 4: Install Requirements

```bash
pip install -r requirements.txt
```

---

## Step 5: Run Pipeline

```bash
python src/pipeline.py
```

---

# Expected Terminal Output

```text
Pipeline completed successfully.
Reports created in: output/
```

---

# What I Learned

In this project, I learned how to:

- Build warehouse-style schemas
- Create fact and dimension tables
- Write reporting SQL queries
- Join tables using surrogate keys
- Generate business reports
- Export reporting outputs
- Validate reporting queries
- Add logging into reporting pipelines

---

# Tool Swaps (VERY IMPORTANT FOR LEARNING)

This same project can later be built using larger enterprise tools.

| Current Tool | Enterprise Alternative |
|---|---|
| SQLite | PostgreSQL |
| Pandas | PySpark |
| Local CSV Reports | Power BI |
| Local Database | Snowflake |
| Python Scripts | Airflow |
| Local Storage | AWS S3 / ADLS |

---

# Future Improvement Ideas

Later you can extend this project with:

- Slowly Changing Dimensions
- Incremental warehouse loading
- Airflow orchestration
- Power BI dashboards
- dbt transformations
- Partitioned warehouse tables
- Cloud warehouse simulation

---

# Final Summary

This project introduced warehouse-style reporting using star schema design.

You learned:
- how fact and dimension tables work together
- how SQL reporting queries are written
- how business metrics are calculated
- how reporting pipelines generate outputs
- how warehouse modeling improves analytics

This is one of the most important foundational concepts in modern data engineering and analytics engineering.