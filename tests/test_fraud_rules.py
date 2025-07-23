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
    data = [("u1", "2023-01-01 12:00:00", 100.0),
            ("u1", "2023-01-01 12:00:00", 100.0)]
    df = spark.createDataFrame(data, ["user_id", "timestamp", "amount"])
    result = detect_repeated_transfers(df)

    # Debug visual opcional
    # result.show()

    assert result.count() == 1
