from pyspark.sql.functions import from_json, col, current_timestamp, to_date
from src.common.config import get_kafka_config
from src.common.paths import bronze_path, checkpoint_path
from src.common.reader import read_kafka_stream
from src.common.spark import create_spark_session
from src.common.logger import setup_logger
from src.common.dlq import write_bronze_dlq


def run_bronze_pipeline(entity, kafka_topic, schema):
    logger = setup_logger(f"bronze.{entity}")
    logger.info(f"Starting bronze pipeline | entity={entity} topic={kafka_topic}")

    try:
        spark = create_spark_session(f"{entity} Bronze Ingestion")
        kafka_config = get_kafka_config()

        raw_df = read_kafka_stream(
            spark=spark,
            bootstrap_servers=kafka_config["bootstrap_servers"],
            topic=kafka_topic
        ).select(
            col("key").cast("string").alias("kafka_key"),
            col("topic").alias("kafka_topic"),
            col("partition").alias("kafka_partition"),
            col("offset").alias("kafka_offset"),
            col("value").cast("string").alias("raw_value"),
        )

        parsed_df = raw_df.withColumn("data", from_json(col("raw_value"), schema))

        def process_batch(batch_df, batch_id):
            good = batch_df.filter(col("data").isNotNull()).select(
                "data.*", "kafka_key", "kafka_topic", "kafka_partition", "kafka_offset",
            )
            bad = batch_df.filter(col("data").isNull()).select("raw_value")

            good_count = good.count()
            bad_count = write_bronze_dlq(bad, entity)

            if good_count > 0:
                good = good.withColumn("ingestion_timestamp", current_timestamp()) \
                           .withColumn("ingestion_date", to_date(col("ingestion_timestamp")))
                good.write.mode("append").partitionBy("ingestion_date").parquet(str(bronze_path(entity)))

            logger.info(
                f"Batch {batch_id} complete | entity={entity} "
                f"written={good_count} dlq={bad_count}"
            )

        query = (
            parsed_df.writeStream
            .foreachBatch(process_batch)
            .option("checkpointLocation", str(checkpoint_path(entity)))
            .start()
        )

        logger.info(f"Bronze pipeline running | entity={entity}")
        query.awaitTermination()

    except Exception:
        logger.exception(f"Bronze pipeline failed | entity={entity}")
        raise
