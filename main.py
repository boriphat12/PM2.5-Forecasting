import requests
import pandas as pd
import datetime
import time
from dotenv import load_dotenv
import os

load_dotenv()

API = os.getenv("API_TOKEN")
LAT = 13.7539
LON = 100.6015
START_DATE = datetime.datetime(2023, 1, 1).timestamp()
END_DATE = datetime.datetime.now().timestamp()

url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={LAT}&lon={LON}&start={int(START_DATE)}&end={int(END_DATE)}&appid={API}"

print(f"Fetching data...")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    coord_list = data['list']
    formatted_date = []

    for item in coord_list:
        timestamp = datetime.datetime.fromtimestamp(item['dt'])
        components = item['components']

        co = components['co']
        no = components['no']
        no2 = components['no2']
        o3 = components['o3']
        so2 = components['so2']
        pm2_5 = components['pm2_5']
        pm10 = components['pm10']
        nh3 = components['nh3']

        formatted_date.append([timestamp, pm2_5, pm10, co, no, no2, o3, so2, nh3])

    columns = ['datetime', 'pm2.5', 'pm10', 'co', 'no', 'no2', 'o3', 'so2', 'nh3']
    df = pd.DataFrame(formatted_date, columns=columns)
    filename = 'bangkok_pm25_history.csv'
    df.to_csv(filename)
    print(f"save data: {filename}")
    print(df.head())
else:
    print(f"Error: {response.status_code}")
    print(response.text)