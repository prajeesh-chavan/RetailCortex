{{ config(
    materialized='table'
) }}

WITH silver_inventory AS (
    SELECT * FROM {{ source('snowflake_silver', 'inventory') }}
),

warehouse_keys AS (
    SELECT warehouse_id, warehouse_key FROM {{ ref('gold_dim_warehouse') }}
),

product_keys AS (
    SELECT variant_id, product_key FROM {{ ref('gold_dim_product') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['i.inventory_id', 'CURRENT_DATE']) }} AS snapshot_key,
    COALESCE(wk.warehouse_key, md5('_unknown_')) AS warehouse_key,
    COALESCE(pk.product_key, md5('_unknown_')) AS product_key,
    CAST(REPLACE(CAST(CURRENT_DATE AS VARCHAR), '-', '') AS INT) AS snapshot_date_key,
    i.quantity_on_hand,
    i.quantity_reserved,
    i.quantity_on_hand - i.quantity_reserved AS quantity_available,
    i.reorder_level,
    i.unit_cost,
    i.quantity_on_hand * i.unit_cost AS inventory_value,
    i.last_stock_update_at,
    CURRENT_TIMESTAMP() AS snapshot_timestamp
FROM silver_inventory i
LEFT JOIN warehouse_keys wk ON i.warehouse_id = wk.warehouse_id
LEFT JOIN product_keys pk ON i.variant_id = pk.variant_id
