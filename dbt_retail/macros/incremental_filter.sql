{% macro incremental_filter(source_column='ingestion_timestamp', target_column='silver_ingest_time') %}
    {% if is_incremental() %}
        WHERE {{ source_column }} > (SELECT MAX({{ target_column }}) FROM {{ this }})
    {% endif %}
{% endmacro %}
