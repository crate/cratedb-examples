{% macro default__reset_csv_table(model, full_refresh, old_relation, agate_table) %}
    {% set sql = "" %}
    {% if full_refresh %}
        {{ adapter.drop_relation(old_relation) }}
        {% set sql = create_csv_table(model, agate_table) %}
    {% else %}
        {{ adapter.truncate_relation(old_relation) }}
        {% set sql = "delete from " ~ old_relation %}
    {% endif %}

    {{ return(sql) }}
{% endmacro %}

{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

        {{ default_schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}

{% macro postgres__create_schema(relation) -%}
  {%- call statement('create_schema') -%}
    /* schemas are not created in CrateDB */
    DROP TABLE IF EXISTS thisschemadefinitelydoesnotexits.thiswouldnotexist
    /* but we need to run something to not have just EOF */
  {% endcall %}
{% endmacro %}

{% macro postgres__create_table_as(temporary, relation, sql) -%}
  {%- set unlogged = config.get('unlogged', default=false) -%}
  {%- set sql_header = config.get('sql_header', none) -%}

  {{ sql_header if sql_header is not none }}

  create  table {{ relation }}
  as (
    {{ sql|replace('"crate".', "") }}
  );
{%- endmacro %}

{% macro postgres__drop_schema(relation) -%}
  {% if relation.database -%}
    {{ adapter.verify_database(relation.database) }}
  {%- endif -%}
  {%- call statement('drop_schema') -%}
    /* schemas are not dropped in CrateDB */
  {%- endcall -%}
{% endmacro %}

{% macro default__drop_relation(relation) -%}
  {% call statement('drop_relation', auto_begin=False) -%}
    drop {{ relation.type }} if exists "{{ relation.schema }}"."{{ relation.identifier }}"
  {%- endcall %}
{% endmacro %}

{% macro default__drop_schema(relation) -%}
  {%- call statement('drop_schema') -%}
    /* schemas are not dropped in CrateDB */
  {% endcall %}
{% endmacro %}

{% macro default__create_view_as(relation, sql) -%}
  {%- set sql_header = config.get('sql_header', none) -%}

  {{ sql_header if sql_header is not none }}
  create view "{{ relation.schema }}"."{{ relation.identifier }}" as 
    {{ sql|replace('"crate".', "") }}
  ;
{%- endmacro %}

{% macro postgres__rename_relation(from_relation, to_relation) -%}
	{% do drop_relation(to_relation) %}
	{% set schema_query = "SELECT table_type FROM information_schema.tables WHERE table_schema = '{}' AND table_name = '{}'".format(from_relation.schema, from_relation.identifier) %}
	{% set results = run_query(schema_query) %}
	{% if execute %}
		{% set results_list = results.columns[0].values() %}
	{% else %}
		{% set results_list = [] %}
	{% endif %}
	{% for relation_type in results_list %}  
		{% if relation_type == 'VIEW' %}    
			{% set view_query = "SELECT view_definition FROM information_schema.views WHERE table_schema = '{}' AND table_name = '{}'".format(from_relation.schema, from_relation.identifier) %}
			{% set view_definitions = run_query(view_query) %}
			{% if execute %}
				{% set view_definitions_list = view_definitions.columns[0].values() %}
			{% else %}
				{% set view_definitions_list = [] %}
			{% endif %}
			{% for view_definition in view_definitions_list %}  				
				{% call statement('drop_view') -%}
					DROP VIEW IF EXISTS {{ to_relation.schema }}.{{ to_relation.identifier }};
				{%- endcall %}
				{% call statement('create_view') -%}
					CREATE VIEW {{ to_relation.schema }}.{{ to_relation.identifier }} AS {{ view_definition }}
				{%- endcall %}
				{% call statement('drop_view') -%}
					DROP VIEW IF EXISTS {{ from_relation.schema }}.{{ from_relation.identifier }};
				{%- endcall %}
			{% endfor %}
		{% else %}
			{% call statement('rename_table') -%}
				ALTER TABLE {{ from_relation.schema }}.{{ from_relation.identifier }}
					RENAME TO {{ to_relation.identifier }}
			{%- endcall %}
		{% endif %}
	{% endfor %}
{% endmacro %}

