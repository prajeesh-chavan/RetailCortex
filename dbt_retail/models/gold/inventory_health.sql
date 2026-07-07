{{ config(
    materialized='table'
) }}

WITH snapshot_latest AS (
    SELECT
        warehouse_key,
        product_key,
        MAX(snapshot_date_key) AS latest_date_key
    FROM {{ ref('fact_inventory_snapshot') }}
    GROUP BY warehouse_key, product_key
),

latest_inventory AS (
    SELECT fis.*
    FROM {{ ref('fact_inventory_snapshot') }} fis
    JOIN snapshot_latest sl
        ON fis.warehouse_key = sl.warehouse_key
        AND fis.product_key = sl.product_key
        AND fis.snapshot_date_key = sl.latest_date_key
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['li.warehouse_key', 'li.product_key']) }} AS inventory_health_key,
    li.product_key,
    li.warehouse_key,
    li.quantity_on_hand,
    li.quantity_reserved,
    li.quantity_available,
    li.reorder_level,
    CASE
        WHEN li.reorder_level > 0 AND li.quantity_on_hand > 0
        THEN li.quantity_on_hand / NULLIF(li.reorder_level, 0)
        ELSE NULL
    END AS days_until_out_of_stock,
    CASE
        WHEN li.quantity_on_hand > li.reorder_level * 3 THEN true
        ELSE false
    END AS is_overstocked,
    CASE
        WHEN li.quantity_on_hand <= 0 THEN 'OUT_OF_STOCK'
        WHEN li.quantity_on_hand <= li.reorder_level THEN 'LOW_STOCK'
        WHEN li.quantity_on_hand > li.reorder_level * 3 THEN 'OVERSTOCKED'
        ELSE 'IN_STOCK'
    END AS stock_status,
    CURRENT_TIMESTAMP() AS last_refresh_timestamp
FROM latest_inventory li
