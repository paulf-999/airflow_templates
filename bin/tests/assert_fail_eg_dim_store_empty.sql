-- dim_store shouldn't be empty
select  count(*) as row_count
from    {{ ref('dim_store' )}}
having  row_count > 1
