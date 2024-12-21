{{ config(materialized='incremental',
    unique_key='id',
    incremental_strategy='delete+insert'
  )
}}

select * from {{ ref('jobslog') }}
{% if is_incremental() %}

  where started >= (select max(started) from {{ this }})

{% endif %}
