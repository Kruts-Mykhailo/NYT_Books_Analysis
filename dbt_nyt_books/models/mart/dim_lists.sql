{{
    config(
        materialized='incremental',
        unique_key='list_id',
        incremental_strategy='merge'
    )
}}

select 
    distinct list_id, 
    list_name
from {{ ref('stg_books')}}