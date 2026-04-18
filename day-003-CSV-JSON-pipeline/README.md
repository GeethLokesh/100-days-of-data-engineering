# Day 3: CSV to JSON Conversion Pipeline

## Project Overview

This project builds a Python ETL pipeline to convert raw CSV data into structured JSON format. The pipeline cleans, validates, and standardizes data before exporting it.

## Problem Statement

CSV files are commonly used for storing raw data, but modern data systems and APIs prefer JSON format. This project simulates a real-world ingestion process where CSV data is transformed into JSON for downstream systems.

## What This Project Does

* Reads raw CSV data
* Cleans and standardizes records
* Converts data into JSON format
* Generates:

  * Clean JSON dataset
  * Data quality report
  * Execution logs

## Tech Stack

* Python
* CSV & JSON processing
* Logging

## Folder Structure

```id="u1ss9d"
day-003-csv-to-json-pipeline/
├── README.md
├── requirements.txt
├── src/
├── data/
├── output/
└── screenshots/
```

## How to Run

```bash id="qmxm8z"
python src/pipeline.py
```

## Output

* `sales.json` → Clean structured data
* `data_quality_report.txt` → Data validation report
* `pipeline.log` → Execution logs

## Key Learning

* CSV ingestion
* Data transformation
* JSON conversion
* Data validation techniques

## Future Improvements

* Load into database
* Handle large files efficiently
* Add schema validation
