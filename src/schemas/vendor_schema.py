from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

VENDOR_SCHEMA = StructType([
    StructField("vendor_id", StringType()),
    StructField("vendor_name", StringType()),
    StructField("legal_name", StringType()),
    StructField("vendor_code", StringType()),
    StructField("primary_contact_name", StringType()),
    StructField("email", StringType()),
    StructField("phone", StringType()),
    StructField("tax_registration_number", StringType()),
    StructField("vendor_status", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

VENDOR_BRONZE_SCHEMA = StructType([
    StructField("vendor_id", StringType()),
    StructField("vendor_name", StringType()),
    StructField("legal_name", StringType()),
    StructField("vendor_code", StringType()),
    StructField("primary_contact_name", StringType()),
    StructField("email", StringType()),
    StructField("phone", StringType()),
    StructField("tax_registration_number", StringType()),
    StructField("vendor_status", StringType()),
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
