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

    '''
    Doesn’t assume an exact number of flagged windows — avoids fragility due to PySpark’s windowing.
    Ensures correctness of logic — checks the right user and IBAN were flagged.
    Scales well if more test cases or users are added.
    Closer to what you’d do in production QA — testing outcomes, not implementation detail.'''

    data = [
        ("u1", "NL01BANK0123456789", "2023-01-01 12:00:00"),
        ("u1", "NL01BANK0123456789", "2023-01-01 12:01:00"),
        ("u1", "NL01BANK0123456789", "2023-01-01 12:02:00"),
        ("u2", "NL02BANK9876543210", "2023-01-01 13:00:00")  # control user
    ]
    df = spark.createDataFrame(data, ["user_id", "counterparty_iban", "timestamp"])

    result = detect_repeated_transfers(df)
    result_local = result.collect()

    # Assert: All flagged windows are for the right user + iban
    for row in result_local:
        assert row["user_id"] == "u1"
        assert row["counterparty_iban"] == "NL01BANK0123456789"
        assert row["transfer_count"] >= 3

    # Optional: Assert number of detected windows (can change with window overlap)
    assert len(result_local) >= 1