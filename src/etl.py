import logging
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, to_timestamp

# ───── LOGGING SETUP ───────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("FraudETL")

# ───── FUNCTIONS ───────────────────────────────────
def load_data(spark: SparkSession, path: str) -> DataFrame:
    logger.info(f"Loading data from: {path}")
    df = spark.read.csv(path, header=True, inferSchema=True)
    logger.info(f"Loaded {df.count()} rows with {len(df.columns)} columns.")
    return df

def transform(df: DataFrame) -> DataFrame:
    logger.info("Transforming data: parsing timestamps and casting amounts...")
    return (
        df.withColumn("timestamp", to_timestamp("timestamp"))
          .withColumn("amount", col("amount").cast("double"))
    )

# ───── MAIN ────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Starting Spark ETL job...")

    spark = (
        SparkSession.builder
        .appName("FraudETL")
        .config("spark.sql.parquet.enableVectorizedReader", "false")
        .config("spark.hadoop.mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
        .getOrCreate()
    )

    try:
        df = load_data(spark, "data/transactions_demo.csv")
        df = transform(df)

        logger.info("Writing transformed data to artifacts/output.csv...")
        (
            df.coalesce(1)
              .write
              .mode("overwrite")
              .option("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
              .csv("artifacts/output.csv", header=True)
        )

        logger.info("ETL job completed successfully. ✨")

    except Exception as e:
        logger.exception("ETL job failed with an error:")
        raise e

    finally:
        logger.info("Stopping Spark session.")
        spark.stop()
