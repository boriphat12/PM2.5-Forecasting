import requests
import pandas as pd
import datetime
import time
from dotenv import load_dotenv
import os
import openmeteo_requests
import requests_cache
from retry_requests import retry

load_dotenv()

API = os.getenv("API_TOKEN")
LAT = 13.754
LON = 100.5014
START_DATE = datetime.datetime(2023, 1, 1).timestamp()
END_DATE = datetime.datetime.now().timestamp()

def fectch_pm25():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={LAT}&lon={LON}&start={int(START_DATE)}&end={int(END_DATE)}&appid={API}"

    print(f"Fetching PM2.5 data")
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
        print(df.head())
        return df
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def fetch_weather():
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": "2023-01-01",
        "end_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "hourly": ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m", "wind_direction_10m"]
    }

    print("Fetching Weather Data")
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_rain = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(4).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temp"] = hourly_temperature_2m
    hourly_data["humidity"] = hourly_relative_humidity_2m
    hourly_data["rain"] = hourly_rain
    hourly_data["wind_speed"] = hourly_wind_speed_10m
    hourly_data["wind_dir"] = hourly_wind_direction_10m

    weather_df = pd.DataFrame(data = hourly_data)
    print(f"Weather Data Fetched: {len(weather_df)} rows")
    #print(weather_df.head())
    weather_df = weather_df.rename(columns={'date': 'datetime'})
    weather_df['datetime'] = weather_df['datetime'].dt.tz_convert('Asia/Bangkok').dt.tz_localize(None)
    return weather_df

pm_df = fectch_pm25()
weather_df = fetch_weather()

final_df = pd.merge(pm_df, weather_df, on='datetime', how='inner')
print(final_df.head())

final_df.to_csv('bangkok_pm25_complete.csv', index=False)