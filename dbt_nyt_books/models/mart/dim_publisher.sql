
select 
    md5(publisher) as publisher_id,
    publisher,
    COUNT(*) as unique_books_published
from {{ ref('raw_books') }}
group by publisher, primary_isbn13