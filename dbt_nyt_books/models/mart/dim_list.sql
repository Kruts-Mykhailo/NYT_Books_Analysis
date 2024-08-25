{{
    config(
        unique_key='list_id'
    )
}}


select 
    list_id, 
    list_name
from {{ source('dbt_nyt_books', 'raw_books') }}
group by list_id, list_name