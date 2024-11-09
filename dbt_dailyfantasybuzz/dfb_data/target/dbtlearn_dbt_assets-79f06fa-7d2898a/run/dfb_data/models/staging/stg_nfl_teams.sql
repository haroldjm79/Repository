
  create or replace   view storage.dfb.stg_nfl_teams
  
   as (
    with source as (
select * from storage.dfb.seed_nfl_teams
)select * from source
  );

