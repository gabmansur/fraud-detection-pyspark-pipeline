import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os

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

# ───── LOAD FUNCTION ───────────────────────────────
def load_csv_data(path: str) -> pd.DataFrame:
    logger.info(f"Loading data from {path}...")
    files = [f for f in os.listdir(path) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("No CSV file found in output folder.")

    df = pd.read_csv(os.path.join(path, files[0]))
    logger.info(f"Loaded {len(df)} rows.")
    return df

# ───── PLOT 1: TRANSACTION DISTRIBUTION ────────────
def plot_transaction_distribution(df: pd.DataFrame):
    logger.info("Plotting transaction amount distribution...")

    # Optional: remove top 1% outliers for cleaner plot
    df = df[df["amount"] < df["amount"].quantile(0.99)]

    plt.figure(figsize=(10, 6))
    sns.histplot(
        df["amount"],
        bins=30,
        kde=True,
        color="mediumpurple",
        edgecolor="white"
    )
    plt.title("Transaction Amount Distribution", fontsize=16)
    plt.xlabel("Amount")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("artifacts/transaction_distribution.png", dpi=300)
    logger.info("Saved plot to artifacts/transaction_distribution.png")
    plt.show()

# ───── PLOT 2: TRANSACTIONS OVER TIME ──────────────
def plot_transactions_over_time(df: pd.DataFrame):
    logger.info("Plotting transactions over time...")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    daily_sum = df["amount"].resample("D").sum()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_sum, color="mediumvioletred", linewidth=2.5)
    plt.title("Daily Total Transaction Amount", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig("artifacts/transactions_over_time.png", dpi=300)
    logger.info("Saved plot to artifacts/transactions_over_time.png")
    plt.show()

# ───── MAIN ────────────────────────────────────────
if __name__ == "__main__":
    df = load_csv_data("artifacts/output.csv")
    plot_transaction_distribution(df)
    plot_transactions_over_time(df)