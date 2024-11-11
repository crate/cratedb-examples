
-- Use the `ref` function to select from other models

select *
from {{ ref('starter_first') }}
where id = 1
