import snowflake.snowpark.functions as F

def model(dbt, session):
    df = dbt.ref('py_nfl_data')
    df1 = dbt.ref('fct_nfl_teams')
    data_df = df.join(df1, df['Game_Info'] == df1['abbrev'])
    return data_df