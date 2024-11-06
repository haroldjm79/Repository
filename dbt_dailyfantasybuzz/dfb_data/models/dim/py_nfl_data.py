import snowflake.snowpark.functions as F

def model(dbt, session):
    data_df = dbt.ref('stg_dfb_data')
    data_df = data_df.drop('PLAYER_ID')
    data_df = data_df.filter(data_df['PPG'] > 1)
    return data_df