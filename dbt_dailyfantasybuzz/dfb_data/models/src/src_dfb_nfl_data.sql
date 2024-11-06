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