{{ config(
    materialized='incremental',
    unique_key='channel_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'sales_channels') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['channel_id']) }} AS channel_key,
    channel_id,
    channel_name,
    channel_type,
    is_active,
    created_at,
    updated_at,
    is_deleted,
    ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at,
    CURRENT_TIMESTAMP() AS dw_updated_at

FROM source_silver
