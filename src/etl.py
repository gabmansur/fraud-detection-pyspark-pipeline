from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, to_timestamp

def load_data(spark: SparkSession, path: str) -> DataFrame:
    print(f"📂 Loading data from: {path}")
    return spark.read.csv(path, header=True, inferSchema=True)

def transform(df: DataFrame) -> DataFrame:
    print("🔄 Transforming data: casting 'timestamp' and 'amount'")
    return (
        df.withColumn("timestamp", to_timestamp("timestamp"))
          .withColumn("amount", col("amount").cast("double"))
    )

if __name__ == "__main__":
    spark = SparkSession.builder.appName("FraudDetector").getOrCreate()

    input_path = "data/transactions.csv"
    output_path = "artifacts/output.parquet"  # <-- you can also write to .csv if you want

    df = load_data(spark, input_path)
    df = transform(df)

    print("Showing transformed data:")
    df.show(truncate=False)

    print(f"Writing transformed data to: {output_path}")
    df.write.mode("overwrite").parquet(output_path)

    spark.stop()