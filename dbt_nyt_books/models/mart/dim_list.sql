SELECT 
    list_id, 
    list_name
FROM {{ ref('stg_books') }}
GROUP BY list_id, list_name