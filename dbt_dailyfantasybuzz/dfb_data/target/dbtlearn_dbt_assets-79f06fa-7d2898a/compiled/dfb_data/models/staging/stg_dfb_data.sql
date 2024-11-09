with  __dbt__cte__src_dfb_nfl_data as (
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
), source as (
    select * from __dbt__cte__src_dfb_nfl_data

)

    select *
    from source