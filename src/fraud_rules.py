from pyspark.sql.functions import window, count, col

def detect_rapid_repeated_transfers(df):
    return df.groupBy("account_id", "counterparty_iban", window("timestamp", "5 minutes")) \
             .agg(count("*").alias("tx_count")) \
             .filter(col("tx_count") >= 3)