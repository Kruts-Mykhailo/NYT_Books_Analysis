{{
    config(
        unique_key='publisher_id'
    )
}}

with src_unique_books as (
    select 
        publisher,
        primary_isbn13,
        count(*) as unique_books_published
    from {{ source('dbt_nyt_books', 'raw_books') }}
    group by publisher, primary_isbn13

)
select 
    {{ dbt_utils.md5('publisher') }} as publisher_id,
    publisher,
    unique_books_published
from {{ ref('stg_books') }} as sb
inner join src_unique_books as sub on sub.publisher = sb.publisher
