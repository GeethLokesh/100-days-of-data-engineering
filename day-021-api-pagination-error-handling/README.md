# Day 21: API Data Ingestion with Pagination and Error Handling

## Project Overview

This project demonstrates how to build a beginner-friendly API ingestion pipeline using Python.

In real-world data engineering, APIs often return data in multiple pages instead of sending everything in one request. This project shows how to collect paginated API data, handle temporary API errors, validate the data, and save clean output files.

---

# Problem Statement

A business team wants to collect post data from an external API for reporting and analysis. The API returns data in pages, so the pipeline must fetch all pages, handle request failures, validate the records, and store the final clean dataset.

---

# What This Project Does

This pipeline:

- Connects to a public API
- Fetches records using pagination
- Retries failed API requests
- Saves raw API data as JSON
- Cleans and validates the data
- Removes duplicate records
- Saves clean data as CSV
- Creates a data quality report
- Logs pipeline execution details

---

# Folder Structure

```text
day-021-api-pagination-error-handling/
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
- Requests
- Pandas
- JSON
- CSV
- Logging
- VS Code

---

# Why Pagination Is Important

APIs usually do not return all data at once. They split data into smaller pages to improve performance and avoid large responses.

Example:

```text
Page 1: records 0 to 24
Page 2: records 25 to 49
Page 3: records 50 to 74
Page 4: records 75 to 99
```

In this project, the pipeline keeps requesting the next page until no more records are returned.

---

# Why Error Handling Is Important

In real-world systems:

- APIs may temporarily fail
- Network issues can happen
- Timeouts may occur
- Servers may become unavailable

A good data pipeline should not fail immediately.

This project uses retry logic:

```python
MAX_RETRIES = 3
```

If the API request fails, the pipeline retries automatically before stopping.

This makes pipelines more reliable in production environments.

---

# Smart Enhancement Added

This project includes:

- Retry-based error handling
- Logging system
- Data quality validation
- Duplicate removal

These are real-world data engineering practices commonly used in production pipelines.

---

# Pipeline Flow

## Step 1: Connect to API

The pipeline connects to:

```text
https://jsonplaceholder.typicode.com/posts
```

---

## Step 2: Fetch Data Using Pagination

Instead of requesting all records at once, the pipeline fetches records page by page.

Example:

```python
params = {
    "_start": start,
    "_limit": limit
}
```

`_start` controls where the page begins.

`_limit` controls how many records are fetched.

---

## Step 3: Retry Failed Requests

If the API call fails:

- Error is logged
- Pipeline waits for 2 seconds
- Retries again

Example:

```python
time.sleep(RETRY_DELAY_SECONDS)
```

---

## Step 4: Save Raw API Data

Raw API response is stored in:

```text
output/raw_api_posts.json
```

This is important because raw data should always be preserved for debugging and reprocessing.

---

## Step 5: Validate and Clean Data

The pipeline checks for:

- Missing columns
- Missing values
- Duplicate records

Then it:

- Removes duplicates
- Removes invalid rows
- Cleans text fields

---

## Step 6: Save Clean Data

Clean records are saved into:

```text
output/clean_posts.csv
```

---

## Step 7: Generate Data Quality Report

The pipeline creates:

```text
output/data_quality_report.txt
```

The report contains:

- Total records received
- Duplicate records removed
- Missing value counts
- Final clean records count

---

## Step 8: Logging

Pipeline logs are stored in:

```text
output/pipeline.log
```

Logs help data engineers:

- Monitor pipelines
- Debug failures
- Track reruns
- Identify API issues

---

# Expected Output

Terminal output:

```text
Pipeline completed successfully
Raw data saved to: output/raw_api_posts.json
Clean data saved to: output/clean_posts.csv
Data quality report saved to: output/data_quality_report.txt
```

---

# Output Files

```text
output/
├── raw_api_posts.json
├── clean_posts.csv
├── data_quality_report.txt
└── pipeline.log
```

---

# Data Quality Checks

The pipeline validates:

- Total records received
- Duplicate records
- Missing userId values
- Missing id values
- Missing title values
- Missing body values
- Final clean records saved

---

# Key Concepts Learned

In this project, you learned:

- API ingestion
- Pagination handling
- Retry logic
- Error handling
- Logging
- Data validation
- Raw vs clean data layers
- JSON processing
- CSV output generation

---

# Real-World Use Cases

This type of pipeline is commonly used for:

- Social media data ingestion
- Financial transaction APIs
- Healthcare API integrations
- Weather data collection
- E-commerce product ingestion
- Third-party SaaS integrations

---

# Tool Swaps For Learning

| Current Tool | Alternative Tool | Usage |
|---|---|---|
| Requests | httpx | Faster async API requests |
| Pandas | Polars | Faster dataframe processing |
| CSV | PostgreSQL | Store structured records in database |
| JSON File | MongoDB | Store semi-structured API data |
| Logging Module | Loguru | Advanced logging system |
| Script Pipeline | Airflow DAG | Workflow orchestration |

---

# What Makes This a Data Engineering Project

This is not just API calling.

This project demonstrates actual data engineering concepts:

- Ingestion pipelines
- Pagination control
- Retry mechanisms
- Pipeline reliability
- Data quality validation
- Logging and monitoring
- Raw and clean data separation

These concepts are heavily used in production systems.

---

# Final Learning Summary

By completing this project, you now understand:

- How APIs provide paginated data
- How engineers fetch large datasets safely
- Why retry logic matters
- Why logging is critical
- Why raw data should always be stored
- How validation protects downstream systems
- How production pipelines become reliable

This project introduces real-world ingestion engineering practices used in enterprise systems.