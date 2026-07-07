{{ config(
    materialized='incremental',
    unique_key='movement_key',
    incremental_strategy='merge'
) }}

WITH silver_movements AS (
    SELECT * FROM {{ source('snowflake_silver', 'inventory_movements') }}
    {{ incremental_filter() }}
),

warehouse_keys AS (
    SELECT i.inventory_id, i.variant_id, wk.warehouse_key
    FROM {{ source('snowflake_silver', 'inventory') }} i
    JOIN {{ ref('gold_dim_warehouse') }} wk ON i.warehouse_id = wk.warehouse_id
),

product_keys AS (
    SELECT i.inventory_id, pk.product_key
    FROM {{ source('snowflake_silver', 'inventory') }} i
    JOIN {{ ref('gold_dim_product') }} pk ON i.variant_id = pk.variant_id
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['m.movement_id']) }} AS movement_key,
    CAST(REPLACE(CAST(m.movement_timestamp AS DATE), '-', '') AS INT) AS movement_date_key,
    COALESCE(wk.warehouse_key, md5('_unknown_')) AS warehouse_key,
    COALESCE(pk.product_key, md5('_unknown_')) AS product_key,
    m.movement_type,
    m.movement_quantity,
    m.reference_type,
    m.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at
FROM silver_movements m
LEFT JOIN warehouse_keys wk ON m.inventory_id = wk.inventory_id
LEFT JOIN product_keys pk ON m.inventory_id = pk.inventory_id
