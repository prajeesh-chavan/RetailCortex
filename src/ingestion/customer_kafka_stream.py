from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


# ----------------------------
# Spark Session
# ----------------------------
spark = (
    SparkSession.builder
    .appName("Customer Stream")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
    )
    .config("spark.sql.streaming.schemaInference", "true")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ----------------------------
# Set Configurations
# ----------------------------
KAFKA_TOPIC = "telemetry.ecommerce.customers"
BOOTSTRAP_SERVERS = "localhost:9092"



# ----------------------------
# Schema
# ----------------------------
customer_schema = StructType([
    StructField("created_at", StringType()),
    StructField("customer_id", StringType()),
    StructField("customer_status", StringType()),
    StructField("email", StringType()),
    StructField("first_name", StringType()),
    StructField("is_deleted", StringType()),
    StructField("last_name", StringType()),
    StructField("phone", StringType()),
    StructField("registered_at", StringType()),
    StructField("updated_at", StringType())
])


# ----------------------------
# Read from Kafka
# ----------------------------
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()


# ----------------------------
# Parse JSON
# ----------------------------
json_df = df.selectExpr(
    "CAST(value AS STRING) AS value"
)

bronze_df = (
    json_df
    .select(
        from_json(col("value"), customer_schema).alias("data")
    )
    .select("data.*")
    .withColumn("ingest_time", current_timestamp())
)


# ----------------------------
# Output Paths
# ----------------------------
PROJECT_ROOT = Path.cwd()

OUTPUT_PATH = PROJECT_ROOT  / "Data" / "bronze" / "customers"
CHECKPOINT_PATH = PROJECT_ROOT / "Data" / "checkpoints" / "customers"


# ----------------------------
# Write Stream (Parquet)
# ----------------------------
query = bronze_df.writeStream \
    .format("parquet") \
    .option("path", OUTPUT_PATH) \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .outputMode("append") \
    .start()


# ----------------------------
# Monitor
# ----------------------------
print("Customers stream started...")

query.awaitTermination()

