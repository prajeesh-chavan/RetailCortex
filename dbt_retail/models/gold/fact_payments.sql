{{ config(
    materialized='incremental',
    unique_key='payment_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'payments') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['p.payment_id']) }} AS payment_key,
    p.payment_id,
    {{ dbt_utils.generate_surrogate_key(['p.order_id']) }} AS order_key,
    p.payment_method,
    p.payment_provider,
    p.payment_status,
    p.amount,
    p.currency_code,
    p.processed_at,
    p.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at

FROM source_silver p
