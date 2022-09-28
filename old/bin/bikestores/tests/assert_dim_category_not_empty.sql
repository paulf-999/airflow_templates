-- dim_category shouldn't be empty
SELECT count(*) AS row_count
FROM {{ ref('dim_category' ) }}
HAVING row_count < 1
