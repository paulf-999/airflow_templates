-- dim_store shouldn't be empty
SELECT count(*) AS row_count
FROM {{ ref('dim_store' ) }}
HAVING row_count < 1
