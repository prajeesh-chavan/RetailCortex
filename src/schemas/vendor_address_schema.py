from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

VENDOR_ADDRESS_SCHEMA = StructType([
    StructField("vendor_address_id", StringType()),
    StructField("vendor_id", StringType()),
    StructField("address_id", StringType()),
    StructField("address_type", StringType()),
    StructField("is_default", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

VENDOR_ADDRESS_BRONZE_SCHEMA = StructType([
    StructField("vendor_address_id", StringType()),
    StructField("vendor_id", StringType()),
    StructField("address_id", StringType()),
    StructField("address_type", StringType()),
    StructField("is_default", StringType()),
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
