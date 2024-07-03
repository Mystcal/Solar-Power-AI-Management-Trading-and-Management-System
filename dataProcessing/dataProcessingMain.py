"""
Author: Ryan Lee Jun Xian
Description: 
"""

"""
Imports:
    get_solar_data - Function to retrieve solar data from OpenWeatherMap API
    export_to_excel - Function to export solar data to an Excel file
"""
from dataProcessingSolarIrradiance import get_solar_data, export_solar_to_csv
from dataProcessingWeather import get_weather_data, export_weather_to_csv
"""
Global Variables:
"""
latitude = 3.0625  # Latitude of Monash University Malaysia
longitude = 101.6144  # Longitude of Monash University Malaysia
date = "2023-03-30"  # Example date
timezone = "+08:00"  # Timezone of Malaysia
api_key = "b37d117a089ccfe73b56961599bef2aa"  # Your unique API key

# Retrieve weather data
weather_data = get_weather_data(latitude, longitude, api_key)
if weather_data:
    export_weather_to_csv(weather_data, "weatherHourlyForecast.csv")
else:
    print("No weather data retrieved.")

# # Retrieve solar data
# solar_data = get_solar_data(latitude, longitude, date, timezone, api_key)
# if solar_data:
#     export_solar_to_csv(solar_data, "solarIrradiance.csv")
# else:
#     print("No solar data retrieved.")