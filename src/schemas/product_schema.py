from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

PRODUCT_SCHEMA = StructType([
    StructField("product_id", StringType()),
    StructField("vendor_id", StringType()),
    StructField("brand_id", StringType()),
    StructField("category_id", StringType()),
    StructField("product_name", StringType()),
    StructField("description", StringType(), True),
    StructField("product_status", StringType()),
    StructField("tax_class", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

PRODUCT_BRONZE_SCHEMA = StructType([
    StructField("product_id", StringType()),
    StructField("vendor_id", StringType()),
    StructField("brand_id", StringType()),
    StructField("category_id", StringType()),
    StructField("product_name", StringType()),
    StructField("description", StringType(), True),
    StructField("product_status", StringType()),
    StructField("tax_class", StringType()),
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
