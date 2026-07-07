{{ config(
    materialized='incremental',
    unique_key='review_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'product_reviews') }}
    {{ incremental_filter() }}
),

product_keys AS (
    SELECT product_id, product_key,
        ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY variant_id) AS rn
    FROM {{ ref('gold_dim_product') }}
),

customer_keys AS (
    SELECT customer_id, customer_key FROM {{ ref('dim_customer') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['r.review_id']) }} AS review_key,
    r.review_id,
    COALESCE(pk.product_key, md5('_unknown_')) AS product_key,
    COALESCE(ck.customer_key, md5('_unknown_')) AS customer_key,
    r.rating,
    r.is_verified_purchase,
    r.is_approved,
    r.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at
FROM source_silver r
LEFT JOIN product_keys pk ON r.product_id = pk.product_id AND pk.rn = 1
LEFT JOIN customer_keys ck ON r.customer_id = ck.customer_id
