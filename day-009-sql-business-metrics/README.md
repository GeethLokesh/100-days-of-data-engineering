# Day 9: Sales KPI Reporting with SQL Aggregations

## Project Title

Sales KPI Reporting with SQL Aggregations

---

## Problem Statement

Businesses generate large volumes of sales transaction data daily, but raw data alone is not useful for decision-making. Stakeholders need summarized insights such as total revenue, number of orders, customer activity, category performance, and product rankings.

This project focuses on transforming raw sales data into meaningful business metrics using SQL aggregation logic, while also ensuring reliability through logging and data quality validation.

---

## What We Are Building

We are building a mini reporting pipeline that:

* takes raw sales data
* loads it into a SQLite database
* runs SQL aggregation queries
* generates business KPI reports
* creates a data quality report
* logs pipeline execution

This simulates a real-world reporting workflow used by analytics and business teams.

---

## Folder Structure

```
day-009-sql-business-metrics/
├── README.md
├── requirements.txt
├── src/
├── data/
├── output/
└── screenshots/
```

---

## Tools Used

* Python
* Pandas
* SQLite
* SQL
* VS Code
* Logging

---

## Skills Covered

* SQL aggregations
* GROUP BY operations
* SUM, COUNT, AVG functions
* ORDER BY for sorting
* LIMIT for top results
* Business KPI reporting
* SQLite-based reporting workflows
* Logging in pipelines
* Data quality validation

---

## Project Flow

### Step 1: Data Creation

Sample sales transaction data is created and stored in a CSV file.

### Step 2: Data Loading

The CSV data is loaded into a SQLite database table.

### Step 3: SQL Aggregation

SQL queries are executed to calculate business metrics.

### Step 4: Report Generation

Each query result is saved as a report file.

### Step 5: Data Quality Checks

Validation checks are performed to ensure data correctness.

### Step 6: Logging

All pipeline steps are logged for monitoring and debugging.

---

## Reports Generated

### 1. KPI Summary

Provides an overall business view including:

* total number of orders
* total number of customers
* total items sold
* total revenue
* average order value

Used by managers for quick decision-making.

---

### 2. Revenue by Category

Shows performance of each product category based on:

* total quantity sold
* total revenue generated

Helps identify high-performing and low-performing categories.

---

### 3. Top Products

Lists top 5 products based on revenue.

Helps answer:

* which products generate the most revenue
* what products should be promoted

---

### 4. Sales by Payment Method

Breaks down sales by payment type:

* number of orders per payment method
* revenue contribution of each method

Useful for understanding customer payment behavior.

---

## Data Quality Report

A separate report is generated to validate the data before trusting outputs.

### Checks included:

* null values in important fields
* duplicate order IDs
* invalid quantity values (zero or negative)
* invalid unit price values

### Why this matters:

Even if the pipeline runs successfully, poor data quality can lead to incorrect business decisions.
This report ensures that the data is reliable before reporting.

---

## Logging

A log file is created to track pipeline execution.

### Logging captures:

* pipeline start and completion
* database connection status
* report generation steps
* data quality check execution
* any errors during execution

### Why logging is important:

* helps debug pipeline failures
* helps trace issues step by step
* improves pipeline monitoring

---

## Expected Output

After running the project, the `output/` folder will contain:

* SQLite database file
* KPI summary report
* revenue by category report
* top products report
* sales by payment method report
* data_quality_report.txt
* pipeline.log

---

## Real-World Use Case

This project reflects how data engineers support business reporting in real organizations.

Common use cases include:

* finance reporting
* sales dashboards
* product performance analysis
* customer insights
* operational reporting

Instead of giving raw data, engineers provide aggregated, clean, and validated datasets.

---

## What You Learn From This Project

* how to transform raw transactional data into business metrics
* how SQL aggregations are used in real reporting
* how to structure reporting pipelines
* how to add logging to track pipeline execution
* how to validate data before trusting results
* how to generate multiple reporting outputs

---

## Difference Between Day 8 and Day 9

Day 8 focused on learning SQL queries and transformations.

Day 9 focuses on using SQL to answer business questions and generate reporting outputs.

This is an important shift from data handling to business analytics.

---

## Future Improvements

This project can be extended by:

* adding date-based reporting (daily, monthly trends)
* using PostgreSQL instead of SQLite
* scheduling the pipeline
* connecting reports to Power BI or Tableau
* adding more advanced data quality checks
* building dashboards on top of the outputs

---

## Conclusion

This project demonstrates how raw sales data can be transformed into meaningful business insights using SQL aggregation techniques.

By combining reporting logic, logging, and data quality checks, it provides a strong foundation for real-world data engineering workflows.
