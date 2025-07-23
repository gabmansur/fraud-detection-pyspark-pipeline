import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.fraud_rules import detect_repeated_transfers
from pyspark.sql import SparkSession
import pytest

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[*]").appName("TestRules").getOrCreate()

def test_detect_repeated_transfers(spark):
    data = [
        ("u1", "NL01BANK0123456789", "2023-01-01 12:00:00"),
        ("u1", "NL01BANK0123456789", "2023-01-01 12:01:00"),
        ("u1", "NL01BANK0123456789", "2023-01-01 12:02:00"),
        ("u2", "NL02BANK9876543210", "2023-01-01 13:00:00")
    ]
    df = spark.createDataFrame(data, ["user_id", "counterparty_iban", "timestamp"])

    result = detect_repeated_transfers(df)

    # Optional for debugging
    # result.show(truncate=False)

    assert result.count() == 1