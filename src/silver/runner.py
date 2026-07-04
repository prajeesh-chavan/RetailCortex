from src.common.reader import read_parquet_stream
from src.common.spark import create_spark_session
from src.common.paths import bronze_path, checkpoint_path
from src.common.config import get_snowflake_options
from src.common.writer import write_snowflake_batch


def run_silver_pipeline(entity, bronze_schema, transform_func, table_name, merge_key):
    spark = create_spark_session(f"{entity} Silver Transformation")

    stream_df = read_parquet_stream(
        spark=spark,
        path=str(bronze_path(entity)),
        schema=bronze_schema
    )

    clean_df = transform_func(stream_df)
    sf_options = get_snowflake_options()

    def merge_batch(batch_df, batch_id):
        print(f"Processing micro-batch ID: {batch_id}")
        write_snowflake_batch(
            dataframe=batch_df,
            sf_options=sf_options,
            table_name=table_name,
            merge_key=merge_key
        )

    query = (
        clean_df.writeStream
        .foreachBatch(merge_batch)
        .option("checkpointLocation", str(checkpoint_path(f"silver_{entity}")))
        .trigger(availableNow=True)
        .start()
    )

    query.awaitTermination()
