import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from src.fraud_rules import detect_repeated_transfers 

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

    # DEBUGGING 
    logger.info("Data schema:")
    df.printSchema()
    df.show(5)

    logger.info("Applying fraud rules...")
    flagged = detect_repeated_transfers(df)

    output_dir = "output/suspicious_transfers"
    os.makedirs(output_dir, exist_ok=True)

    count = flagged.count()
    if count > 0:
        logger.info(f"Detected {count} suspicious transactions.")

        # 🧼 Flatten the struct column
        flagged = flagged \
            .withColumn("window_start", col("window.start")) \
            .withColumn("window_end", col("window.end")) \
            .drop("window")

        flagged.write.mode("overwrite").csv(output_dir, header=True)
        logger.info(f"Saved results to {output_dir}")
    else:
        logger.warning("No suspicious transactions found. No file will be saved.")