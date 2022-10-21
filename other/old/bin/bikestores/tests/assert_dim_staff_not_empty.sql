-- dim_staff shouldn't be empty
SELECT count(*) AS row_count
FROM {{ ref('dim_staff' ) }}
HAVING row_count < 1
