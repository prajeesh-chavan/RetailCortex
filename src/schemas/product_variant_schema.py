from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

PRODUCT_VARIANT_SCHEMA = StructType([
    StructField("variant_id", StringType()),
    StructField("product_id", StringType()),
    StructField("sku", StringType()),
    StructField("barcode", StringType(), True),
    StructField("color", StringType(), True),
    StructField("size", StringType(), True),
    StructField("unit_price", StringType()),
    StructField("cost_price", StringType()),
    StructField("currency_code", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

PRODUCT_VARIANT_BRONZE_SCHEMA = StructType([
    StructField("variant_id", StringType()),
    StructField("product_id", StringType()),
    StructField("sku", StringType()),
    StructField("barcode", StringType(), True),
    StructField("color", StringType(), True),
    StructField("size", StringType(), True),
    StructField("unit_price", StringType()),
    StructField("cost_price", StringType()),
    StructField("currency_code", StringType()),
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
