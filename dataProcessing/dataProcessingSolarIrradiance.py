"""
Author: Ryan Lee Jun Xian
Description: Functions to retrieve solar data from OpenWeatherMap and export it to a CSV file.
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

def get_solar_data(latitude, longitude, date, timezone, api_key):
    """
    Description: Retrieve solar data from OpenWeatherMap API.
    Input:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        date (str): Date in the 'YYYY-MM-DD' format for which data is requested.
        timezone (str): Timezone in the '±XX:XX' format.
        api_key (str): Your unique API key.
    Output:
        dict: Solar data for the given location and date.
    """
    base_url = "https://api.openweathermap.org/energy/1.0/solar/data"
    api_call_url = f"{base_url}?lat={latitude}&lon={longitude}&date={date}&tz={timezone}&appid={api_key}"
    
    response = requests.get(api_call_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve solar data. Status code: {response.status_code}")
        return None

def export_solar_to_csv(data, filename):
    """
    Description: Export data to a CSV file.
    Input: 
        data (dict): Solar data.
        filename (str): Name of the CSV file.
    """
    hourly_data = data['irradiance']['hourly']
    df = pd.DataFrame(hourly_data)
    df_clear_sky = pd.DataFrame(df['clear_sky'].tolist())
    df_clear_sky.columns = [f"clear_{col}" for col in df_clear_sky.columns]  # Prefix clear sky columns
    df_cloudy_sky = pd.DataFrame(df['cloudy_sky'].tolist())
    df_cloudy_sky.columns = [f"cloudy_{col}" for col in df_cloudy_sky.columns]  # Prefix cloudy sky columns
    df_combined = pd.concat([df[['hour']], df_clear_sky, df_cloudy_sky], axis=1)
    output_folder = "data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, filename)
    df_combined.to_csv(output_path, index=False)
    print(f"Data exported to {output_path}")