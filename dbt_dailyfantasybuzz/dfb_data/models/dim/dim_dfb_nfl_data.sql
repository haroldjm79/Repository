{{
 config(
 materialized = 'view'
 )
}}
WITH A AS (
 SELECT
 {{ dbt_utils.generate_surrogate_key(['date', 'name','game_info']) }} as record_id
, *
 FROM
 {{ ref('src_dfb_nfl_data') }}
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