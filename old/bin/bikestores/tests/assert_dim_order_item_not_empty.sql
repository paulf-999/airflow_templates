-- dim_order_item shouldn't be empty
SELECT count(*) AS row_count
FROM {{ ref('dim_order_item') }}
HAVING row_count < 1
