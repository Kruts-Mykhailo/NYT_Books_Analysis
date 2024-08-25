
select
    current_timestamp() as load_timestamp,
    sb.primary_isbn13 as book_id,
    sb.published_date,
    {{ dbt_utils.md5('age_group') }} as age_group_id,
    {{ dbt_utils.md5('publisher') }} as publisher_id,
    {{ dbt_utils.md5('author') }} as author_id,
    list_id,
    case 
        when rank > rank_last_week then 1 else 0
    end as rank_increased_flag,
    case 
        when rank < rank_last_week then 1 else 0
    end as rank_decreased_flag

from {{ ref('stg_books') }} as sb
