import snowflake.snowpark.functions as F

def model(dbt, session):
    data_df = dbt.ref('stg_nfl_teams')
    return data_df