{{ config(
    materialized='incremental',
    unique_key='vendor_key',
    incremental_strategy='merge'
) }}

WITH silver_vendors AS (
    SELECT * FROM {{ source('snowflake_silver', 'vendors') }}
    {{ incremental_filter() }}
),

vendor_default_addresses AS (
    SELECT va.vendor_id, a.locality, a.administrative_area, a.country_code
    FROM {{ source('snowflake_silver', 'vendor_addresses') }} va
    JOIN {{ source('snowflake_silver', 'addresses') }} a
        ON va.address_id = a.address_id
    WHERE va.is_default = true
    QUALIFY ROW_NUMBER() OVER (PARTITION BY va.vendor_id ORDER BY va.vendor_address_id) = 1
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['v.vendor_id']) }} AS vendor_key,
    v.vendor_id,
    v.vendor_name,
    v.legal_name,
    v.vendor_code,
    v.primary_contact_name,
    v.email,
    v.phone,
    v.tax_registration_number,
    v.vendor_status,
    addr.locality,
    addr.administrative_area,
    addr.country_code,
    v.created_at,
    v.updated_at,
    v.is_deleted,
    v.ingestion_timestamp AS silver_ingest_time,
    CURRENT_TIMESTAMP() AS dw_created_at,
    CURRENT_TIMESTAMP() AS dw_updated_at

FROM silver_vendors v
LEFT JOIN vendor_default_addresses addr
    ON v.vendor_id = addr.vendor_id
