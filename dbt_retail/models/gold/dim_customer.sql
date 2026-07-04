{{ config(
    materialized='incremental',
    unique_key='customer_key',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'customers') }}
    {{ incremental_filter() }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} AS customer_key,
    customer_id,
    first_name,
    last_name,
    full_name,
    email,
    phone,
    date_of_birth,
    customer_status,
    customer_type,
    registered_date,
    registered_at,
    is_deleted,
    ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at,
    CURRENT_TIMESTAMP() AS dw_updated_at

FROM source_silver
