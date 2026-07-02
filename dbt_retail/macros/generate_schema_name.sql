{#
    This macro overrides dbt's default behavior.
    Instead of concatenating target_schema + custom_schema,
    it will use ONLY the custom schema if one is specified.
#}

{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- if custom_schema_name is none -%}

        {{ target.schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}