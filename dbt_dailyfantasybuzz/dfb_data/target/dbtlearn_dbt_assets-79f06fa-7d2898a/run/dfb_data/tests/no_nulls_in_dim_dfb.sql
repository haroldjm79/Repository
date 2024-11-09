select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
 SELECT * FROM storage.dfb.dim_dfb_nfl_data WHERE
 RECORD_ID IS NULL OR
 DATE IS NULL OR
 NAME IS NULL OR
 POSITION IS NULL OR
 SALARY IS NULL OR
 SALARY_CHAR IS NULL OR
 GAME_INFO IS NULL OR
 OVER_UNDER IS NULL OR
 PPG IS NULL OR
 VALUE IS NULL OR
 PROJECTION IS NULL OR
 
 FALSE

      
    ) dbt_internal_test