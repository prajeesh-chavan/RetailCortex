{{ config(
    materialized='table'
) }}

WITH channel_base AS (
    SELECT
        channel_key,
        channel_id,
        channel_name
    FROM {{ ref('dim_sales_channel') }}
),

order_agg AS (
    SELECT
        channel_key,
        COUNT(*) AS total_orders,
        SUM(total_amount) AS total_revenue,
        COUNT(DISTINCT customer_key) AS total_customers,
        SUM(total_amount) / NULLIF(COUNT(*), 0) AS average_order_value,
        MAX(order_date_key) AS last_order_date
    FROM {{ ref('fact_orders') }}
    GROUP BY channel_key
),

first_orders AS (
    SELECT
        customer_key,
        MIN(order_date_key) AS first_order_date_key
    FROM {{ ref('fact_orders') }}
    GROUP BY customer_key
),

new_customer_agg AS (
    SELECT
        o.channel_key,
        COUNT(DISTINCT fo.customer_key) AS new_customers
    FROM {{ ref('fact_orders') }} o
    JOIN first_orders fo ON o.customer_key = fo.customer_key
    GROUP BY o.channel_key
),

return_agg AS (
    SELECT
        o.channel_key,
        COUNT(DISTINCT r.return_key) AS return_count
    FROM {{ ref('fact_returns') }} r
    JOIN {{ ref('fact_orders') }} o ON r.order_key = o.order_key
    GROUP BY o.channel_key
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['cb.channel_key']) }} AS channel_performance_key,
    cb.channel_key,
    COALESCE(oa.total_orders, 0) AS total_orders,
    COALESCE(oa.total_revenue, 0) AS total_revenue,
    COALESCE(oa.average_order_value, 0) AS average_order_value,
    COALESCE(oa.total_customers, 0) AS total_customers,
    COALESCE(nca.new_customers, 0) AS new_customers,
    COALESCE(ra.return_count, 0) / NULLIF(oa.total_orders, 0) AS refund_rate,
    oa.last_order_date,
    CURRENT_TIMESTAMP() AS last_refresh_timestamp
FROM channel_base cb
LEFT JOIN order_agg oa ON cb.channel_key = oa.channel_key
LEFT JOIN new_customer_agg nca ON cb.channel_key = nca.channel_key
LEFT JOIN return_agg ra ON cb.channel_key = ra.channel_key
