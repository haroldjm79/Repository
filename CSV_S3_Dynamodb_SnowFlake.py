import pandas as pd
import boto3,sys,json
from itertools import groupby
from operator import itemgetter
from decimal import Decimal
import snowflake.connector

conn = snowflake.connector.connect(
    account='xxxxxx-xxxxxxxx',
    user='HAROLDJM79',
    password='xxxxxxxxxxxxxxxxx',
    warehouse='COMPUTE_WH',
    database = 'STORAGE',
    schema = 'DFB',
)

session  = boto3.Session()
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('customer_total')

df  = pd.read_csv(r's3://csv/data.csv')
dictf = df.to_dict(orient='records')
#[
#{'id': 212234, 'customer': 'harold', 'date': '07/09/2024', 'amount': 150}, 
#{'id': 435298, 'customer': 'jack', 'date': '01/01/2024', 'amount': 1000}, 
#{'id': 500001, 'customer': 'alice', 'date': '06/24/2024', 'amount': 30}, 
#{'id': 500001, 'customer': 'alice', 'date': '08/24/2024', 'amount': 3009}, 
#{'id': 397861, 'customer': 'barb', 'date': '03/30/2024', 'amount': 90}, 
#{'id': 212234, 'customer': 'harold', 'date': '07/31/2024', 'amount': 2150}, 
#{'id': 911411, 'customer': 'debbie', 'date': '04/20/2024', 'amount': 300},
#{'id': 397861, 'customer': 'barb', 'date': '05/30/2024', 'amount': 670}, 
#{'id': 435298, 'customer': 'jack', 'date': '09/01/2024', 'amount': 400}, 
#{'id': 212234, 'customer': 'harold', 'date': '05/11/2024', 'amount': 3009}
#]


grouper = itemgetter("id","customer")
result = []
for key, grp in groupby(sorted(dictf, key = grouper), grouper):
    temp_dict = dict(zip(["id","customer"], key))
    temp_dict["amount"] = sum(item["amount"] for item in grp)
    #temp_dict["date"] = max(item["date"] for item in grp)
    result.append(temp_dict)
    
#{'id': 212234, 'customer': 'harold', 'amount': 5309}
#{'id': 397861, 'customer': 'barb', 'amount': 760}
#{'id': 435298, 'customer': 'jack', 'amount': 1400}
#{'id': 500001, 'customer': 'alice', 'amount': 3039}
#{'id': 911411, 'customer': 'debbie', 'amount': 300}

#Save customer totals to S3  
df = result
df =pd.DataFrame(df)
df.to_csv("s3://csv/data_trans_totals.csv",header=True,index=False)

#Save customer totals to NoSQL dynamodb
def readf(x):
    for i in x:
        c = i['id']
        b = i['customer']
        d = i['amount']
        response = table.put_item(
           Item={
                'id':c,
                'customer':b,
                'amount':d
                }
        )
readf(result)
#Save customer totals to snowflake, created stage and table prior to copying data
query="COPY INTO customer_totals FROM @customer_totals file_format = (type = 'csv' SKIP_HEADER = 1) ;"
sf = pd.read_sql(query,conn)
