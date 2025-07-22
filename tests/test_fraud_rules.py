import pytest
from pyspark.sql import SparkSession, Row
from src.fraud_rules import detect_rapid_repeated_transfers

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()

def test_detect_repeated_transfers(spark):
    data = [
        Row(transaction_id="TX001", account_id="A001", timestamp="2025-07-01 10:00:00", counterparty_iban="NL11FAKE0001"),
        Row(transaction_id="TX002", account_id="A001", timestamp="2025-07-01 10:01:00", counterparty_iban="NL11FAKE0001"),
        Row(transaction_id="TX003", account_id="A001", timestamp="2025-07-01 10:02:00", counterparty_iban="NL11FAKE0001"),
    ]
    df = spark.createDataFrame(data)
    df = df.withColumn("timestamp", df["timestamp"].cast("timestamp"))
    result = detect_rapid_repeated_transfers(df)
    assert result.count() == 1