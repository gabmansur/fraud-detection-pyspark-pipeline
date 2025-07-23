from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def load_data(spark: SparkSession, path: str) -> DataFrame:
    print(f"Loading data from: {path}")

    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("account_id", StringType(), True),
        StructField("timestamp", StringType(), True),  # We’ll cast this after
        StructField("amount", StringType(), True),     # Same here
        StructField("currency", StringType(), True),
        StructField("description", StringType(), True),
        StructField("counterparty_name", StringType(), True),
        StructField("counterparty_iban", StringType(), True),
        StructField("category", StringType(), True),
        StructField("payment_type", StringType(), True)
    ])

    return spark.read.csv(path, header=True, schema=schema)

def transform(df: DataFrame) -> DataFrame:
    print(" Transforming data: casting 'timestamp' and 'amount'")
    return (
        df.withColumn("timestamp", to_timestamp("timestamp"))
          .withColumn("amount", col("amount").cast("double"))
    )

if __name__ == "__main__":
    spark = SparkSession.builder.appName("FraudDetector").getOrCreate()

    input_path = "data/transactions.csv"
    output_path = "artifacts/output.parquet"

    df = load_data(spark, input_path)
    df = transform(df)

    print("Showing transformed data:")
    df.show(truncate=False)

    print(f"Writing transformed data to: {output_path}")
    df.write.mode("overwrite").parquet(output_path)

    spark.stop()