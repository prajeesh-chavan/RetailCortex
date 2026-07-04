from pyspark.sql.functions import from_json, col, current_timestamp, to_date
from src.common.config import get_kafka_config
from src.common.paths import bronze_path, checkpoint_path
from src.common.reader import read_kafka_stream
from src.common.spark import create_spark_session
from src.common.writer import write_parquet_stream


def run_bronze_pipeline(entity, kafka_topic, schema):
    spark = create_spark_session(f"{entity} Bronze Ingestion")

    kafka_df = read_kafka_stream(
        spark=spark,
        bootstrap_servers=get_kafka_config()["bootstrap_servers"],
        topic=kafka_topic
    )

    bronze_df = (
        kafka_df
        .selectExpr("CAST(value AS STRING) AS value")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
        .withColumn("ingest_time", current_timestamp())
        .withColumn("ingest_date", to_date(col("ingest_time")))
    )

    query = write_parquet_stream(
        dataframe=bronze_df,
        output_path=str(bronze_path(entity)),
        checkpoint_path=str(checkpoint_path(entity)),
        partitionBy=["ingest_date"]
    )

    query.awaitTermination()
