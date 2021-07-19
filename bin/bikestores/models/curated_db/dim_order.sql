SELECT * FROM {{ source('bike_sales', 'orders') }}
