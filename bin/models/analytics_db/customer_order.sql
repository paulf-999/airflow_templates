SELECT  order_item.order_id
        , product.product_id
        , store.store_id
        , staff.staff_id
        , product.product_name
        , customer_order.order_date
        , customer_order.required_date
        , customer_order.shipped_date
        , order_item.quantity
        , order_item.list_price
        , order_item.discount
FROM    {{ ref('dim_product') }}            AS product
    LEFT JOIN {{ ref('dim_order_item') }}   AS order_item
    ON order_item.product_id = product.product_id
    LEFT JOIN {{ ref('dim_order') }}        AS customer_order
    ON customer_order.order_id = order_item.order_id
    LEFT JOIN {{ ref('dim_store') }}        AS store
    ON store.store_id = customer_order.store_id
    LEFT JOIN {{ ref('dim_staff') }}        AS staff
    ON staff.staff_id = customer_order.staff_id
LIMIT 5
