import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.etl import transform
from pyspark.sql import SparkSession
import pytest

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[*]").appName("TestETL").getOrCreate()

def test_transform_schema(spark):
    data = [("2023-01-01 12:00:00", "100.50")]
    df = spark.createDataFrame(data, ["timestamp", "amount"])
    result = transform(df)

    # Debug visual opcional
    # result.show()

    assert result.schema["timestamp"].dataType.simpleString() == "timestamp"
    assert result.schema["amount"].dataType.simpleString() == "double"
