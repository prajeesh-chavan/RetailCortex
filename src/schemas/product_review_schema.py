from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

PRODUCT_REVIEW_SCHEMA = StructType([
    StructField("review_id", StringType()),
    StructField("product_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("order_id", StringType(), True),
    StructField("rating", StringType()),
    StructField("review_title", StringType(), True),
    StructField("review_body", StringType(), True),
    StructField("is_verified_purchase", StringType()),
    StructField("is_approved", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

PRODUCT_REVIEW_BRONZE_SCHEMA = StructType([
    StructField("review_id", StringType()),
    StructField("product_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("order_id", StringType(), True),
    StructField("rating", StringType()),
    StructField("review_title", StringType(), True),
    StructField("review_body", StringType(), True),
    StructField("is_verified_purchase", StringType()),
    StructField("is_approved", StringType()),
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
