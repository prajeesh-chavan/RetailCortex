from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

CATEGORY_SCHEMA = StructType([
    StructField("category_id", StringType()),
    StructField("category_name", StringType()),
    StructField("parent_category_id", StringType(), True),
    StructField("description", StringType(), True),
    StructField("is_active", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

CATEGORY_BRONZE_SCHEMA = StructType([
    StructField("category_id", StringType()),
    StructField("category_name", StringType()),
    StructField("parent_category_id", StringType(), True),
    StructField("description", StringType(), True),
    StructField("is_active", StringType()),
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
