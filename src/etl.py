from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

def load_data(spark, path):
    return spark.read.csv(path, header=True, inferSchema=True)

def transform(df):
    return df.withColumn("timestamp", to_timestamp("timestamp")) \
             .withColumn("amount", col("amount").cast("double"))

if __name__ == "__main__":
    spark = SparkSession.builder.appName("FraudDetector").getOrCreate()
    df = load_data(spark, "data/transactions.csv")
    df = transform(df)
    df.show(truncate=False)