{{ config(
    materialized='incremental',
    unique_key='customer_id',
    incremental_strategy='merge'
) }}

WITH source_silver AS (
    SELECT * FROM {{ source('snowflake_silver', 'customers') }}
    
    {% if is_incremental() %}
      -- This filter ensures Snowflake only scans rows updated since the last dbt run
      WHERE ingest_time > (SELECT MAX(silver_ingest_time) FROM {{ this }})
    {% endif %}
),

gold_transformations AS (
    SELECT
        customer_id,
        full_name,
        email,
        registered_at,
        ingest_time AS silver_ingest_time,
        
        -- Handle soft deletes safely
        COALESCE(is_deleted, FALSE) AS is_deleted,
        
        -- Clean up text formatting
        TRIM(full_name) AS cleaned_full_name,
        
        -- Business Logic metrics
        DATE(registered_at) AS registration_date,
        YEAR(registered_at) AS registration_year,
        
        -- Row-level audit metadata
        CURRENT_TIMESTAMP() AS gold_updated_at

    FROM source_silver
)

SELECT * FROM gold_transformations