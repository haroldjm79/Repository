import gspread
from pandas import DataFrame
from datetime import date
from conn import credentials, conn

# Access Data from GCP
client = gspread.authorize(credentials)

sheet = client.open('DFS')
sheet_instance = sheet.get_worksheet(0)

records_data = sheet_instance.get_all_records()

today = date.today()
df = DataFrame(records_data)

df = df.rename(columns={'Over/Under': 'over_under', 'AvgPointsPerGame': 'ppg', 'Roster Position': 'roster_position',
                        'TeamAbbrev': 'game_info', 'Best Value': 'Value'})
df['projection'] = 0
df['Date'] = today
df['id'] = 1
df = df[['Date', 'Name', 'id', 'roster_position', 'Salary', 'game_info', 'over_under', 'ppg', 'Value', 'projection']]
df.to_csv('DailyFBFiles/week1_update.csv', index=False)

# Upload to Postgres
cursor = conn.cursor()


with open('DailyFBFiles/week1_update.csv', 'r') as f:
    try:
        next(f)
        cursor.copy_from(f, 'dfbnfl', sep=',')
        print("File successfully loaded into DK NFL!")
    except Exception as e:
        print("Cannot import destination file into DK: ", e)

conn.commit()

conn.close()
