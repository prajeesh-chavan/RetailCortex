from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

SHIPMENT_ITEM_SCHEMA = StructType([
    StructField("shipment_item_id", StringType()),
    StructField("shipment_id", StringType()),
    StructField("order_item_id", StringType()),
    StructField("quantity_shipped", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

SHIPMENT_ITEM_BRONZE_SCHEMA = StructType([
    StructField("shipment_item_id", StringType()),
    StructField("shipment_id", StringType()),
    StructField("order_item_id", StringType()),
    StructField("quantity_shipped", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
