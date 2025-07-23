import logging
from pyspark.sql import DataFrame

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
    logger.info("Detecting repeated transfers based on user_id, timestamp, and amount...")

    result_df = (
        df.groupBy("user_id", "timestamp", "amount")
          .count()
          .filter("count > 1")
    )

    count = result_df.count()
    logger.info(f"Detected {count} repeated transfers.")

    return result_df
