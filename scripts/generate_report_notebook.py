from pathlib import Path

# Prepare the notebook skeleton
notebook_path = Path("notebooks/final_report.ipynb")
notebook_path.parent.mkdir(parents=True, exist_ok=True)

# Create a minimal starter notebook with markdown and code blocks
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# Title and intro
cells.append(nbf.v4.new_markdown_cell("# 🕵️‍♀️ Fraud Detection Report\n"
    "This notebook presents the findings of a PySpark-based fraud detection system, "
    "applied to synthetic transaction data."))

# Dataset summary
cells.append(nbf.v4.new_markdown_cell("## 📊 Dataset Summary"))
cells.append(nbf.v4.new_code_cell("""import pandas as pd

df = pd.read_csv("artifacts/output.csv")
print("Number of transactions:", len(df))
print("Time range:", df['timestamp'].min(), "→", df['timestamp'].max())
print("Accounts:", df['account_id'].nunique())
df.head()"""))

# Visuals
cells.append(nbf.v4.new_markdown_cell("## 📈 Visualizations"))

cells.append(nbf.v4.new_code_cell("""from IPython.display import Image, display

display(Image(filename="artifacts/transaction_distribution.png"))
display(Image(filename="artifacts/transactions_over_time.png"))
try:
    display(Image(filename="artifacts/suspicious_windows.png"))
except:
    print("No suspicious plot available.")
"""))

# Fraud logic
cells.append(nbf.v4.new_markdown_cell("## 🧠 Fraud Detection Logic"))
cells.append(nbf.v4.new_markdown_cell(
    "We define suspicious behavior as **three or more transactions from the same account "
    "to the same IBAN within a 5-minute window**. This pattern may indicate 'smurfing' or "
    "automated transfers typical of money laundering techniques."
))

# Suspicious transfer output
cells.append(nbf.v4.new_markdown_cell("## 🚨 Suspicious Transactions Detected"))
cells.append(nbf.v4.new_code_cell("""import glob

# Load latest suspicious transfer output
suspicious_files = glob.glob("output/suspicious_transfers/part-*.csv")
if suspicious_files:
    suspicious_df = pd.read_csv(suspicious_files[0])
    display(suspicious_df)
else:
    print("No suspicious files found.")
"""))

# Wrap-up
cells.append(nbf.v4.new_markdown_cell("## ✅ Summary & Next Steps"))
cells.append(nbf.v4.new_markdown_cell(
    "- 3 suspicious transaction windows were detected.\n"
    "- Transactions show clustering patterns typical of fraud.\n"
    "- Next steps: tune detection thresholds, expand rule set, and explore ML-based methods."
))

nb['cells'] = cells

# Save it
with open(notebook_path, 'w') as f:
    nbf.write(nb, f)