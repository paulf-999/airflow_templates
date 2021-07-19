-- dim_staff shouldn't be empty
select  count(*) as row_count
from    {{ ref('dim_staff' )}}
having  row_count < 1
