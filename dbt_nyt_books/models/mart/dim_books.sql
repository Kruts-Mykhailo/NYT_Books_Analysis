{{
    config(
        unique_key='primary_isbn13'
    )
}}

with book_details as (
    select 
        coalesce(sb.primary_isbn13, dim_b.book_id) as book_id,
        coalesce(sb.primary_isbn13, dim_b.primary_isbn13) as primary_isbn13,
        coalesce(sb.primary_isbn10, dim_b.primary_isbn10) as primary_isbn10,
        coalesce(sb.book_uri, dim_b.book_uri) as book_uri,
        coalesce(sb.contributor, dim_b.contributor) as contributor,
        coalesce(sb.contributor_note, dim_b.contributor_note) as contributor_note,
        coalesce(sb.created_date, dim_b.created_date) as created_date,
        coalesce(sb.description, dim_b.description) as description,
        coalesce(sb.update_rate, dim_b.update_rate) as update_rate,
        coalesce(sb.updated_date, dim_b.updated_date) as updated_date,
        coalesce(sb.weeks_on_list, dim_b.weeks_on_list) as weeks_on_list,
        case sb.primary_isbn13 is null and coalesce(dim_b.is_removed_flag, 0) = 0
            then 1
            else 0 
        end as is_removed_flag
    from {{ ref('stg_books')}} as sb
    full outer join {{ this }} as dim_b on sb.primary_isbn13 = dim_b.primary_isbn13
    where (sb.primary_isbn13 is null and dim_b.is_removed_flag = 1) OR (sb.primary_isbn13 is not null)

)

select 
    book_id
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
    rank as last_known_rank,
    is_removed_flag
from book_details