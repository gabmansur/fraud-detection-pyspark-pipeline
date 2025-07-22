# 🕵️‍♀️ Suspicious Transaction Detector

A simple prototype for demonstrating **fraud detection** using **PySpark**, **PyTest**, and **CI/CD automation**.

This project simulates a lightweight version of a **transaction monitoring pipeline**, focused on detecting potentially suspicious activity based on rapid transactions within a short time window — a basic signal often used in **money laundering and fraud prevention** scenarios.

---

## 🎯 Purpose

This is a **1-day prototype** built to demonstrate my ability to:

- 💾 Ingest and transform data using **PySpark**
- 🧪 Validate logic using **unit tests with PyTest**
- 🔁 Integrate tests in a **CI/CD pipeline using GitHub Actions**
- 🔐 Simulate real-world financial risk logic like transaction spike detection

> This is not a production tool — just a compact project to showcase relevant technical and analytical skills for data engineering roles focused on **fraud detection**, **ETL reliability**, and **data pipeline testing**.

---

## 🧱 Tech Stack

| Layer       | Tool          |
|-------------|---------------|
| Data Engine | PySpark       |
| Testing     | PyTest        |
| Automation  | GitHub Actions |
| Language    | Python 3.10+  |

---

## 🧪 What It Does

- Loads example transaction data from CSV
- Transforms data (cast types, parse timestamps)
- Applies a basic **fraud rule**:  
  > Flag accounts with more than 3 transactions in 5 minutes
- Uses **PyTest** to ensure:
  - ETL transforms run correctly
  - Schema and types are as expected
  - Fraud rules flag the right rows
- Runs tests automatically on every push via **GitHub Actions**


## 📂 Project Structure
fraud-detection-pyspark-pipeline/
│
├── data/                  
│   └── transactions.csv           # Sample transaction data
│
├── src/                          
│   ├── etl.py                     # PySpark data ingestion and transformation
│   └── fraud_rules.py             # Basic fraud rule logic
│
├── tests/                        
│   ├── test_etl.py                # Unit tests for the ETL process
│   └── test_fraud_rules.py        # Unit tests for fraud detection rules
│
├── .github/
│   └── workflows/
│       └── test.yml               # CI pipeline using GitHub Actions
│
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview (this file)


## 🛣️ Future Ideas (if taken further)

- ✅ Add more advanced fraud signals (velocity, country-based anomalies)
- ✅ Integrate Delta Lake or Databricks runtime
- ✅ Load from and write to real cloud data sources (Azure Blob, ADLS)
- ✅ Add anomaly detection using basic ML/AI models
- ✅ Add alerting logic or a Streamlit dashboard for results



## ✨ Why I Built This

I'm deeply interested in the intersection of **data engineering and responsible financial systems**. I believe that robust pipelines and smart data validation can prevent real harm — not just to institutions, but to people. I built this small project to show how even a simplified system can demonstrate:

- Strategic thinking
- Technical implementation
- Data intuition