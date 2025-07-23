from pyspark.sql import DataFrame
from pyspark.sql.functions import window, count, col

import os
os.environ["PYSPARK_PYTHON"] = "./.venv/Scripts/python.exe"

def detect_rapid_repeated_transfers(df: DataFrame) -> DataFrame:
    """
    Detects accounts that made at least 3 transactions to the same counterparty
    within a 5-minute window.

    Parameters:
    - df: Spark DataFrame with columns ['account_id', 'counterparty_iban', 'timestamp']

    Returns:
    - DataFrame with columns ['account_id', 'counterparty_iban', 'window', 'tx_count']
    """
    return (
        df.groupBy(
            col("account_id"),
            col("counterparty_iban"),
            window(col("timestamp"), "5 minutes")
        )
        .agg(count("*").alias("tx_count"))
        .filter(col("tx_count") >= 3)
    )
