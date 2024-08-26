{{
    config(
        incremental_key='published_date'
    )
}}
with source as (
    select * from {{ source('dbt_nyt_books', 'raw_books') }}
)
select
    age_group,
    author,
    book_uri,
    contributor,
    contributor_note,
    cast(created_date as date) as created_date,
    description,
    cast(updated_date as date) as updated_date,
    updated_rate as update_rate,
    cast(price as float) as price,
    publisher,
    cast(published_date as date) as published_date,
    primary_isbn10 as primary_isbn10,
    primary_isbn13 as primary_isbn13,
    cast(list_id as int),
    list_name,
    cast(rank as int) as rank,
    cast(rank_last_week as int) as rank_last_week,
    cast(weeks_on_list as int) as weeks_on_list
from source
where published_date >= (select max(published_date) from {{ this }})
