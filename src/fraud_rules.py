import logging
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, window, count, to_timestamp

# ───── LOGGING SETUP ───────────────────────────────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ───── FUNCTION ────────────────────────────────────
def detect_repeated_transfers(df: DataFrame) -> DataFrame:
    logger.info("Detecting suspicious patterns: ≥3 transfers to same IBAN within 5-minute window...")

    # Convert timestamp to actual TimestampType
    df = df.withColumn("timestamp", to_timestamp("timestamp"))

    # Group by sliding window + user_id + recipient
    windowed_df = (
        df.groupBy(
            window(col("timestamp"), "5 minutes", "1 minute"),
            col("user_id"),
            col("counterparty_iban")
        )
        .agg(count("*").alias("transfer_count"))
        .filter(col("transfer_count") >= 3)
    )

    logger.info(f"Detected {windowed_df.count()} suspicious transfer windows.")

    return windowed_df

# ───── SCRIPT ENTRY POINT ──────────────────────────
if __name__ == "__main__":
    spark = SparkSession.builder.appName("FraudDetection").getOrCreate()
    df = spark.read.csv("data/transactions.csv", header=True, inferSchema=True)

    flagged = detect_repeated_transfers(df)
    flagged.printSchema()
    flagged.show(truncate=False)

    # Optional: save results
    flagged.write.mode("overwrite").csv("output/suspicious_transfers", header=True)