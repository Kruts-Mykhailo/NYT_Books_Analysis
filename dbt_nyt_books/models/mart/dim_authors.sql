{{
    config(
        materialized='incremental',
        unique_key='author_id',
        incremental_strategy='merge'
    )
}}

select
    distinct author,
    md5(author) as author_id
from {{ ref('stg_books') }}