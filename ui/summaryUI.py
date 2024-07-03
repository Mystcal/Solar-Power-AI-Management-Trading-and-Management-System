import streamlit as st
import numpy as np
import time
import pandas as pd
import settingUI

battery_percentage_min = settingUI.get_battery_percentage_min()
battery_percentage_max = settingUI.get_battery_percentage_max()

# Define global variables
solar_power = np.random.uniform(8, 10) * 0.25  # Reduced fluctuation by 50%
battery_power = float(50)  # Battery charge percentage
home_usage = np.random.uniform(9, 11) * 0.25  # Reduced fluctuation by 50%
grid_usage = solar_power if battery_power >= 100 else max(0, home_usage - solar_power)
credit = 0  # Initial credit

# Lists to store data for line charts
solar_data = []
home_data = []
grid_data = []
battery_data = []

# Function to generate random data for the main summary
def generate_random_data(battery_override=False):
    global solar_power, home_usage, grid_usage, battery_power, credit

    if grid_usage != 0:
        grid_usage = 0

    battery_percentage_min = settingUI.get_battery_percentage_min()
    battery_percentage_max = settingUI.get_battery_percentage_max()

    # Update values with +-10% variation
    solar_power = round(np.random.uniform(solar_power * 0.9, solar_power * 1.1), 2)
    home_usage = round(np.random.uniform(home_usage * 0.9, home_usage * 1.1), 2)
    
    # Check if battery override is active
    if battery_override:
        battery_power = st.slider("Battery Charge (%)", min_value=float(0), max_value=float(100), value=battery_power)
        if battery_power >= battery_percentage_max:
            surplus = battery_power - battery_percentage_max
            grid_usage = surplus
        elif battery_power <= battery_percentage_min:
            deficit = battery_power - battery_percentage_min
            grid_usage = deficit
        else:
            1+1  # Do nothing
    else:
        if battery_power >= battery_percentage_max:
            surplus = battery_power - battery_percentage_max
            battery_power -= surplus
            grid_usage = surplus
        elif battery_power <= battery_percentage_min:
            deficit = battery_power - battery_percentage_min
            battery_power += deficit
            grid_usage = deficit
        else:
            # Use solar power for home
            battery_power += solar_power - home_usage
    
    # Cap battery charge between 0 and 100
    battery_power = max(0, min(battery_power, 100))
    
    # Update credit
    credit += grid_usage * 0.0218  # Assuming rate is 0.218 RM/kWh

    # Append data to lists for line charts
    solar_data.append(solar_power)
    home_data.append(home_usage)
    grid_data.append(grid_usage * -1)
    battery_data.append(battery_power)
    
    # Keep only the last 4 values for each list
    if len(solar_data) > 4:
        solar_data.pop(0)
        home_data.pop(0)
        grid_data.pop(0)
        battery_data.pop(0)

# Function to provide recommendation based on battery charge
def get_recommendation(charge):
    if charge <= 1:
        return "Your battery is critically low, but don't worry! We are currently buying power from the grid. 🔌"
    elif charge <= 25:
        return "Your battery is low. Consider reducing power usage. 📉"
    elif charge >= 75:
        return "Your battery is almost full. Good job on managing your power usage! 🌞"
    elif charge >= 99:
        return "Your battery is fully charged! We are currently selling excess power back to the grid. You are being compensated in electricity credits! 🌞"
    else:
        return "Your battery is at a good level. Keep up the good work! 🌟"

# Function to display the summary
def main():
    global battery_power, credit, grid_usage

    # Add sidebar items
    st.sidebar.write("### Settings")
    battery_override = st.sidebar.toggle("Battery Override")
    st.sidebar.write("### Recommendation")
    st.sidebar.write(get_recommendation(battery_power))
    
    while True:       
        # Generate random summary data
        generate_random_data(battery_override)
        
        # Display summary data in three columns
        st.write("### Current Summary")
        col1, col2, col3, col4 = st.columns(4)

        # Column 1: Solar Power In and Home Usage
        with col1:
            # Line chart for solar power
            st.write("#### Solar Power")
            st.area_chart(pd.DataFrame({'Solar Power': solar_data[-4:]}), height=384, color="#FFFF00")
            st.write(f"#### Solar Power In (kW): {solar_power:.2f}")

        # Column 2: Battery Charge, Charging/Discharging, Grid Usage
        with col2:
            # Line chart for Home power
            st.write("#### Home Usage Trend")
            st.area_chart(pd.DataFrame({'Home Usage': home_data[-4:]}), height=384)
            # Display home usage
            st.write(f"#### Home Usage (kW): {home_usage:.2f}")

        with col3:
            # Line chart for grid power
            st.write("#### Grid Power Trend")
            st.area_chart(pd.DataFrame({'Grid Usage': grid_data[-4:]}), height=384, color="#FF0000")
            st.write(f"#### Usage (kW): {grid_usage * -1:.2f}")
            # Display credit
            st.write(f"#### Credit: RM {credit:.2f}")

        with col4:
            # Display battery charge
            st.write("#### Battery Charge")
            st.area_chart(pd.DataFrame({'Charge (%)': battery_data[-4:]}), height=384, color="#00FF00")
            st.write(f"#### Charge (%): {battery_power:.2f}")
        time.sleep(1)  # Update every second
        st.rerun()  # Rerun the app to update the UI

if __name__ == "__main__":
    main()
