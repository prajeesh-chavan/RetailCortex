{{ config(
    materialized='incremental',
    unique_key='carrier_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'carriers') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['carrier_id']) }} AS carrier_key,
    carrier_id,
    carrier_name,
    carrier_code,
    tracking_url_template,
    is_active,
    created_at,
    updated_at,
    is_deleted,
    ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at,
    CURRENT_TIMESTAMP() AS dw_updated_at

FROM source_silver
