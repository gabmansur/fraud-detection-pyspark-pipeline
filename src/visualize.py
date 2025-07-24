import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
import sys

# ───── LOGGING SETUP ───────────────────────────────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ───── STYLE SETUP ─────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)

# ───── GLOBALS ─────────────────────────────────────
PLOT_DIR = "artifacts"
SUSPICIOUS_DIR = "output/suspicious_transfers"

# ───── LOAD FUNCTION ───────────────────────────────
def load_csv_data(path: str) -> pd.DataFrame:
    logger.info(f"Loading data from folder: {path}")
    
    files = [f for f in os.listdir(path) if f.startswith("part-") and f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("No CSV partition found in folder.")

    filepath = os.path.join(path, files[0])
    logger.info(f"Reading file: {filepath}")
    
    df = pd.read_csv(filepath)
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    return df

# ───── PLOT 1: TRANSACTION DISTRIBUTION ────────────
def plot_transaction_distribution(df: pd.DataFrame):
    logger.info("Plotting transaction amount distribution...")
    df = df[df["amount"] < df["amount"].quantile(0.99)]

    plt.figure(figsize=(10, 6))
    sns.histplot(df["amount"], bins=30, kde=True, color="mediumpurple", edgecolor="white")
    plt.title("Transaction Amount Distribution", fontsize=16)
    plt.xlabel("Amount")
    plt.ylabel("Frequency")
    plt.tight_layout()
    output_path = os.path.join(PLOT_DIR, "transaction_distribution.png")
    plt.savefig(output_path, dpi=300)
    logger.info(f"Saved plot to {output_path}")
    plt.close()

# ───── PLOT 2: TRANSACTIONS OVER TIME ──────────────
def plot_transactions_over_time(df: pd.DataFrame):
    logger.info("Plotting transactions over time...")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["timestamp", "amount"])

    if df.empty:
        logger.warning("DataFrame is empty after cleaning — skipping plot.")
        return

    df.set_index("timestamp", inplace=True)
    daily_sum = df["amount"].resample("D").sum()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_sum, color="mediumvioletred", linewidth=2.5)
    plt.title("Daily Total Transaction Amount", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.tight_layout()
    output_path = os.path.join(PLOT_DIR, "transactions_over_time.png")
    plt.savefig(output_path, dpi=300)
    logger.info(f"Saved plot to {output_path}")
    plt.close()

# ───── PLOT 3: SUSPICIOUS WINDOWS ──────────────────
def plot_suspicious_transaction_windows():
    logger.info("Plotting suspicious transaction windows...")
    if not os.path.exists(SUSPICIOUS_DIR):
        logger.warning("Fraud output directory not found. Run `make fraud` first.")
        return

    files = [f for f in os.listdir(SUSPICIOUS_DIR) if f.endswith(".csv")]
    if not files:
        logger.warning("No suspicious transfer files found.")
        return

    fraud_dfs = [pd.read_csv(os.path.join(SUSPICIOUS_DIR, f)) for f in files]
    fraud_df = pd.concat(fraud_dfs, ignore_index=True)
    
    if "window.start" not in fraud_df.columns:
        logger.warning("Expected column `window.start` not found in suspicious output.")
        return

    fraud_df["window_start"] = pd.to_datetime(fraud_df["window.start"], errors="coerce")
    fraud_df = fraud_df.dropna(subset=["window_start"])

    plt.figure(figsize=(10, 5))
    fraud_df.groupby(fraud_df["window_start"].dt.date).size().plot(
        kind="bar", color="crimson", alpha=0.7
    )
    plt.title("Suspicious Transaction Windows Per Day")
    plt.xlabel("Date")
    plt.ylabel("Number of Fraud Windows")
    plt.xticks(rotation=45)
    plt.tight_layout()
    output_path = os.path.join(PLOT_DIR, "suspicious_transaction_windows.png")
    plt.savefig(output_path, dpi=300)
    logger.info(f"Saved plot to {output_path}")
    plt.close()

# ───── MAIN ────────────────────────────────────────
if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "artifacts/transactions_demo.csv"
    df = load_csv_data(input_path)
    plot_transaction_distribution(df)
    plot_transactions_over_time(df)
    plot_suspicious_transaction_windows()