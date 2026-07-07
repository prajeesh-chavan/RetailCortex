{{ config(
    materialized='incremental',
    unique_key='shipment_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'shipments') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['s.shipment_id']) }} AS shipment_key,
    s.shipment_id,
    {{ dbt_utils.generate_surrogate_key(['s.order_id']) }} AS order_key,
    {{ dbt_utils.generate_surrogate_key(['s.carrier_id']) }} AS carrier_key,
    {{ dbt_utils.generate_surrogate_key(['s.warehouse_id']) }} AS warehouse_key,
    s.shipment_number,
    s.tracking_number,
    s.shipment_status,
    s.shipped_at,
    s.estimated_delivery_at,
    s.delivered_at,
    s.shipping_charge,
    s.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at

FROM source_silver s
