select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select date
from storage.dfb.dim_dfb_nfl_data
where date is null



      
    ) dbt_internal_test