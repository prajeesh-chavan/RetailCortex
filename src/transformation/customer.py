from src.common.spark import create_spark_session
from src.common.reader import read_parquet_batch
from src.common.paths import bronze_path
from pyspark.sql.functions import col, to_timestamp, lower, concat_ws
from src.common.writer import write_snowflake_batch
from src.common.config import get_snowflake_options

spark = create_spark_session("Customer Silver Transformation")

bronze_path = bronze_path("customers")

print(f"Reading from Bronze Path: {bronze_path}")

bronze_df = read_parquet_batch(
    spark=spark,
    path=str(bronze_path)
)

clean_df = bronze_df \
    .withColumn("created_at", to_timestamp("created_at")) \
    .withColumn("registered_at", to_timestamp("registered_at")) \
    .withColumn("updated_at", to_timestamp("updated_at")) \
    .withColumn("ingest_time", to_timestamp("ingest_time")) \
    .withColumn("email", lower(col("email"))) \
    .withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name"))) \
    .filter(col("is_deleted") == "false")


final_df = clean_df.select(
    "customer_id",
    "full_name",
    "email",
    "registered_at",
    "ingest_time",
    "created_at",
    "updated_at"
)

sf_options = get_snowflake_options()

print(sf_options)

write_snowflake_batch(
    dataframe=final_df,
    sf_options=sf_options,
    table_name="customers"
)

# final_df.show(5, truncate=False)

print("Customer Silver Transformation completed successfully.")