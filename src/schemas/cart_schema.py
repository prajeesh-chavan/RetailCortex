from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

CART_SCHEMA = StructType([
    StructField("cart_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("session_id", StringType(), True),
    StructField("cart_status", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

CART_BRONZE_SCHEMA = StructType([
    StructField("cart_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("session_id", StringType(), True),
    StructField("cart_status", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
