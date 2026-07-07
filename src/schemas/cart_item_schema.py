from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

CART_ITEM_SCHEMA = StructType([
    StructField("cart_item_id", StringType()),
    StructField("cart_id", StringType()),
    StructField("variant_id", StringType()),
    StructField("quantity", StringType()),
    StructField("unit_price", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

CART_ITEM_BRONZE_SCHEMA = StructType([
    StructField("cart_item_id", StringType()),
    StructField("cart_id", StringType()),
    StructField("variant_id", StringType()),
    StructField("quantity", StringType()),
    StructField("unit_price", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
