{{ config(
    materialized='incremental',
    unique_key='return_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'returns') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['r.return_id']) }} AS return_key,
    r.return_id,
    {{ dbt_utils.generate_surrogate_key(['r.order_id']) }} AS order_key,
    {{ dbt_utils.generate_surrogate_key(['r.customer_id']) }} AS customer_key,
    r.return_number,
    r.return_reason,
    r.return_status,
    r.return_timestamp,
    r.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at

FROM source_silver r
