from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

RETURN_SCHEMA = StructType([
    StructField("return_id", StringType()),
    StructField("order_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("return_number", StringType()),
    StructField("return_reason", StringType(), True),
    StructField("return_status", StringType()),
    StructField("return_timestamp", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

RETURN_BRONZE_SCHEMA = StructType([
    StructField("return_id", StringType()),
    StructField("order_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("return_number", StringType()),
    StructField("return_reason", StringType(), True),
    StructField("return_status", StringType()),
    StructField("return_timestamp", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
