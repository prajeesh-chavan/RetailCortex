from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

BRAND_SCHEMA = StructType([
    StructField("brand_id", StringType()),
    StructField("brand_name", StringType()),
    StructField("description", StringType(), True),
    StructField("is_active", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

BRAND_BRONZE_SCHEMA = StructType([
    StructField("brand_id", StringType()),
    StructField("brand_name", StringType()),
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
