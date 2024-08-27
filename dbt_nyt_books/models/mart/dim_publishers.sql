{{
    config(
        materialized='incremental',
        unique_key='publisher_id',
        incremental_strategy='merge'
    )
}}

with book_publisher as (
    select 
        distinct publisher,
        primary_isbn13
    from {{ ref('stg_books') }}
)
select 
    md5(publisher) as publisher_id,
    publisher,
    count(*) unique_books_published
from {{ ref('stg_books') }} 
group by publisher

