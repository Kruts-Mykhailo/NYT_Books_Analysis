with age_groups as (
    select distinct age_group from {{ ref('stg_books') }}
), 
transformed_groups as (
    select 
        case 
            when age_group is null or age_group = '' then 'ALL'
            else age_group 
        end as age_group,
        case 
            when age_group is null or age_group = '' then 0
            when age_group like 'Ages % and up' then cast(substring(age_group from '(\d+)') as int)
            when age_group like 'Ages % to %' then cast(substring(age_group from '(\d+)') as int)
            else 0
        end as from_age,
        case 
            when age_group is null or age_group = '' then 100
            when age_group like 'Ages % and up' then 100
            when age_group like '%to%' then
                cast(substring(age_group from 'to (\d+)') as int)
            else 100
        end as to_age
    from age_groups
)
select
    md5(age_group) as age_group_id,
    age_group,
    from_age,
    to_age
from transformed_groups

