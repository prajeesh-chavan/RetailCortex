from pyspark.sql.functions import *
from pyspark.sql.types import *
from src.common.config import load_config
from src.common.paths import bronze_path, checkpoint_path
from src.common.reader import read_kafka_stream
from src.common.spark import create_spark_session
from src.common.writer import write_parquet_stream
from src.schemas.customer import CUSTOMER_SCHEMA


# ----------------------------
# Spark Session
# ----------------------------
spark = create_spark_session("Customer Bronze Ingestion")


# ----------------------------
# Set Configurations
# ----------------------------
kafka_config = load_config("config/kafka.yaml")

BOOTSTRAP_SERVERS = kafka_config.get("bootstrap_servers", "localhost:9092")
KAFKA_TOPIC = kafka_config.get("topics", {}).get("customers", "customers")


# ----------------------------
# Read from Kafka
# ----------------------------
kafka_df = read_kafka_stream(
    spark=spark,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    topic=KAFKA_TOPIC
)


# ----------------------------
# Parse JSON
# ----------------------------
json_df = kafka_df.selectExpr(
    "CAST(value AS STRING) AS value"
)

bronze_df = (
    json_df
    .select(
        from_json(col("value"), CUSTOMER_SCHEMA).alias("data")
    )
    .select("data.*")
    .withColumn("ingest_time", current_timestamp())
)


# ----------------------------
# Output Paths
# ----------------------------
OUTPUT_PATH = bronze_path("customers")
CHECKPOINT_PATH = checkpoint_path("customers")


# ----------------------------
# Write Stream (Parquet)
# ----------------------------
query = write_parquet_stream(
    dataframe=bronze_df,
    output_path=OUTPUT_PATH,
    checkpoint_path=CHECKPOINT_PATH
)

# ----------------------------
# Monitor
# ----------------------------
print("Customers stream started...")

query.awaitTermination()

