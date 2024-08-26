{{
    config(
        unique_key='primary_isbn13'
    )
}}

select 
    md5(concat(primary_isbn13, list_id)) as book_id,
    primary_isbn13,
    primary_isbn10,
    book_uri,
    contributor,
    contributor_note,
    created_date,
    description,
    update_rate,
    updated_date,
    weeks_on_list,
    rank as last_known_rank
 from {{ ref('stg_books')}}