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

clean_df = bronze_df.select(
    "*",
    to_timestamp("created_at").alias("created_at"),
    to_timestamp("registered_at").alias("registered_at"),
    to_timestamp("updated_at").alias("updated_at"),
    to_timestamp("ingest_time").alias("ingest_time"),
    lower(col("email")).alias("email"),
    concat_ws(" ", col("first_name"), col("last_name")).alias("full_name"),
    lower(col("is_deleted")).cast("boolean").alias("is_deleted")
)


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

print(sf_options)

write_snowflake_batch(
    dataframe=final_df,
    sf_options=sf_options,
    table_name="customers"
)

# final_df.show(5, truncate=False)

print("Customer Silver Transformation completed successfully.")