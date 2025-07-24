
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from pyspark.sql import SparkSession
from src.fraud_rules import detect_repeated_transfers  # 👈 import your fraud logic

# ───── LOGGING SETUP ─────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

# ───── MAIN SCRIPT ─────
if __name__ == "__main__":
    logger.info("Starting Spark session...")
    spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

    logger.info("Loading CSV data...")
    df = spark.read.csv("artifacts/output.csv", header=True, inferSchema=True)

    logger.info("Applying fraud rules...")
    flagged = detect_repeated_transfers(df)

    logger.info("Saving results to output/suspicious_transfers/")
    flagged.write.mode("overwrite").csv("output/suspicious_transfers", header=True)

    logger.info("Finished successfully! 🎉")
