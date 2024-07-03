"""
Author: Ryan Lee Jun Xian
Description: Functions to retrieve weather data from OpenWeatherMap and export it to a CSV file.
"""

"""
Imports:
    requests - Retrieve data from OpenWeatherMap API
    pandas - Data manipulation and export to Excel
    os - Create directories
"""
import requests
import pandas as pd
import os

def get_weather_data(latitude, longitude, api_key):
    """
    Description: Retrieve weather forecast data from OpenWeatherMap API.
    
    Input:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        api_key (str): Your unique API key.
    
    Output:
        dict: Weather forecast data for the given location.
    """
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    units = "metric"  # Use metric units
    api_call_url = f"{base_url}?lat={latitude}&lon={longitude}&appid={api_key}&units={units}"
    
    response = requests.get(api_call_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve weather forecast data. Status code: {response.status_code}")
        return None

def export_weather_to_csv(weather_data, filename):
    """
    Export weather forecast data to a CSV file, merging with existing data if available.
    """
    hourly_forecast_data = weather_data['list']
    df_new = pd.json_normalize(hourly_forecast_data)
    
    # Parse nested JSON columns
    if 'main' in df_new.columns:
        main_columns = ['temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'sea_level', 'grnd_level', 'humidity', 'temp_kf']
        df_main = pd.json_normalize(df_new['main'])
        df_main.columns = [f"main_{col}" for col in df_main.columns]
        df_new = pd.concat([df_new, df_main], axis=1)
        df_new.drop(columns=['main'], inplace=True)
    
    if 'weather' in df_new.columns:
        df_weather = pd.json_normalize(df_new['weather'])
        for col in df_weather.columns:
            df_new[f"weather_{col}"] = df_weather[col]
        df_new.drop(columns=['weather'], inplace=True)
        # Normalize further for nested weather columns
        df_weather_main = pd.json_normalize(df_new['weather_0'])
        for col in df_weather_main.columns:
            df_new[f"weather_{col}"] = df_weather_main[col]
        df_new.drop(columns=['weather_0'], inplace=True)
    
    # Export new data to a new CSV file
    output_folder = "data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path_new = os.path.join(output_folder, filename)
    df_new.to_csv(output_path_new, index=False)
    print(f"Weather forecast data exported to {output_path_new}")

    # Check if historical data file exists
    historical_file = "historicalWeatherForecast.csv"
    if os.path.exists(historical_file):
        # Load existing historical data
        df_existing = pd.read_csv(historical_file)
        # Merge new data with existing data based on timestamp
        df_merged = pd.concat([df_existing, df_new]).drop_duplicates(subset=['dt'], keep='last')
        df_merged.to_csv(historical_file, index=False)
        print(f"Weather forecast data merged and updated in {historical_file}")
    else:
        # Export new data to a new CSV file
        output_path_historical = os.path.join(output_folder, historical_file)
        df_new.to_csv(output_path_historical, index=False)
        print(f"Weather forecast data exported to {output_path_historical}")