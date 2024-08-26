select
    distinct author,
    md5(author) as author_id
from {{ ref('stg_books') }}