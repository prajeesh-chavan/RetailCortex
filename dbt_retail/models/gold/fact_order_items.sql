{{ config(
    materialized='incremental',
    unique_key='order_item_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'order_items') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['oi.order_item_id']) }} AS order_item_key,
    {{ dbt_utils.generate_surrogate_key(['oi.order_id']) }} AS order_key,
    {{ dbt_utils.generate_surrogate_key(['oi.variant_id']) }} AS product_key,
    {{ dbt_utils.generate_surrogate_key(['oi.vendor_id']) }} AS vendor_key,
    NULL AS customer_key,
    oi.order_item_id,
    oi.product_name_snapshot,
    oi.sku_snapshot,
    oi.quantity_ordered,
    oi.quantity_fulfilled,
    oi.quantity_returned,
    oi.unit_price,
    oi.line_discount_amount,
    oi.line_tax_amount,
    oi.line_shipping_amount,
    oi.line_total_amount,
    oi.currency_code,
    oi.item_status,
    oi.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at

FROM source_silver oi
