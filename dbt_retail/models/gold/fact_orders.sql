{{ config(
    materialized='incremental',
    unique_key='order_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'orders') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['o.order_id']) }} AS order_key,
    {{ dbt_utils.generate_surrogate_key(['o.customer_id']) }} AS customer_key,
    {{ dbt_utils.generate_surrogate_key(['o.sales_channel_id']) }} AS channel_key,
    CAST(REPLACE(CAST(o.order_timestamp AS DATE), '-', '') AS INT) AS order_date_key,
    o.order_id,
    o.order_number,
    o.order_status,
    o.fulfillment_status,
    o.payment_status,
    o.order_timestamp,
    o.currency_code,
    o.subtotal_amount,
    o.discount_amount,
    o.tax_amount,
    o.shipping_amount,
    o.total_amount,
    o.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at

FROM source_silver o
