{{ config(
    materialized='table'
) }}

WITH customer_base AS (
    SELECT
        customer_key,
        customer_id
    FROM {{ ref('dim_customer') }}
),

order_agg AS (
    SELECT
        customer_key,
        MIN(order_date_key) AS first_order_date,
        MAX(order_date_key) AS last_order_date,
        COUNT(*) AS total_orders,
        COUNT(CASE WHEN order_status IN ('DELIVERED', 'SHIPPED') THEN 1 END) AS completed_orders,
        COUNT(CASE WHEN order_status = 'CANCELLED' THEN 1 END) AS cancelled_orders,
        SUM(total_amount) AS total_spend,
        SUM(total_amount) / NULLIF(COUNT(*), 0) AS average_order_value
    FROM {{ ref('fact_orders') }}
    GROUP BY customer_key
),

item_agg AS (
    SELECT
        customer_key,
        SUM(quantity_ordered) AS total_items_purchased
    FROM {{ ref('fact_order_items') }}
    GROUP BY customer_key
),

return_agg AS (
    SELECT
        customer_key,
        COUNT(*) AS return_count,
        SUM(refund_amount) AS total_refunds
    FROM {{ ref('fact_returns') }}
    GROUP BY customer_key
)

SELECT
    cb.customer_key,
    oa.first_order_date,
    oa.last_order_date,
    oa.total_orders,
    oa.completed_orders,
    oa.cancelled_orders,
    COALESCE(ia.total_items_purchased, 0) AS total_items_purchased,
    oa.total_spend,
    COALESCE(ra.total_refunds, 0) AS total_refunds,
    oa.average_order_value,
    oa.total_spend - COALESCE(ra.total_refunds, 0) AS customer_lifetime_value,
    COALESCE(ra.return_count, 0) / NULLIF(oa.completed_orders, 0) AS return_rate,
    DATEDIFF('day', TO_DATE(CAST(oa.last_order_date AS VARCHAR), 'YYYYMMDD'), CURRENT_DATE) AS recency_days,
    oa.completed_orders AS frequency_score,
    oa.total_spend AS monetary_score,
    CASE
        WHEN oa.total_spend >= 50000 THEN 'PLATINUM'
        WHEN oa.total_spend >= 10000 THEN 'GOLD'
        WHEN oa.total_spend >= 5000 THEN 'SILVER'
        WHEN oa.total_spend > 0 THEN 'BRONZE'
        ELSE 'INACTIVE'
    END AS customer_segment,
    CURRENT_TIMESTAMP() AS last_refresh_timestamp
FROM customer_base cb
LEFT JOIN order_agg oa ON cb.customer_key = oa.customer_key
LEFT JOIN item_agg ia ON cb.customer_key = ia.customer_key
LEFT JOIN return_agg ra ON cb.customer_key = ra.customer_key
