{{ config(
    materialized='incremental',
    unique_key='product_key',
    incremental_strategy='merge'
) }}

WITH silver_products AS (
    SELECT * FROM {{ source('snowflake_silver', 'products') }}
    {% if is_incremental() %}
        WHERE ingestion_timestamp > (SELECT MAX(silver_ingest_time) FROM {{ this }})
    {% endif %}
),

silver_variants AS (
    SELECT * FROM {{ source('snowflake_silver', 'product_variants') }}
    {% if is_incremental() %}
        WHERE ingestion_timestamp > (SELECT MAX(silver_ingest_time) FROM {{ this }})
    {% endif %}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['pv.variant_id']) }} AS product_key,
    p.product_id,
    p.vendor_id,
    pv.variant_id,
    pv.sku,
    pv.barcode,
    p.product_name,
    b.brand_name,
    c.category_name,
    v.vendor_name,
    pv.color,
    pv.size,
    pv.unit_price,
    p.product_status,
    p.created_at,
    p.updated_at,
    p.is_deleted,
    GREATEST(p.ingestion_timestamp, pv.ingestion_timestamp) AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at,
    CURRENT_TIMESTAMP() AS dw_updated_at

FROM silver_variants pv
JOIN silver_products p ON pv.product_id = p.product_id
LEFT JOIN {{ source('snowflake_silver', 'brands') }} b ON p.brand_id = b.brand_id
LEFT JOIN {{ source('snowflake_silver', 'categories') }} c ON p.category_id = c.category_id
LEFT JOIN {{ source('snowflake_silver', 'vendors') }} v ON p.vendor_id = v.vendor_id
