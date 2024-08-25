with source as (

    select * from {{ source('dbt_nyt_books', 'raw_books') }}

),
select
    cast(id as int) as id,
    age_group,
    author,
    book_uri,
    contributor,
    contributor_note,
    cast(created_date as date) as created_date,
    description,
    cast(updated_date as date) as updated_date,
    cast(updated_rate as date) as update_rate,
    cast(price as float) as price,
    publisher,
    cast(published_date as date) as published_date,
    cast(primary_isbn10 as int) as primary_isbn10,
    cast(primary_isbn13 as int) as primary_isbn13,
    cast(list_id as int),
    list_name,
    cast(rank as int) as rank,
    cast(rank_last_week as int) as rank_last_week,
    cast(weeks_on_list as int) as weeks_on_list
from source
where published_date >= (select max(published_date) from {{ this }})
