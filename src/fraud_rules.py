import logging
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, window, count, to_timestamp

# ───── LOGGING SETUP ─────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# ───── FRAUD RULE FUNCTION ─────
def detect_repeated_transfers(df: DataFrame) -> DataFrame:
    logger.info("Detecting ≥3 transfers to the same IBAN within 5-minute windows...")

    df = df.withColumn("timestamp", to_timestamp("timestamp"))

    windowed_df = (
        df.groupBy(
            window(col("timestamp"), "5 minutes", "1 minute"),
            col("account_id"),
            col("counterparty_iban")
        )
        .agg(count("*").alias("transfer_count"))
        .filter(col("transfer_count") >= 3)
    )

    logger.info(f"Detected {windowed_df.count()} suspicious transfer windows.")
    return windowed_df
