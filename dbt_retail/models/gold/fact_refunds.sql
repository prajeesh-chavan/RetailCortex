{{ config(
    materialized='incremental',
    unique_key='refund_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'refunds') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['r.refund_id']) }} AS refund_key,
    r.refund_id,
    {{ dbt_utils.generate_surrogate_key(['r.order_id']) }} AS order_key,
    {{ dbt_utils.generate_surrogate_key(['r.payment_id']) }} AS payment_key,
    r.refund_reference,
    r.refund_status,
    r.refund_reason,
    r.refund_amount,
    r.currency_code,
    r.processed_at,
    r.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at

FROM source_silver r
