"""
Author: Ryan Lee Jun Xian
Description: This script retrieves weather forecast data from OpenWeatherMap API and exports the data to an Excel file.
"""
import requests
import pandas as pd
import json
import xml.etree.ElementTree as ET
import os

"""
Variables:
    apiKey (str) - OpenWeatherMap API key
    latitude (float) - Latitude of Monash University Malaysia
    longitude (float) - Longitude of Monash University Malaysia
    mode (str) - Mode for data retrieval: "json" or "xml"
    outputFileJson (str) - Output Excel file name for JSON data
    outputFileXml (str) - Output Excel file name for XML data
    output_directory (str) - Output directory for Excel files
"""
apiKey = "b37d117a089ccfe73b56961599bef2aa"
latitude = 3.0602
longitude = 101.6498
mode = "json"
unit = "metric"
outputFileJson = "weather_forecast_json.xlsx"
outputFileXml = "weather_forecast_xml.xlsx"
output_directory = "data"

def parseJsonWeatherData(jsonData):
    """
    Description: This function parses the JSON data and extracts relevant information.
    Input: jsonData (dict) - JSON data
    Output: forecasts (list) - List of dictionaries containing weather forecast data
    """
    forecasts = []
    for forecast in jsonData['list']:
        forecastData = {
            "Time": forecast['dt_txt'],
            "Temperature (Celsius)": forecast['main']['temp'],
            "Feels Like (Celsius)": forecast['main']['feels_like'],
            "Minimum Temperature (Celsius)": forecast['main']['temp_min'],
            "Maximum Temperature (Celsius)": forecast['main']['temp_max'],
            "Pressure (millibars)": forecast['main']['pressure'],
            "Sea Level Pressure (millibars)": forecast['main'].get('sea_level', None),
            "Ground Level Pressure (millibars)": forecast['main'].get('grnd_level', None),
            "Humidity (%)": forecast['main']['humidity'],
            "Temperature KF": forecast['main'].get('temp_kf', None),
            "Weather Condition ID": forecast['weather'][0]['id'],
            "Weather Main": forecast['weather'][0]['main'],
            "Weather Description": forecast['weather'][0]['description'],
            "Weather Icon": forecast['weather'][0]['icon'],
            "Cloudiness (%)": forecast['clouds']['all'],
            "Wind Speed (m/s)": forecast['wind']['speed'],
            "Wind Direction (degrees)": forecast['wind'].get('deg', None),
            "Wind Gust (m/s)": forecast['wind'].get('gust', None),
            "Visibility (kilometers)": forecast.get('visibility', None) / 1000 if forecast.get('visibility', None) else None,
            "Probability of Precipitation": forecast.get('pop', None),
            "Rain Volume (last 3 hours, mm)": forecast['rain'].get('3h', None) if 'rain' in forecast else None,
            "Snow Volume (last 3 hours, mm)": forecast['snow'].get('3h', None) if 'snow' in forecast else None,
            "Part of the Day": forecast['sys']['pod'],
            "City Latitude": jsonData['city']['coord']['lat'],
            "City Longitude": jsonData['city']['coord']['lon'],
            "City Population": jsonData['city']['population'],
            "City Timezone (seconds from UTC)": jsonData['city']['timezone'],
            "City Sunrise (Unix UTC)": jsonData['city']['sunrise'],
            "City Sunset (Unix UTC)": jsonData['city']['sunset']
        }
        forecasts.append(forecastData)
    return forecasts

def parseXmlWeatherData(xml_data):
    """
    Description: This function parses the XML data and extracts relevant information.
    Input: xml_data (str) - XML data
    Output: forecasts (list) - List of dictionaries containing weather forecast data
    """
    root = ET.fromstring(xml_data)
    forecasts = []

    for time in root.findall("./forecast/time"):
        forecast = {
            "Time From": time.attrib.get("from", None),
            "Time To": time.attrib.get("to", None),
            "Weather Condition": time.find("./symbol").attrib.get("name", None),
            "Probability of Precipitation": float(time.find("./precipitation").attrib.get("probability", 0)),
            "Precipitation Unit": time.find("./precipitation").attrib.get("unit", None),
            "Precipitation Volume (mm)": float(time.find("./precipitation").attrib.get("value", 0)),
            "Precipitation Type": time.find("./precipitation").attrib.get("type", None),
            "Wind Direction (degrees)": int(time.find("./windDirection").attrib.get("deg", None)),
            "Wind Direction Code": time.find("./windDirection").attrib.get("code", None),
            "Wind Direction Name": time.find("./windDirection").attrib.get("name", None),
            "Wind Speed (m/s)": float(time.find("./windSpeed").attrib.get("mps", None)),
            "Wind Type": time.find("./windSpeed").attrib.get("nameType", None),
            "Wind Gust (m/s)": float(time.find("./windGust").attrib.get("gust", None)),
            "Temperature": float(time.find("./temperature").attrib.get("value", None)),
            "Minimum Temperature": float(time.find("./temperature").attrib.get("min", None)),
            "Maximum Temperature": float(time.find("./temperature").attrib.get("max", None)),
            "Feels Like Temperature": float(time.find("./feels_like").attrib.get("value", None)),
            "Pressure": float(time.find("./pressure").attrib.get("value", None)),
            "Humidity": int(time.find("./humidity").attrib.get("value", None)),
            "Cloudiness Name": time.find("./clouds").attrib.get("value", None),
            "Cloudiness": int(time.find("./clouds").attrib.get("all", None)),
            "Visibility": int(time.find("./visibility").attrib.get("value", None))
        }
        forecasts.append(forecast)

    return forecasts

def getWeatherForecast(latitude, longitude, apiKey, mode):
    """
    Description: This function retrieves weather forecast data from OpenWeatherMap API.
    Input: 
        latitude (float) - Latitude of the location
        longitude (float) - Longitude of the location
        apiKey (str) - API key for OpenWeatherMap
        mode (str) - Data retrieval mode: "json" or "xml"
    Output:
        Returns a tuple containing the data format and the retrieved weather forecast data.
        If the data format is JSON, the first element of the tuple will be 'json' and the second element will be a dictionary.
        If the data format is XML, the first element of the tuple will be 'xml' and the second element will be a string.
        If the data format is unknown or the weather forecast retrieval fails, both elements of the tuple will be None.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={apiKey}&mode={mode}&units={unit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        if data.startswith('{'):  # JSON data
            return 'json', json.loads(data)
        elif data.startswith('<'):  # XML data
            return 'xml', data
        else:
            print("Unknown data format")
            return None, None
    else:
        print("Failed to retrieve weather forecast")
        return None, None

if __name__ == "__main__":
    # Get weather forecast data
    data_format, weather_data = getWeatherForecast(latitude, longitude, apiKey, mode)
    
    if weather_data:
        if data_format == 'json':
            # Parse the JSON data
            jsonData = parseJsonWeatherData(weather_data)
            
            # Create a DataFrame
            df_json = pd.DataFrame(jsonData)
            
            # Define output file path
            outputFileJson = os.path.join(output_directory, "weatherForecastJson.xlsx")
            
            # Export JSON data to Excel
            df_json.to_excel(outputFileJson, index=False)
            print(f"Weather forecast data (JSON) exported to {outputFileJson}")
        
        elif data_format == 'xml':
            # Parse the XML data
            xml_data = parseXmlWeatherData(weather_data)
            
            # Create a DataFrame
            df_xml = pd.DataFrame(xml_data)
            
            # Define output file path
            outputFileXml = os.path.join(output_directory, "weatherForecastXml.xlsx")
            
            # Export XML data to Excel
            df_xml.to_excel(outputFileXml, index=False)
            print(f"Weather forecast data (XML) exported to {outputFileXml}")
    else:
        print("Weather forecast data not available")