from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

ADDRESS_SCHEMA = StructType([
    StructField("address_id", StringType()),
    StructField("address_line_1", StringType()),
    StructField("address_line_2", StringType(), True),
    StructField("locality", StringType()),
    StructField("administrative_area", StringType()),
    StructField("postal_code", StringType()),
    StructField("country_code", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

ADDRESS_BRONZE_SCHEMA = StructType([
    StructField("address_id", StringType()),
    StructField("address_line_1", StringType()),
    StructField("address_line_2", StringType(), True),
    StructField("locality", StringType()),
    StructField("administrative_area", StringType()),
    StructField("postal_code", StringType()),
    StructField("country_code", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
