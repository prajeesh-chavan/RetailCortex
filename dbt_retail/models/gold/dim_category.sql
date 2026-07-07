{{ config(
    materialized='incremental',
    unique_key='category_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'categories') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['cat.category_id']) }} AS category_key,
    cat.category_id,
    cat.category_name,
    parent.category_name AS parent_category_name,
    cat.description,
    cat.is_active,
    cat.created_at,
    cat.updated_at,
    cat.is_deleted,
    cat.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at,
    CURRENT_TIMESTAMP() AS dw_updated_at

FROM source_silver cat
LEFT JOIN source_silver parent
    ON cat.parent_category_id = parent.category_id
