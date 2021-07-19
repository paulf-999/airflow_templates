-- dim_order_item shouldn't be empty
select  count(*) as row_count
from    {{ ref('dim_order_item' )}}
having  row_count < 1
