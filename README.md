# 🕵️‍♀️ Fraud Detection with PySpark – Local Dev Prototype on Ubuntu (WSL2)

This is a clean and testable fraud detection prototype, built locally using PySpark and Ubuntu (via WSL2). It simulates how financial institutions could monitor transactions for suspicious activity while showing off a scalable, modular, and developer-friendly pipeline.

## Table of Contents

- [Overview](#overview)
- [Why This Project](#why-this-project)
- [Architecture](#architecture)
- [Pipeline Flow](#pipeline-flow)
- [Key Features](#key-features)
- [Setup & Usage](#setup--usage)
- [Fraud Detection Rules](#fraud-detection-rules)
- [Tests](#tests)
- [Output](#output)
- [Future Improvements](#future-improvements)
- [FAQ](#faq)

## Overview

This pipeline ingests transaction data, applies transformations, and flags potential fraudulent behavior based on frequency-based rules. It ends with visualizations that help explore anomalies in transaction patterns over time and volume.

Built as a hands-on prototype to demonstrate:

- Data engineering with PySpark
- Testing and transformation logic
- Visualization of suspicious behaviors
- Modular structure for future expansion

## Why This Project

Designed to simulate responsibilities in a real financial data engineering role, especially for domains like:

- Fraud detection
- Anti-money laundering (AML)
- Transaction monitoring
- Real-time alerting systems

The goal was to build something functional, readable, and portable—without relying on large infrastructure or cloud components.

## Architecture

```text
fraud-detection-pyspark-pipeline/
│
├── .github/workflows/         ← GitHub Actions CI setup
│   └── test.yml               ← CI pipeline for automated testing
│
├── artifacts/                 ← Generated output files
│   ├── output.csv             ← Transformed transaction data
│   ├── output.parquet         ← Parquet format output
│   └── transaction_distribution.png  ← Visual distribution of transaction amounts
│
├── data/
│   └── transactions.csv       ← Raw input transaction data
│
├── output/                    ← Optional output folder if separated
│
├── src/                       ← Source code for data pipeline
│   ├── __init__.py
│   ├── etl.py                 ← PySpark ETL logic
│   ├── fraud_rules.py         ← Fraud detection rule logic
│   └── visualize.py           ← Transaction visualization logic
│
├── tests/                     ← Unit tests using Pytest
│   ├── conftest.py            ← Pytest shared fixtures
│   ├── test_etl.py            ← Tests for ETL logic
│   └── test_fraud_rules.py    ← Tests for fraud rules
│
├── .venv/                     ← Virtual environment (excluded in version control)
│
├── Makefile                   ← CLI workflow commands (run, test, freeze, visualize, etc.)
├── requirements.txt           ← Frozen Python dependencies
└── README.md                  ← Project documentation
```

## Pipeline Flow

The local data pipeline follows this flow:

1. **Load Raw Data**  
   CSV file from `data/transactions.csv` is read into a PySpark DataFrame.

2. **ETL Transformations**  
   Performed in [`etl.py`](src/etl.py), including:
   - Timestamp parsing
   - Missing value handling
   - Column normalization
   - Saving to `.csv` and `.parquet`

3. **Fraud Detection**  
   [`fraud_rules.py`](src/fraud_rules.py) applies multiple fraud-detection rules, returning filtered suspicious entries.

4. **Visualization**  
   [`visualize.py`](src/visualize.py) creates plots from the transformed data and saves them to `artifacts/`.

5. **Optional HTML Report**  
   Via Jupyter Notebook in `notebooks/final_report.ipynb`, executed using `make report`.


## Key Features

- **Modular Design**: Each step is isolated (ETL, rules, visualization)
- **Multiple Fraud Rules**: Combines time-based, value-based, and frequency-based filters
- **Seaborn Visualizations**: Clean and informative plots
- **Unit Tested**: Includes tests with `pytest` to ensure pipeline reliability
- **Makefile Shortcuts**: Clean dev flow using `make run`, `make visualize`, etc.
- **Environment Portability**: Works inside WSL2 using `.venv`


## Setup and Usage

1. Clone and Initialize
```bash

git clone https://github.com/your-username/fraud-detection-pyspark-pipeline.git
cd fraud-detection-pyspark-pipeline
python3 -m venv .venv
source .venv/bin/activate  # WSL/Linux
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Run the Pipeline
```bash
make transform         # Run ETL
make fraud             # Apply fraud rules
make visualize         # Generate visual report
make test              # Run unit tests

or run it all:
make all
```

## Fraud Detection Rules

The pipeline includes four initial fraud detection rules, all defined in [`src/fraud_rules.py`](src/fraud_rules.py). Each rule is modular and easy to extend or modify.

| Rule Name             | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `high_value`          | Flags any transaction with an amount greater than €10,000                   |
| `weekend_transaction`| Flags transactions occurring on Saturday or Sunday                          |
| `rapid_repeated`      | Detects ≥3 transfers to the same IBAN within a 5-minute sliding window      |
| `unusual_time`        | Flags transactions made between 00:00 and 06:00                             |

> Each rule returns a filtered DataFrame containing only the suspicious entries matching that rule. These are then combined and deduplicated for final analysis and visualization.

You can easily add new rules by defining a new function in `fraud_rules.py` that:
1. Accepts a `DataFrame` as input
2. Applies a filtering condition
3. Returns a suspicious subset of transactions

## Tests


All unit tests are located in the [`tests/`](tests/) folder and follow the `pytest` framework.

```bash
make test
```

| File                        | What it Tests                                 |
|-----------------------------|-----------------------------------------------|
| `tests/test_etl.py`         | ETL pipeline logic, data types, null handling |
| `tests/test_fraud_rules.py` | All individual fraud detection rules          |
| `tests/conftest.py`         | Shared fixtures and mock data                 |

## Coverage

- Ensures ETL produces valid, clean DataFrames  
- Verifies fraud rules return expected suspicious transactions  
- Tests run fast and are isolated for local development  
- Works with GitHub Actions CI (`.github/workflows/test.yml`)


## Output

Artifacts are automatically saved to the `artifacts/` directory upon pipeline execution.

| File                                     | Description                                  |
|------------------------------------------|----------------------------------------------|
| `artifacts/output.csv`                   | Cleaned + transformed transactions (CSV)     |
| `artifacts/output.parquet`               | Same data in Parquet format (for big data)   |
| `artifacts/transaction_distribution.png` | Histogram of transaction amounts (Seaborn)   |
| `artifacts/final_report.html`            | Rendered Jupyter notebook report (optional)  |

To regenerate the output files manually:

```bash
make visualize
make report
```

## Future Improvements

This project can be extended in multiple directions to increase robustness, scalability, and coverage:

- **Additional Fraud Rules**  
  Implement more sophisticated rules (e.g., sudden location changes, round-amount transfers, account velocity) using a rules engine or ML model.

- **Real-time Streaming Support**  
  Migrate from batch processing to real-time detection using Spark Structured Streaming and Kafka/EventHub.

- **Dashboards & Alerts**  
  Integrate live dashboards (e.g., Power BI, Grafana) and real-time fraud alerts via email, Slack, or webhook.

- **Enhanced Test Coverage**  
  Expand test coverage with property-based testing, data fuzzing, and integration tests.

- **CI/CD Enhancements**  
  Add automated linting, coverage reporting, and Docker-based deployment for production readiness.

- **Data Versioning**  
  Integrate with tools like DVC or Delta Lake to track data lineage and model versions.

- **Anomaly Detection with Machine Learning**  
  Introduce unsupervised ML techniques to detect novel fraud patterns beyond rule-based logic.

- **Support for Multiple Input Sources**  
  Generalize the pipeline to support additional data formats (e.g., JSON, Parquet) and APIs.

- **User Behavior Modeling**  
  Build user-level profiling to detect behavior deviation over time.


## FAQ

❓ Why did you build this project?

To demonstrate how to
- Design and execute a modular, testable, end-to-end PySpark pipeline
- Translate business needs (fraud detection, compliance) into scalable logic
- Showcase technical breadth and strategic thinking — from data transformation to stakeholder-ready visualizations
- Also, to prove that you don’t need a 100-man team and five microservices to make something robust and useful.

❓ Why fraud detection?

Because it matters. Whether it’s compliance, transaction monitoring, or anti-money laundering, fraud detection is a clear, high-impact example of how data pipelines serve real-world risk mitigation. Also? It’s fun to model patterns that seem almost human in their sneakiness, lol

❓ Why PySpark?

It’s used in production environments by banks, fintechs, and data platforms I’d love to work with. It scales, it’s testable, and you can build elegant workflows with it. Real pipelines aren’t pandas-only and I wanted to show comfort in distributed contexts.

❓Why not go bigger?

The goal wasn’t “build the next Palantir.” It was to:
- Focus on quality over quantity
- Keep it clean and local, no unnecessary cloud complexity for a prototype
- Keep the cognitive load low for reviewers (you)

❓ Why the notebook report and Seaborn plots?

Because technical stakeholders need validation, and business stakeholders want to see something. The final_report.html and the distribution chart serve both ends of the spectrum. Also, visual context is crucial when interpreting thresholds or rule sensitivity.

❓Why Makefile + venv + WSL2?
I wanted a workflow that:

- Runs the same way every time — no surprises
- Doesn’t require an IDE or heavy config
- Shows environment maturity and cross-platform portability
- Also: fewer buttons, more predictability.

❓What’s the business value?

- For banks like Rabobank:
   - These pipelines form the backbone of regulatory compliance systems
   - Rules like these contribute to real-time fraud alerts and monitoring workflows
   - The project simulates a simplified but extendable version of what could plug into transaction surveillance tooling
- For teams:
   - Demonstrates the crossover of an engineer and a strategist
   - Clear documentation and modular design mean it can scale, be explained, and be owned

❓Why didn’t you use machine learning?

Because not every problem is a job interview for an XGBoost model. Most fraud detection in production still relies on heuristic and rules-based systems especially for explainability, auditability, and integration with legacy systems. This prototype follows that philosophy: use what works, build confidence first, then layer on the complexity if and when it's needed.

❓How would you productionize this?
In phases:
1. Infrastructure: Containerize the jobs, deploy on Airflow or Databricks for orchestration.
2. Monitoring: Add logging to a central system (e.g., ELK or Azure Monitor), plus basic rule alerting.
3. Integration: Wrap fraud rules into a REST API or push to a message bus for real-time streaming ingestion.
4. Governance: Schema evolution, version control for rules, and alerts for drift or logic fatigue.
5. Scaling: Move from local to cluster-ready Spark jobs (easy thanks to PySpark's portability).

❓Why is there a Makefile in a Spark project?

Because I believe the command line should feel like a conversation, not a battle.
Also, I have better things to do than remember 6 flags every time I want to test something. Like giving Tom and Mia attention and drinking 5 cups of coffee per day

❓What surprised you while building this?

I'd say more like want to sit and cry with how much time I lost battling Windows instead of writing code. Between weird python3 alias issues, pip behaving like it was on vacation, and file paths deciding to rebel, I quickly learned that trying to do data engineering on native Windows is like trying to run a marathon in flip-flops.

![aaaaaaa](meme.png)

Switching to Ubuntu via WSL2 felt like moving from dial-up to fiber. Suddenly dependencies just worked, PySpark behaved and Makefile commands actually ran without cryptic errors

Moral of the story: I spent more time learning what not to do in cross-platform setups than expected, but that’s part of the journey. Now I know how to build stuff that actually runs cleanly on any machine. Including one with a cat sitting on the keyboard.

❓ Where do Tom and Mia fit into this pipeline?

Tom is Head of QA: he walks across the keyboard during testing.
Mia is the quiet CTO: she watches from her bench and judges your DAG decisions in silence.
Coffee is the uncredited co-author of every function that works on the first try.

