#  Fraud Detection in PySpark – Scalable CI/CD Prototype


This is a simple, fully functional prototype simulating how a financial institution might detect suspicious transactions using scalable, testable tools common in data engineering. This project is not built for production—it’s designed to demonstrate practical knowledge of:

- Ingesting and transforming structured data using PySpark
- Implementing rule-based fraud detection logic
- Validating transformations using PyTest
- Automating testing with CI/CD using GitHub Actions

## 📚 Table of Contents

- [Architecture & Design Choices](#architecture-and-design-choices)
- [Component Breakdown](#component-breakdown)
- [Key Skills & Focus Areas](#key-skills--focus-areas)  
- [Tech Stack](#tech-stack)  
- [What the Code Does](#what-the-code-does)  
- [Project Structure](#project-structure)  
- [Sample Transaction Schema](#sample-transaction-schema)  
- [What Happens When You Run It](#what-happens-when-you-run-it)  
- [Future Development Ideas](#future-development-ideas)  
- [FAQ — Why These Tools and Choices](#️faq--why-these-tools-and-choices)


## Architecture & Design Choices
This pipeline emulates a real-world setup for financial data monitoring. It ingests transactions from a simulated dataset, transforms and filters them through business logic, and automatically validates the process via CI/CD pipelines.

This diagram shows how each component connects in the prototype:

- **Data ingestion** from a CSV file using PySpark
- **Transformation logic** applied in `etl.py` (casting, parsing)
- **Fraud detection** via `fraud_rules.py`
- **Validation** through `test_etl.py` and `test_fraud_rules.py` using PyTest
- **Continuous testing** on every commit via GitHub Actions (`.yml` config)

This mirrors how financial institutions like Rabobank monitor transactions at scale.



![Architecture Diagram](/assets/architecture.png)

## Component Breakdown
| **Component**               | **What It Does**                                                                                                                         | **Why It Matters**                                                                                                                |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `transactions.csv`          | This is a **fake input dataset**, made to look like real banking transactions from Rabobank’s APIs.                                      | Simulates real-life data you'd get from a payment stream or customer account. Gives the pipeline something meaningful to process. |
| `etl.py`                    | Runs a **PySpark job** that reads the CSV, **casts columns** (like amounts and timestamps), and prepares the data for analysis.          | This step ensures the raw text is converted into clean, typed data that machines can understand and analyze accurately.           |
| `DataFrame Transformations` | Part of `etl.py`, this refers to all the steps like parsing dates, converting string numbers to floats, and ensuring correct data types. | Just like cleaning vegetables before cooking — you can’t detect fraud on messy data.                                              |
| `fraud_rules.py`            | Applies a **simple rule**: if someone sends money to the same person more than 3 times within 5 minutes, it gets flagged as suspicious.  | Mimics what real fraud detection systems do, watch for unusual behavior patterns that could signal money laundering.             |
| `Suspicious Output`         | The result: a list of flagged transactions that **violated the fraud rule**.                                                             | This is the final alert, the potential fraud that an investigator or automated alert system would look into further.             |
| `test_etl.py`               | Uses **PyTest** to check whether the ETL steps (like type casting and missing values) are working correctly.                             | Catches bugs in the data pipeline before they affect fraud detection. Keeps the base clean and trustable.                         |
| `test_fraud_rules.py`       | Uses **PyTest** to check if the fraud rule is flagging the right transactions (and only the right ones).                                 | Validates that our logic works as intended, so we don’t wrongly accuse innocent people or miss real fraud.                      |
| `GitHub Actions`            | Every time code changes, this tool **automatically runs all tests** to make sure everything still works.                                 | Prevents “it worked on my machine” disasters. Gives team confidence that new updates didn’t break anything important.             |
| `test.yml` (GitHub config)  | A YAML file that defines when and how tests run (on every push, on the right Python version, etc).                                       | Think of it like a recipe card for GitHub Actions, it says: “when there’s new code, here’s how to test it.”                      |
| `Automated test results`    | The outcome of the above: a green ✅ or red ❌ that tells you whether all your logic is working.                                           | Gives instant feedback that the project is safe to continue building on or that something broke and needs fixing.               |


## Key Skills & Focus Areas

This project demonstrates real-world data engineering principles in a focused prototype:

| **Area**              | **What It Demonstrates**                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------ |
| Data transformation   | Cleaned, parsed, and typed structured data using PySpark, replicating enterprise pipelines |
| API Schema modeling   | Simulated real transaction structures based on [Rabobank’s PSD2 API](https://developer.rabobank.nl/api-documentation)     |
| Fraud detection logic | Reusable, rule-based detection to flag behavioral anomalies in transaction patterns        |
| Unit testing          | Used PyTest + fixtures to validate transformations and logic in isolation                  |
| CI/CD automation      | Configured GitHub Actions to trigger automated tests on every push                         |
| Modular architecture  | Organized code with clear separation of ETL, rules, data, tests, and workflows             |

🪄 Gabi’s take: I built this to reflect real-world expectations: clean structure, automation, modularity, and accuracy, all under 24 hours.

## Tech Stack

| Layer       | Tool            |
|-------------|-----------------|
| Data engine | PySpark         |
| Testing     | PyTest          |
| Automation  | GitHub Actions  |
| Language    | Python 3.10+    |

---

## How It Works

1. Loads example transaction data from a CSV file
2. Transforms the data using PySpark (parsing timestamps, casting amounts)
3. Applies a fraud rule: flags accounts that make three or more transactions to the same IBAN within a five-minute window
4. Uses PyTest to validate that the transformations and logic work as expected
5. Runs all tests automatically through GitHub Actions on every commit

## Project Structure

| Path                         | Description                                        |
| ---------------------------- | -------------------------------------------------- |
| `data/transactions.csv`      | Simulated transactions inspired by Rabobank’s PSD2 schema for clarity.       |
| `src/etl.py`                 | PySpark pipeline for loading and transforming data |
| `src/fraud_rules.py`         | Fraud rule to detect repeated IBAN transactions    |
| `tests/test_etl.py`          | PyTest test for ETL data transformation            |
| `tests/test_fraud_rules.py`  | PyTest test for fraud rule logic                   |
| `.github/workflows/test.yml` | GitHub Actions pipeline for automated testing      |
| `requirements.txt`           | Python dependencies (PySpark, PyTest)              |
| `README.md`                  | Project documentation                              |

## Sample Transaction Schema

Based on field definitions from [Rabobank’s PSD2 API](https://developer.rabobank.nl/api-documentation) to reflect industry data structures.

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

## What Happens When You Run It
1. etl.py loads the CSV using PySpark, parsing timestamps and casting data
2. fraud_rules.py runs rule-based logic to flag suspicious transfers
3. PyTest tests (test_etl.py, test_fraud_rules.py) validate everything
4. GitHub Actions (.yml) automatically triggers tests on every commit

## Future Development Ideas

If extended, the prototype could include:

- Additional fraud logic (e.g., large round transfers, cross-country anomalies)
- Spark Structured Streaming (for real-time detection)
- Deployment to Azure with ADLS or Blob Storage ingestion
- Integration with Delta Lake or Databricks runtime
- Dashboard visualization with Streamlit or Power BI
- Machine Learning models for anomaly detection


## ❓ FAQ — Why These Tools and Choices?
Below are answers to common questions about tool choices, alternatives, and how this prototype reflects real-world engineering decisions.

❓ Why did you use PySpark instead of Pandas or SQL?
Because even though the dataset is small, this project simulates how financial data is handled at scale.
PySpark can process millions of transactions across multiple machines
- is common in enterprise banking environments like Rabobank
- offers better performance and flexibility than Pandas when scaling up (pandas is faster to prototype but not the point here)
- This shows readiness for real-world data volumes, not just prototypes.

❓ Isn’t PySpark overkill?
Kind of, but also not really. It’s overkill for this CSV, but not for the kind of problems I’d be solving in a real job. I wanted to prove I can think bigger than the sample size.

❓ Why PyTest instead of other testing libraries?
PyTest is
- Simple, clean, and expressive
- Works out-of-the-box with no [boilerplate](#boilerplate "Boilerplate = repetitive setup code you have to write every time. basically less typing,
less setup, easier to focus on the logic, not the structure")
- Supports [fixtures](#fixtures "Boilerplate = A reusable setup that prepares data or state before a test runs. keeps tests clean, avoids repetition, simplifies complex setups"). great for mocking test data like transactions)
- Easy to integrate with CI/CD tools like GitHub Actions
- It allowed me to validate not only my transformations, but also fraud detection logic with precision and speed.
- Usual alternative: unittest (Python’s built-in testing library). Standard: comes with Python, no need to install; More verbose/boilerplate: requires writing extra code just to define tests; Less flexible and elegant than PyTest

❓Why GitHub Actions?
In real teams, manual testing isn’t enough. CI/CD ensures:
- Code is tested automatically on every push
- You catch errors early (no surprises in production)
- You can collaborate with confidence
- Is easy to set up with a .yml config
- I used GitHub Actions for this prototype because it integrates naturally with GitHub, is lightweight, and takes just minutes to configure for PyTest. But in a real-world enterprise setting like Rabobank, where Azure is more prevalent, I would absolutely set up a proper Azure Pipeline, so the integration with ADF, Azure Data Lake, or even containerized services is seamless.

❓ What about Azure Pipelines?
In a real company setting like Rabobank? For sure. Azure Pipelines is tighter with tools like ADF, Data Lake, and the whole Azure ecosystem. But for this demo? GitHub Actions was the fastest way to get the job done with full automation.

❓ Couldn’t this fraud rule be done in SQL?
100%. But writing it in Python gave me more flexibility. It’s easier to test, reuse, and expand. Plus, in real life, pipelines usually mix SQL and Python anyway, so I went with what felt cleaner for this setup.

❓ Why so much effort on testing for a demo?
Because I think showing the process matters more than the outcome. Anyone can write some logic and say “look, it works.” But I wanted to show can you can structure things in a clean, modular, testable, and stable. Even in a little prototype.

❓ What’s a fixture?
It's basically prepped data for your tests. Think of it like setting the table before serving a meal, your test knows what to expect and doesn't start from scratch each time.

❓ Why so much effort on testing for a demo?
Because this isn’t just about the output, it’s about the process. code should be testable, clean, and not break if you sneeze on it. 😄

❓ Why GitHub Actions instead of Azure Pipelines?
This is just a quick prototype, so GitHub Actions was the fastest and easiest to set up. But yeah, in a big corp like Rabobank, I’d use Azure Pipelines to plug into their cloud stuff. This is just the “fast and clean” demo version.

❓ Isn’t this fraud rule too simple?
Yep, and that’s the point. I wanted to show how rules work, not build an entire detection system. You could easily replace this logic with something more complex (ML, thresholds, geolocation, etc.).

❓ Where did this data come from?
It’s fake, I made it to look like the PSD2 schema from Rabobank. The goal was to simulate what real banking data feels like without needing real personal info.

❓ How long did this take?
Roughly 1 day. I wanted to show what I could build in 24h, if I had to prototype something quickly with structure, tests, automation, and documentation.



_Disclaimer: This project is for educational purposes only. No real transaction or sensitive data is used. Schema inspired by Rabobank APIs._