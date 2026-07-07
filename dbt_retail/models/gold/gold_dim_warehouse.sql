{{ config(
    materialized='incremental',
    unique_key='warehouse_key',
    incremental_strategy='merge'
) }}

WITH silver_warehouses AS (
    SELECT * FROM {{ source('snowflake_silver', 'warehouses') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['w.warehouse_id']) }} AS warehouse_key,
    w.warehouse_id,
    w.warehouse_code,
    w.warehouse_name,
    a.locality,
    a.administrative_area,
    a.country_code,
    w.warehouse_status,
    w.created_at,
    w.updated_at,
    w.is_deleted,
    w.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at,
    CURRENT_TIMESTAMP() AS dw_updated_at

FROM silver_warehouses w
LEFT JOIN {{ source('snowflake_silver', 'addresses') }} a
    ON w.address_id = a.address_id
