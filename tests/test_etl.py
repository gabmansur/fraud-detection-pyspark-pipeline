import pytest
from pyspark.sql import SparkSession
from src.etl import transform

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()

def test_transform_schema(spark):
    df = spark.createDataFrame([
        ("TX1", "A001", "2025-07-01 10:00:00", "1000", "EUR", "desc", "Alice", "NL00BANK0001", "shopping", "bulk")
    ], ["transaction_id", "account_id", "timestamp", "amount", "currency", "description", "counterparty_name", "counterparty_iban", "category", "payment_type"])
    
    df_t = transform(df)
    assert df_t.schema["amount"].dataType.typeName() == "double"
