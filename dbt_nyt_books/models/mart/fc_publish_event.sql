{{
    config(
        unique_key='event_id',
        cluster_by=['published_date']
    )
}}
select
    md5(concat(primary_isbn13, list_id, published_date)) as event_id,
    {{ dbt_date.now() }} as load_timestamp,
    md5(concat(primary_isbn13, list_id)) as book_id,
    published_date,
    md5(age_group) as age_group_id,
    md5(publisher) as publisher_id,
    md5(author) as author_id,
    list_id,
    case 
        when rank > rank_last_week then 1 else 0
    end as rank_increased_flag,
    case 
        when rank < rank_last_week then 1 else 0
    end as rank_decreased_flag

from {{ ref('stg_books') }} as sb
