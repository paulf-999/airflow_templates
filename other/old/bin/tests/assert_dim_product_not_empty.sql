-- dim_product shouldn't be empty
SELECT count(*) AS row_count
FROM {{ ref('dim_product' ) }}
HAVING row_count < 1
