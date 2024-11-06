
  
    

        create or replace transient table storage.dfb.dfb_nfl_cleansed
         as
        (
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
from storage.dfb.dim_dfb_nfl_data
where PPG > 1
        );
      
  