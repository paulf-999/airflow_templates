{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

        {{ 'beep' }}

    {%- else -%}

        {{ 'beep' }}_{{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}