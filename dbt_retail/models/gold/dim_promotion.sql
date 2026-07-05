{{ config(
    materialized='incremental',
    unique_key='promotion_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'promotions') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['promotion_id']) }} AS promotion_key,
    promotion_id,
    promotion_name,
    promotion_code,
    promotion_type,
    discount_percentage,
    discount_amount,
    minimum_purchase_amount,
    maximum_discount_cap,
    applicable_to,
    applicable_entity_id,
    usage_limit,
    usage_count_per_customer,
    valid_from,
    valid_until,
    is_active,
    created_at,
    updated_at,
    is_deleted,
    ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at,
    CURRENT_TIMESTAMP() AS dw_updated_at

FROM source_silver
