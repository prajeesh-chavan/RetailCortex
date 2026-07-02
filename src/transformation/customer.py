from src.common.reader import read_parquet_stream
from src.common.spark import create_spark_session
from src.common.paths import bronze_path, checkpoint_path
from src.common.config import get_snowflake_options
from src.common.writer import write_snowflake_batch
from pyspark.sql.functions import col, to_timestamp, lower, concat_ws
from src.schemas.customer import CUSTOMER_BRONZE_SCHEMA

spark = create_spark_session("Customer Silver Transformation")
bronze_path = bronze_path("customers")

checkpoint_path = checkpoint_path("silver_customers")

streaming_bronze_df = read_parquet_stream(
    spark=spark,
    path=str(bronze_path),
    schema=CUSTOMER_BRONZE_SCHEMA
    )


clean_df = streaming_bronze_df \
    .withColumn("created_at", to_timestamp("created_at")) \
    .withColumn("registered_at", to_timestamp("registered_at")) \
    .withColumn("updated_at", to_timestamp("updated_at")) \
    .withColumn("ingest_time", to_timestamp("ingest_time")) \
    .withColumn("email", lower(col("email"))) \
    .withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name"))) \
    .withColumn("is_deleted", (lower(col("is_deleted"))).cast("boolean"))

final_df = clean_df.select(
    "customer_id",
    "full_name",
    "email",
    "registered_at",
    "ingest_time",
    "is_deleted",
    "created_at",
    "updated_at"
)

sf_options = get_snowflake_options()

def merge_into_snowflake(batch_df, batch_id):
    print(f"Processing micro-batch ID: {batch_id}")
    write_snowflake_batch(
        dataframe=batch_df,
        sf_options=sf_options,
        table_name="customers"
    )

query = (
    final_df.writeStream
    .foreachBatch(merge_into_snowflake)
    .option("checkpointLocation", str(checkpoint_path))
    .trigger(availableNow=True)
    .start()
)

# Block the script until Spark finished processing all available data
query.awaitTermination()

print("Customer Silver Streaming Transformation completed successfully.")