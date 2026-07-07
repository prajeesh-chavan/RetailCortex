{{ config(
    materialized='table'
) }}

WITH vendor_base AS (
    SELECT
        vendor_key,
        vendor_id,
        vendor_name
    FROM {{ ref('dim_vendor') }}
),

product_agg AS (
    SELECT
        v.vendor_id,
        MIN(p.created_at) AS first_product_added_date,
        MAX(p.created_at) AS last_product_added_date,
        COUNT(DISTINCT p.product_id) AS total_products,
        COUNT(DISTINCT CASE WHEN p.product_status = 'ACTIVE' THEN p.product_id END) AS active_products
    FROM {{ source('snowflake_silver', 'products') }} p
    JOIN vendor_base v ON p.vendor_id = v.vendor_id
    GROUP BY v.vendor_id
),

order_item_agg AS (
    SELECT
        vendor_key,
        COUNT(DISTINCT order_key) AS total_orders_supplied,
        SUM(quantity_ordered) AS total_units_supplied,
        SUM(line_total_amount) AS total_sales,
        SUM(line_total_amount) / NULLIF(COUNT(DISTINCT order_key), 0) AS average_order_value
    FROM {{ ref('fact_order_items') }}
    GROUP BY vendor_key
),

return_agg AS (
    SELECT
        vendor_key,
        COUNT(DISTINCT return_key) AS return_count
    FROM {{ ref('fact_returns') }}
    GROUP BY vendor_key
),

inventory_agg AS (
    SELECT
        dp.vendor_id,
        SUM(fis.quantity_on_hand) AS inventory_on_hand,
        SUM(fis.inventory_value) AS inventory_value
    FROM {{ ref('fact_inventory_snapshot') }} fis
    JOIN {{ ref('gold_dim_product') }} dp ON fis.product_key = dp.product_key
    GROUP BY dp.vendor_id
),

shipment_agg AS (
    SELECT
        foi.vendor_key,
        AVG(DATEDIFF('day', fs.shipped_at, fs.delivered_at)) AS average_fulfillment_time_days,
        SUM(CASE WHEN fs.delivered_at > fs.estimated_delivery_at THEN 1 ELSE 0 END) AS late_delivery_count,
        SUM(CASE WHEN fs.delivered_at <= fs.estimated_delivery_at THEN 1 ELSE 0 END) AS on_time_delivery_count,
        MAX(fs.delivered_at) AS last_delivery_date
    FROM {{ ref('fact_shipments') }} fs
    JOIN {{ ref('fact_order_items') }} foi ON fs.order_key = foi.order_key
    GROUP BY foi.vendor_key
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['vb.vendor_key']) }} AS vendor_performance_key,
    vb.vendor_key,
    pa.first_product_added_date,
    pa.last_product_added_date,
    COALESCE(pa.total_products, 0) AS total_products,
    COALESCE(pa.active_products, 0) AS active_products,
    COALESCE(oia.total_orders_supplied, 0) AS total_orders_supplied,
    COALESCE(oia.total_units_supplied, 0) AS total_units_supplied,
    COALESCE(ia.inventory_on_hand, 0) AS inventory_on_hand,
    COALESCE(ia.inventory_value, 0) AS inventory_value,
    COALESCE(oia.total_sales, 0) AS total_sales,
    oia.average_order_value,
    COALESCE(ra.return_count, 0) / NULLIF(oia.total_orders_supplied, 0) AS return_rate,
    sa.average_fulfillment_time_days,
    CASE
        WHEN (sa.on_time_delivery_count + sa.late_delivery_count) > 0
        THEN sa.on_time_delivery_count / (sa.on_time_delivery_count + sa.late_delivery_count)
    END AS on_time_delivery_rate,
    COALESCE(sa.late_delivery_count, 0) AS late_delivery_count,
    sa.last_delivery_date,
    CURRENT_TIMESTAMP() AS last_refresh_timestamp
FROM vendor_base vb
LEFT JOIN product_agg pa ON vb.vendor_id = pa.vendor_id
LEFT JOIN order_item_agg oia ON vb.vendor_key = oia.vendor_key
LEFT JOIN return_agg ra ON vb.vendor_key = ra.vendor_key
LEFT JOIN inventory_agg ia ON vb.vendor_id = ia.vendor_id
LEFT JOIN shipment_agg sa ON vb.vendor_key = sa.vendor_key
