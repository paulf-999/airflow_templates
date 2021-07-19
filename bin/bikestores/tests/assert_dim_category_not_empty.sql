-- dim_category shouldn't be empty
select  count(*) as row_count
from    {{ ref('dim_category' )}}
having  row_count < 1
