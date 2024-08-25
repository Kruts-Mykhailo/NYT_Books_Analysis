select
    {{ dbt_utils.md5('author') }} as author_id,
    author
from {{ ref('stg_books') }}