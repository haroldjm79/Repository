
  create or replace   view storage.dfb.dim_dfb_nfl_data
  
   as (
    
WITH  __dbt__cte__src_dfb_nfl_data as (
With A as (
select 
Date
,Name
,ID as Player_ID
,ROSTER_POSITION as Position
,Salary
,Concat('$',SALARY) as Salary_Char
,GAME_INFO
,OVER_UNDER
,PPG
,Value
,Projection
from dfb.raw_dfb_nfl_data
)select * from A
), A AS (
 SELECT
 md5(cast(coalesce(cast(date as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(name as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(game_info as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as record_id
, *
 FROM
 __dbt__cte__src_dfb_nfl_data
)
Select
record_id 
,Date
,Name
,Position
,Salary
,Salary_Char
,GAME_INFO
,OVER_UNDER  
,PPG
,Value
,Projection
from A
where PPG > 1
  );

