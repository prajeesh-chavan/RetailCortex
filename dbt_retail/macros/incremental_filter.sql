{% macro incremental_filter(source_column='ingest_time', target_column='silver_ingest_time') %}
    {% if is_incremental() %}
        WHERE {{ source_column }} > (SELECT MAX({{ target_column }}) FROM {{ this }})
    {% endif %}
{% endmacro %}
