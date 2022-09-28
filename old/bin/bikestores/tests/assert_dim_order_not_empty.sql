-- dim_order shouldn't be empty
SELECT count(*) AS row_count
FROM {{ ref('dim_order') }}
HAVING row_count < 1
