import streamlit as st
import pandas as pd
import datetime
import summaryUI
import weatherForecastUI
import historicalWeatherForecastUI
import powerForecastUI
import settingUI
import subprocess

st.set_page_config(layout='wide')

def refresh_data():
    subprocess.run(["python", "dataProcessing/dataProcessingMain.py"])

# Initialize session_state variables if not already present
if 'offgrid' not in st.session_state:
    st.session_state.offgrid = False
if 'battery_percentage' not in st.session_state:
    st.session_state.battery_percentage = (20, 80)
if 'opt_out' not in st.session_state:
    st.session_state.opt_out = False
if 'christmas_mode' not in st.session_state:
    st.session_state.christmas_mode = False

# Function to authenticate user
def authenticate(username, password):
    # Hardcoded authentication for demonstration purposes
    if username == "Ryan Lee" and password == "password":
        return True
    else:
        return False

# Function to display login form
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.username = username
            st.session_state.logged_in = True
            st.session_state.profile_picture = "data/pfp.png"
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Function to load weather data and get current weather condition
def load_weather_data():
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

    # Format time column
    weather_data["Time"] = pd.to_datetime(weather_data["Time"]).dt.strftime("%I%p")

    current_weather_condition = weather_data["Weather Description"].iloc[0]
    weather_icon_code = weather_data["weather_icon"].iloc[0]
    forecast_data = weather_data.iloc[1:5]  # Next 4-hour forecast
    return current_weather_condition, weather_icon_code, forecast_data

# Function to get icon URL
def get_weather_icon_url(weather_icon_code):
    return f"https://openweathermap.org/img/wn/{weather_icon_code}@2x.png"

# Function to display current time
def display_current_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    st.empty().write(f"# Current Time: {current_time}")

# Main function to run the main energy management dashboard
def main():
    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        # Initialize username and profile_picture if not already initialized
        if "username" not in st.session_state:
            st.session_state.username = ""
        if "profile_picture" not in st.session_state:
            st.session_state.profile_picture = "data/pfp.png"

        st.sidebar.image(st.session_state.profile_picture, width=100)
        st.sidebar.markdown(f"**Logged in as {st.session_state.username}**")

        # Add sidebar for navigation
        page = st.sidebar.selectbox("Navigation", ["Home", "Summary", "Power Forecast", "Weather Forecast", "Historical Weather Forecast", "Setting"], key="navigation_selectbox")
        
        if page == "Home":
            display_current_time()
            st.title('Energy Management Dashboard')
            st.write(f"# Welcome back, {st.session_state.username}!")
            st.write("This dashboard provides an overview of the energy consumption and weather forecast for your house.")
            if st.sidebar.button("Update Data", key="update_data_main"):
                refresh_data()
                st.rerun()

            # Display current weather information on the home page
            st.header("Now")
            col1, col2, col3 = st.columns(3)

            with col1:
                weather_condition, weather_icon_code, forecast_data = load_weather_data()
                st.write(f"# {forecast_data['Temperature'].iloc[0]}°C")
                st.write(f"High: {forecast_data['Max Temperature'].iloc[0]}°C Low: {forecast_data['Min Temperature'].iloc[0]}°C")
            with col2:
                weather_icon_url = get_weather_icon_url(weather_icon_code)
                st.image(weather_icon_url, width=100)
            with col3:
                st.write(f"## {weather_condition}")
                st.write(f"Feels like: {forecast_data['Feels Like'].iloc[0]}°C")
            
            # Display 3-hour forecast
            st.header("3-Hour Forecast")
            cols = st.columns(4)
            for i, (_, row) in enumerate(forecast_data.iterrows()):
                cols[i].write(f"Temperature: {row['Temperature']}°C")
                icon_url = get_weather_icon_url(row['weather_icon'])
                cols[i].image(icon_url, use_column_width=True)
                cols[i].write(f"Time: {row['Time']}")
        elif page == "Summary":
            summaryUI.main()
        elif page == "Power Forecast":
            powerForecastUI.main()
        elif page == "Weather Forecast":
            weatherForecastUI.main()
        elif page == "Historical Weather Forecast":
            historicalWeatherForecastUI.main()
        elif page == "Setting":
            settingUI.main()

    # Retrieve settings from settingUI.py using st.session_state
    christmas_mode = st.session_state.christmas_mode
    # Check if Christmas mode is enabled
    if christmas_mode:
        st.snow()

# Run the main energy management dashboard
if __name__ == "__main__":
    main()
