{{ config(
    materialized='table'
) }}

WITH item_totals AS (
    SELECT
        order_key,
        SUM(quantity_ordered) AS total_items_sold
    FROM {{ ref('fact_order_items') }}
    GROUP BY order_key
),

order_agg AS (
    SELECT
        o.channel_key,
        o.order_date_key,
        COUNT(*) AS total_orders,
        COUNT(DISTINCT o.customer_key) AS total_customers,
        SUM(o.total_amount) AS gross_revenue,
        SUM(o.discount_amount) AS discount_amount,
        SUM(o.total_amount) - SUM(o.discount_amount) AS net_revenue,
        SUM(o.tax_amount) AS tax_amount,
        SUM(o.shipping_amount) AS shipping_amount,
        COALESCE(SUM(it.total_items_sold), 0) AS total_items_sold
    FROM {{ ref('fact_orders') }} o
    LEFT JOIN item_totals it ON o.order_key = it.order_key
    GROUP BY o.channel_key, o.order_date_key
),

return_agg AS (
    SELECT
        o.channel_key,
        o.order_date_key,
        COUNT(DISTINCT r.return_key) AS total_refunds,
        SUM(r.refund_amount) AS refund_amount
    FROM {{ ref('fact_returns') }} r
    JOIN {{ ref('fact_orders') }} o ON r.order_key = o.order_key
    GROUP BY o.channel_key, o.order_date_key
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
        channel_key,
        fo.first_order_date_key AS order_date_key,
        COUNT(DISTINCT fo.customer_key) AS total_new_customers
    FROM {{ ref('fact_orders') }} o
    JOIN first_orders fo ON o.customer_key = fo.customer_key
    GROUP BY channel_key, fo.first_order_date_key
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['oa.channel_key', 'oa.order_date_key']) }} AS daily_summary_key,
    oa.order_date_key AS summary_date_key,
    oa.channel_key,
    oa.total_orders,
    oa.total_customers,
    oa.total_items_sold,
    oa.gross_revenue,
    oa.discount_amount,
    oa.net_revenue,
    oa.tax_amount,
    oa.shipping_amount,
    COALESCE(ra.total_refunds, 0) AS total_refunds,
    COALESCE(ra.refund_amount, 0) AS refund_amount,
    COALESCE(nca.total_new_customers, 0) AS total_new_customers,
    CURRENT_TIMESTAMP() AS last_refresh_timestamp
FROM order_agg oa
LEFT JOIN new_customer_agg nca
    ON oa.channel_key = nca.channel_key AND oa.order_date_key = nca.order_date_key
LEFT JOIN return_agg ra
    ON oa.channel_key = ra.channel_key AND oa.order_date_key = ra.order_date_key
