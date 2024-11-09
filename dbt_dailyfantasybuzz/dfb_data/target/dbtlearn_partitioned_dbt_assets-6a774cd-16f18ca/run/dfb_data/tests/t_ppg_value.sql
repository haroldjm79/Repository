select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
SELECT
 *
FROM
 storage.dfb.dim_dfb_nfl_data
WHERE
 PPG > 100

      
    ) dbt_internal_test