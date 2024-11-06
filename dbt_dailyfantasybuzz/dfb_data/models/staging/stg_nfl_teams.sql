with source as (
select * from {{ ref('seed_nfl_teams') }}
)select * from source