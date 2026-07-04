def write_parquet_stream(
    dataframe,
    output_path,
    checkpoint_path,
    partitionBy=None
):
    """
    Write a streaming DataFrame to Parquet format.

    Args:
        dataframe (DataFrame): The streaming DataFrame to write.
        output_path (str): The path where the Parquet files will be written.
        checkpoint_path (str): The path for storing checkpoint information.
        partitionBy (list, optional): A list of columns to partition by.

    Returns:
        StreamingQuery: The streaming query object.
    """
    query = dataframe.writeStream \
        .format("parquet") \
        .option("path", output_path) \
        .option("checkpointLocation", checkpoint_path) \
        .partitionBy(partitionBy) \
        .outputMode("append") \
        .start()

    return query

def write_snowflake_batch(
    dataframe,
    sf_options,
    table_name,
    merge_key=None,
):
    """
    Write a DataFrame to a Snowflake table, with optional upsert via merge key.

    Args:
        dataframe (DataFrame): The DataFrame to write.
        sf_options (dict): A dictionary containing Snowflake connection options.
        table_name (str): The name of the Snowflake table to write to.
        merge_key (str, optional): Column name for merge key.
            When provided, performs upsert instead of append merge.

    Returns:
        None
    """
    writer = dataframe.write \
        .format("snowflake") \
        .options(**sf_options) \
        .option("dbtable", table_name)

    if merge_key:
        writer = writer \
            .option("merge", "on") \
            .option("mergeKey", merge_key)

    writer.mode("append").save()