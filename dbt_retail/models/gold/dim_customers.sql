{{ config(
    materialized='incremental',
    unique_key='customer_id',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'customers') }}
    
    {% if is_incremental() %}
      -- High-performance filter: scans only rows modified since our last run
      WHERE ingest_time > (SELECT MAX(silver_ingest_time) FROM {{ this }})
    {% endif %}
),

gold_transformations AS (
    SELECT
        customer_id,
        full_name,
        email,
        phone,
        customer_status,
        CAST(TO_CHAR(registered_at, 'YYYYMMDD') AS INT) AS registered_date_key,
        COALESCE(is_deleted, FALSE) AS is_deleted,
        ingest_time AS silver_ingest_time,
        CURRENT_TIMESTAMP() AS gold_updated_at

    FROM source_silver
)

SELECT * FROM gold_transformations