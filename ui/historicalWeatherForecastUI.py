import streamlit as st
import pandas as pd
import subprocess

# Load historical weather data from CSV
weather_data = pd.read_csv("data/historicalWeatherForecast.csv")

# Rename columns
weather_data = weather_data.rename(columns={
    "dt_txt": "Time",
    "main.temp": "Temperature",
    "main.feels_like": "Feels Like",
    "main.temp_min": "Min Temperature",
    "main.temp_max": "Max Temperature",
    "main.pressure": "Pressure",
    "main.sea_level": "Sea Level Pressure",
    "main.grnd_level": "Ground Level Pressure",
    "main.humidity": "Humidity",
    "clouds.all": "Cloudiness",
    "wind.speed": "Wind Speed",
    "wind.deg": "Wind Direction",
    "wind.gust": "Wind Gust",
    "rain.3h": "Rain Volume",
    "weather_description": "Weather Description"
})

weather_data2 = weather_data.copy()

# Format time column
weather_data["Time"] = pd.to_datetime(weather_data["Time"]).dt.strftime("%d %I%p")

# Function to refresh data
def refresh_data():
    subprocess.run(["python", "dataProcessing/dataProcessingMain.py"])

# Create a function to display the selected chart
def display_chart(selected_chart, selected_date, show_description=False):
    filtered_data = weather_data[pd.to_datetime(weather_data2["Time"]).dt.date == selected_date]

    if selected_chart == "Temperature":
        st.subheader("Temperature Data")
        if show_description:
            st.write("Temperature data includes the actual temperature (Temperature), the perceived temperature (Feels Like), the minimum temperature (Min Temperature), and the maximum temperature (Max Temperature) during the forecast period.")
        # Plot temperature related data
        temperature_data = filtered_data[["Time", "Temperature", "Feels Like", "Min Temperature", "Max Temperature"]]
        temperature_data.set_index("Time", inplace=True)
        st.line_chart(temperature_data)
    elif selected_chart == "Pressure":
        st.subheader("Pressure Data")
        if show_description:
            st.write("Pressure data includes the atmospheric pressure at sea level (Pressure), the atmospheric pressure at sea level (Sea Level Pressure), and the atmospheric pressure at ground level (Ground Level Pressure) during the forecast period.")
        # Plot pressure related data
        pressure_data = filtered_data[["Time", "Pressure", "Sea Level Pressure", "Ground Level Pressure"]]
        pressure_data.set_index("Time", inplace=True)
        st.bar_chart(pressure_data)
    elif selected_chart == "Humidity":
        st.subheader("Humidity Data")
        if show_description:
            st.write("Humidity data represents the percentage of water vapor in the air during the forecast period.")
        # Plot humidity data
        humidity_data = filtered_data[["Time", "Humidity"]]
        humidity_data.set_index("Time", inplace=True)
        st.line_chart(humidity_data)
    elif selected_chart == "Cloud Cover":
        st.subheader("Cloud Cover Data")
        if show_description:
            st.write("Cloud cover data represents the percentage of the sky covered by clouds during the forecast period.")
        # Plot cloud cover data
        cloud_cover_data = filtered_data[["Time", "Cloudiness"]]
        cloud_cover_data.set_index("Time", inplace=True)
        st.area_chart(cloud_cover_data)
    elif selected_chart == "Wind":
        st.subheader("Wind Data")
        if show_description:
            st.write("Wind data includes the wind speed (Wind Speed) and wind gust (Wind Gust) during the forecast period.")
        # Plot wind speed and gust data
        wind_data = filtered_data[["Time", "Wind Speed", "Wind Gust"]]
        wind_data.set_index("Time", inplace=True)
        st.line_chart(wind_data)
    elif selected_chart == "Wind Direction":
        st.subheader("Wind Direction Data")
        if show_description:
            st.write("Wind direction data represents the direction from which the wind is blowing in degrees during the forecast period.")
        # Plot wind direction data
        wind_direction_data = filtered_data[["Time", "Wind Direction"]]
        wind_direction_data.set_index("Time", inplace=True)
        st.line_chart(wind_direction_data)
    elif selected_chart == "Rain Volume":
        st.subheader("Rain Volume Data")
        if show_description:
            st.write("Rain volume data represents the amount of rainfall in millimeters during the forecast period.")
        # Plot rain volume data
        rain_volume_data = filtered_data[["Time", "Rain Volume"]]
        rain_volume_data.set_index("Time", inplace=True)
        st.scatter_chart(rain_volume_data)
    elif selected_chart == "Weather Description":
        st.subheader("Weather Description Data")
        if show_description:
            st.write("Weather description data provides a textual description of the weather conditions during the forecast period.")
        # Plot weather description data
        weather_description_data = filtered_data[["Time", "Weather Description"]]
        weather_description_data.set_index("Time", inplace=True)
        st.bar_chart(weather_description_data)

# Main function
def main():
    christmas_mode = st.session_state.christmas_mode
    # Check if Christmas mode is enabled
    if christmas_mode:
        st.snow()
    # Sidebar date selection
    selected_date = st.sidebar.date_input("Select Date", min_value=pd.to_datetime(weather_data2["Time"]).dt.date.min(), max_value=pd.to_datetime(weather_data2["Time"]).dt.date.max())

    with st.sidebar:
        show_description = st.toggle("Show Chart Descriptions")

    # Checkbox to select data for display
    st.sidebar.subheader("Select Data to Display")
    display_temperature = st.sidebar.checkbox("Temperature")
    display_pressure = st.sidebar.checkbox("Pressure")
    display_humidity = st.sidebar.checkbox("Humidity")
    display_cloud_cover = st.sidebar.checkbox("Cloud Cover")
    display_wind = st.sidebar.checkbox("Wind")
    display_wind_direction = st.sidebar.checkbox("Wind Direction")
    display_rain_volume = st.sidebar.checkbox("Rain Volume")
    display_weather_description = st.sidebar.checkbox("Weather Description")

    col1, col2 = st.columns(2)

    with col1:
        # Display the selected chart
        if display_temperature:
            display_chart("Temperature", selected_date, show_description)
        if display_pressure:
            display_chart("Pressure", selected_date, show_description)
        if display_humidity:
            display_chart("Humidity", selected_date, show_description)
        if display_cloud_cover:
            display_chart("Cloud Cover", selected_date, show_description)
    with col2:
        if display_wind:
            display_chart("Wind", selected_date, show_description)
        if display_wind_direction:
            display_chart("Wind Direction", selected_date, show_description)
        if display_rain_volume:
            display_chart("Rain Volume", selected_date, show_description)
        if display_weather_description:
            display_chart("Weather Description", selected_date, show_description)

if __name__ == "__main__":
    main()
