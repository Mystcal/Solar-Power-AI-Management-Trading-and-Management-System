import streamlit as st
import pandas as pd
import subprocess

# Load weather data from CSV
weather_data = pd.read_csv("data/weatherHourlyForecast.csv")

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


def refresh_data():
    subprocess.run(["python", "dataProcessing/dataProcessingMain.py"])

# Create a function to display the selected chart
def display_chart(selected_chart, selected_date, show_description=False):
    filtered_data = weather_data[pd.to_datetime(weather_data2["Time"]).dt.date == selected_date]
    if selected_chart == "Temperature":
        st.subheader("Temperature Data")
        if show_description:
            st.write("Temperature data includes the actual temperature (Temperature), the perceived temperature (Feels Like), the minimum temperature (Min Temperature), and the maximum temperature (Max Temperature) during the forecast period.")
            st.write("**Fun Fact:** Did you know that the highest temperature ever recorded on Earth was 56.7°C (134°F) in Furnace Creek Ranch, Death Valley, California, USA?")
        # Plot temperature related data
        temperature_data = filtered_data[["Time", "Temperature", "Feels Like"]]
        temperature_data.set_index("Time", inplace=True)
        st.line_chart(temperature_data)
    elif selected_chart == "Pressure":
        st.subheader("Pressure Data")
        if show_description:
            st.write("Pressure data includes the atmospheric pressure at sea level (Pressure), the atmospheric pressure at sea level (Sea Level Pressure), and the atmospheric pressure at ground level (Ground Level Pressure) during the forecast period.")
            st.write("**Fun Fact:** Did you know that atmospheric pressure decreases with altitude? That's why it's harder to breathe at high altitudes.")
        # Plot pressure related data
        pressure_data = filtered_data[["Time", "Pressure", "Sea Level Pressure", "Ground Level Pressure"]]
        pressure_data.set_index("Time", inplace=True)
        st.bar_chart(pressure_data)
    elif selected_chart == "Humidity":
        st.subheader("Humidity Data")
        if show_description:
            st.write("Humidity data represents the percentage of water vapor in the air during the forecast period.")
            st.write("**Fun Fact:** Did you know that high humidity levels can make it feel hotter than it actually is? That's because sweat evaporates more slowly in humid conditions.")
        # Plot humidity data
        humidity_data = filtered_data[["Time", "Humidity"]]
        humidity_data.set_index("Time", inplace=True)
        st.line_chart(humidity_data)
    elif selected_chart == "Cloud Cover":
        st.subheader("Cloud Cover Data")
        if show_description:
            st.write("Cloud cover data represents the percentage of the sky covered by clouds during the forecast period.")
            st.write("**Fun Fact:** Did you know that clouds play a crucial role in regulating the Earth's temperature? They reflect sunlight back into space, helping to cool the planet.")
        # Plot cloud cover data
        cloud_cover_data = filtered_data[["Time", "Cloudiness"]]
        cloud_cover_data.set_index("Time", inplace=True)
        st.area_chart(cloud_cover_data)
    elif selected_chart == "Wind":
        st.subheader("Wind Data")
        if show_description:
            st.write("Wind data includes the wind speed (Wind Speed) and wind gust (Wind Gust) during the forecast period.")
            st.write("**Fun Fact:** Did you know that wind energy is one of the fastest-growing renewable energy sources? It's clean, abundant, and can be harnessed in various ways.")
        # Plot wind speed and gust data
        wind_data = filtered_data[["Time", "Wind Speed", "Wind Gust"]]
        wind_data.set_index("Time", inplace=True)
        st.line_chart(wind_data)
    elif selected_chart == "Wind Direction":
        st.subheader("Wind Direction Data")
        if show_description:
            st.write("Wind direction data represents the direction from which the wind is blowing in degrees during the forecast period.")
            st.write("**Fun Fact:** Did you know that wind direction is reported as the direction the wind is coming from? For example, a north wind blows from the north towards the south.")
        # Plot wind direction data
        wind_direction_data = filtered_data[["Time", "Wind Direction"]]
        wind_direction_data.set_index("Time", inplace=True)
        st.line_chart(wind_direction_data)
    elif selected_chart == "Rain Volume":
        st.subheader("Rain Volume Data")
        if show_description:
            st.write("Rain volume data represents the amount of rainfall in millimeters during the forecast period.")
            st.write("**Fun Fact:** Did you know that the world's rainiest place is Mawsynram, India? It receives an average annual rainfall of around 11,871 millimeters (467.4 inches)!")
        # Plot rain volume data
        rain_volume_data = filtered_data[["Time", "Rain Volume"]]
        rain_volume_data.set_index("Time", inplace=True)
        st.scatter_chart(rain_volume_data)
    elif selected_chart == "Weather Description":
        st.subheader("Weather Description Data")
        if show_description:
            st.write("Weather description data provides a textual description of the weather conditions during the forecast period.")
            st.write("**Fun Fact:** Did you know that there are over a dozen different types of clouds, each with its own unique characteristics? From fluffy cumulus clouds to towering cumulonimbus clouds, there's a lot to learn about cloud formations!")
        # Plot weather description data
        weather_description_data = filtered_data[["Time", "Weather Description"]]
        weather_description_data.set_index("Time", inplace=True)
        st.bar_chart(weather_description_data)


# Main function
def main():
    # Retrieve settings from settingUI.py using st.session_state
    christmas_mode = st.session_state.christmas_mode
    # Check if Christmas mode is enabled
    if christmas_mode:
        st.snow()
    # Sidebar date selection
    selected_date = st.sidebar.date_input("Select Date", min_value=pd.to_datetime(weather_data2["Time"]).dt.date.min(), max_value=pd.to_datetime(weather_data2["Time"]).dt.date.max())
    
    if st.sidebar.button("Update Data", key="update_data"):
        refresh_data()
        st.rerun()
    # Add popover for selecting the chart
    with st.sidebar:
        show_description = st.toggle("Show Chart Descriptions")
    # Display the selected chart in two columns
    col1, col2 = st.columns(2)
    with col1:
        display_chart("Temperature", selected_date, show_description)
        display_chart("Pressure", selected_date, show_description)
        display_chart("Humidity", selected_date, show_description)
        display_chart("Cloud Cover", selected_date, show_description)
    with col2:
        display_chart("Wind", selected_date, show_description)
        display_chart("Wind Direction", selected_date, show_description)
        display_chart("Rain Volume", selected_date, show_description)
        display_chart("Weather Description", selected_date, show_description)

if __name__ == "__main__":
    main()
