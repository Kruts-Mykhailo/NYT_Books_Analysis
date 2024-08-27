{{
    config(
        materialized='incremental',
        unique_key='book_id',
        incremental_strategy='merge'
    )
}}

with latest_books as (
    select
        md5(concat(primary_isbn13, list_id)) as book_id,
        primary_isbn13,
        list_id,
        primary_isbn10,
        book_uri,
        contributor,
        contributor_note,
        created_date,
        description,
        update_rate,
        updated_date,
        weeks_on_list,
        rank,
        row_number() over (
            partition by primary_isbn13, list_id
            order by updated_date desc
        ) as rn
    from 
        {{ ref('stg_books' )}}
)
select
    book_id,
    primary_isbn13,
    list_id,
    primary_isbn10,
    book_uri,
    contributor,
    contributor_note,
    created_date,
    description,
    update_rate,
    updated_date,
    weeks_on_list,
    rank
from
    latest_books
where
    rn = 1
