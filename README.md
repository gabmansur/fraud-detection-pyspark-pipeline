# Suspicious Transaction Detection – Prototype

This is a simple prototype that simulates how a financial institution might detect suspicious transactions using tools commonly used in data engineering. The project is not meant for production but rather to demonstrate practical knowledge of:

- Data ingestion and transformation with PySpark
- Fraud detection logic
- Testing using PyTest
- Automation of validation through CI/CD (GitHub Actions)

It is designed to align with transaction structures documented in Rabobank's developer portal.

## Purpose

This project was built in one day to demonstrate how to:

- Read and process structured financial data using PySpark
- Apply rule-based logic to detect suspicious behavior (such as high-frequency transfers)
- Validate data transformations and detection logic using PyTest
- Integrate automated testing through a CI/CD pipeline using GitHub Actions
- Simulate real-world financial monitoring processes in a clear and modular way


## Key Concepts Demonstrated

| Focus Area              | Description |
|-------------------------|-------------|
| Data transformation     | Reads a CSV file, parses timestamps, and casts data types correctly using PySpark |
| Rabobank API modeling   | Transaction data is structured based on Rabobank's PSD2 API documentation |
| Fraud detection logic   | Implements a rule to flag repeated transfers to the same IBAN in a short time window |
| Unit testing with PyTest| Validates the ETL and fraud detection logic using isolated, reusable test cases |
| CI/CD pipeline          | Uses GitHub Actions to run tests automatically on every push |
| Code structure          | Modular layout for clarity and maintainability: separate folders for data, source code, and tests |


## Tech Stack

| Layer       | Tool            |
|-------------|-----------------|
| Data engine | PySpark         |
| Testing     | PyTest          |
| Automation  | GitHub Actions  |
| Language    | Python 3.10+    |

---

## What the Code Does

1. Loads example transaction data from a CSV file
2. Transforms the data using PySpark (parsing timestamps, casting amounts)
3. Applies a fraud rule: flags accounts that make three or more transactions to the same IBAN within a five-minute window
4. Uses PyTest to validate that the transformations and logic work as expected
5. Runs all tests automatically through GitHub Actions on every commit

## Project Structure

| Path                         | Description                                        |
| ---------------------------- | -------------------------------------------------- |
| `data/transactions.csv`      | Simulated Rabobank-style transaction data          |
| `src/etl.py`                 | PySpark pipeline for loading and transforming data |
| `src/fraud_rules.py`         | Fraud rule to detect repeated IBAN transactions    |
| `tests/test_etl.py`          | PyTest test for ETL data transformation            |
| `tests/test_fraud_rules.py`  | PyTest test for fraud rule logic                   |
| `.github/workflows/test.yml` | GitHub Actions pipeline for automated testing      |
| `requirements.txt`           | Python dependencies (PySpark, PyTest)              |
| `README.md`                  | Project documentation                              |

## Sample Transaction Schema

The structure below is based on Rabobank’s PSD2 API documentation:

| Field               | Description                            |
|--------------------|----------------------------------------|
| `transaction_id`    | Unique transaction reference            |
| `account_id`        | Sender account (simulated IBAN)         |
| `timestamp`         | Date and time of the transaction        |
| `amount`            | Amount of money transferred (float)     |
| `currency`          | ISO currency code (e.g., EUR)           |
| `description`       | Description or note attached to payment |
| `counterparty_name` | Recipient’s name                        |
| `counterparty_iban` | Recipient’s IBAN                        |
| `category`          | Type of expense (e.g., crypto, travel)  |
| `payment_type`      | e.g. `single`, `bulk`, or `direct_debit`|


## Future Development (If Expanded)

If extended, the prototype could include:

- Additional fraud rules (e.g., round-number transfers, international activity)
- Integration with Delta Lake or Databricks runtime
- Ingestion from real cloud data sources (Azure Blob Storage, ADLS)
- Stream processing with Spark Structured Streaming
- Visualization of flagged transactions using Streamlit or Power BI
- Anomaly detection using ML models


## Why This Was Built

I created this project to demonstrate a complete and practical understanding of the responsibilities expected in a Data Engineering (Testing) role—particularly one involving fraud detection, data quality, and system reliability.

It is intentionally modeled after Rabobank's API and compliance ecosystem, and shows that I understand:

- How financial data flows work
- What real fraud patterns look like
- How to build reliable, testable, maintainable code around that

This was not built as a generic exercise—it is tailored to reflect a realistic, high-impact use case with clear relevance to financial institutions.
