from src.common.reader import read_parquet_stream
from src.common.spark import create_spark_session
from src.common.paths import bronze_path, checkpoint_path
from src.common.config import get_snowflake_options
from src.common.writer import write_snowflake_batch
from src.common.logger import setup_logger
from src.common.dlq import write_silver_dlq


def run_silver_pipeline(entity, bronze_schema, transform_func, table_name, merge_key):
    logger = setup_logger(f"silver.{entity}")
    logger.info(f"Starting silver pipeline | entity={entity} table={table_name}")

    try:
        spark = create_spark_session(f"{entity} Silver Transformation")
        sf_options = get_snowflake_options()

        stream_df = read_parquet_stream(
            spark=spark,
            path=str(bronze_path(entity)),
            schema=bronze_schema
        )

        clean_df = transform_func(stream_df)

        def merge_batch(batch_df, batch_id):
            count = batch_df.count()
            logger.info(f"Processing batch {batch_id} | entity={entity} records={count}")

            try:
                write_snowflake_batch(
                    dataframe=batch_df,
                    sf_options=sf_options,
                    table_name=table_name,
                    merge_key=merge_key
                )
                logger.info(f"Batch {batch_id} complete | entity={entity} merged={count}")

            except Exception as e:
                write_silver_dlq(batch_df, entity, str(e))

        query = (
            clean_df.writeStream
            .foreachBatch(merge_batch)
            .option("checkpointLocation", str(checkpoint_path(f"silver_{entity}")))
            .trigger(availableNow=True)
            .start()
        )

        logger.info(f"Silver pipeline running | entity={entity}")
        query.awaitTermination()
        logger.info(f"Silver pipeline completed | entity={entity}")

    except Exception:
        logger.exception(f"Silver pipeline failed | entity={entity}")
        raise
