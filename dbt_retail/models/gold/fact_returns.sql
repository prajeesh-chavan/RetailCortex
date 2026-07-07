{{ config(
    materialized='incremental',
    unique_key='return_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'returns') }}
    {{ incremental_filter() }}
),

return_item_agg AS (
    SELECT
        return_id,
        SUM(refund_amount) AS total_refund_amount,
        SUM(quantity_returned) AS total_quantity_returned,
        COUNT(*) AS return_item_count
    FROM {{ source('snowflake_silver', 'return_items') }}
    GROUP BY return_id
),

order_item_keys AS (
    SELECT
        oi.order_item_id,
        oi.order_id,
        {{ dbt_utils.generate_surrogate_key(['oi.order_id']) }} AS order_key,
        {{ dbt_utils.generate_surrogate_key(['oi.variant_id']) }} AS product_key,
        {{ dbt_utils.generate_surrogate_key(['oi.vendor_id']) }} AS vendor_key
    FROM {{ source('snowflake_silver', 'order_items') }} oi
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['r.return_id']) }} AS return_key,
    r.return_id,
    {{ dbt_utils.generate_surrogate_key(['r.order_id']) }} AS order_key,
    {{ dbt_utils.generate_surrogate_key(['r.customer_id']) }} AS customer_key,
    oik.product_key,
    oik.vendor_key,
    CAST(REPLACE(CAST(r.return_timestamp AS DATE), '-', '') AS INT) AS date_key,
    r.return_number,
    r.return_reason,
    r.return_status,
    r.return_timestamp,
    COALESCE(ria.total_quantity_returned, 0) AS quantity_returned,
    COALESCE(ria.total_refund_amount, 0) AS refund_amount,
    r.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at
FROM source_silver r
LEFT JOIN return_item_agg ria ON r.return_id = ria.return_id
LEFT JOIN order_item_keys oik ON r.order_id = oik.order_id
    QUALIFY ROW_NUMBER() OVER (PARTITION BY r.return_id ORDER BY oik.order_item_id) = 1
