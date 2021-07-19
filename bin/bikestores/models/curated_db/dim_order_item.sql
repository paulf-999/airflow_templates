SELECT * FROM {{ source('bike_sales', 'order_items') }}
