import gspread
from pandas import DataFrame
from oauth2client.service_account import ServiceAccountCredentials
import boto3
import io

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('dailyfantasybuzz.json', scope)
client = gspread.authorize(creds)
sheet = client.open('DFS Project NBA')
sheet_instance = sheet.get_worksheet(4)

records_data = sheet_instance.get_all_records()
df = DataFrame(records_data)
df = df[['Nickname', 'Position', 'Team', 'Over_Under', 'Current Average', 'Salary', 'Value 2', 'Spread', 'Projection']]

s3 = boto3.client(service_name='s3',
                  region_name='us-east-1',
                  aws_access_key_id='accesskey',
                  aws_secret_access_key='secretkey')

bucket = 'dwhredshift2'

with io.StringIO() as csv_buffer:
    df.to_csv(csv_buffer, index=False)

    response = s3.put_object(Bucket=bucket, Key='dfb_060521.csv', Body=csv_buffer.getvalue())

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"successful S3 put response. Status - {status} ")

    else:
        print(f"Unsuccessful S3 put response. Status - {status} ")
