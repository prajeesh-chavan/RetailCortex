{{ config(
    materialized='table'
) }}

WITH dbt_date_output AS (
    -- This calls the macro and embeds its generated SQL block under a fresh name
    {{ dbt_date.get_date_dimension("2020-01-01", "2030-12-31") }}
)

SELECT
    -- Convert '2020-01-01' to integer 20200101
    CAST(TO_CHAR(date_day, 'YYYYMMDD') AS INT) AS date_key,
    
    -- Keep all the other columns the macro generated for you
    *
FROM dbt_date_output