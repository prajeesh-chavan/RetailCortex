{{ config(
    materialized='table'
) }}

WITH product_base AS (
    SELECT
        product_key,
        product_id,
        variant_id
    FROM {{ ref('gold_dim_product') }}
),

order_item_agg AS (
    SELECT
        product_key,
        SUM(quantity_ordered) AS total_units_sold,
        SUM(line_total_amount) AS total_revenue,
        SUM(line_discount_amount) AS total_discount_given,
        SUM(line_total_amount) / NULLIF(SUM(quantity_ordered), 0) AS average_selling_price,
        COUNT(DISTINCT order_key) AS total_orders_contained,
        COUNT(DISTINCT customer_key) AS total_customers,
        MAX({{ dbt_utils.generate_surrogate_key(['order_key']) }}) AS last_order_key
    FROM {{ ref('fact_order_items') }}
    GROUP BY product_key
),

return_agg AS (
    SELECT
        product_key,
        SUM(quantity_returned) AS return_quantity,
        COUNT(DISTINCT return_key) AS return_count
    FROM {{ ref('fact_returns') }}
    GROUP BY product_key
),

review_agg AS (
    SELECT
        product_key,
        AVG(rating) AS average_rating,
        COUNT(*) AS total_reviews
    FROM {{ ref('fact_product_reviews') }}
    GROUP BY product_key
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['pb.product_key']) }} AS product_performance_key,
    pb.product_key,
    COALESCE(oia.total_units_sold, 0) AS total_units_sold,
    COALESCE(oia.total_revenue, 0) AS total_revenue,
    COALESCE(oia.total_discount_given, 0) AS total_discount_given,
    oia.average_selling_price,
    COALESCE(oia.total_orders_contained, 0) AS total_orders_contained,
    COALESCE(oia.total_customers, 0) AS total_customers,
    rava.average_rating,
    COALESCE(rava.total_reviews, 0) AS total_reviews,
    COALESCE(ra.return_quantity, 0) / NULLIF(oia.total_units_sold, 0) AS return_rate,
    COALESCE(ra.return_quantity, 0) AS return_quantity,
    CURRENT_TIMESTAMP() AS last_refresh_timestamp
FROM product_base pb
LEFT JOIN order_item_agg oia ON pb.product_key = oia.product_key
LEFT JOIN return_agg ra ON pb.product_key = ra.product_key
LEFT JOIN review_agg rava ON pb.product_key = rava.product_key
