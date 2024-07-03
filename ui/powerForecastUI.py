import streamlit as st
import pandas as pd

def main():
    st.sidebar.title("Power Forecast App")

    # Load power forecast data
    power_data_path = "data/DC_AC_Power_Predictions.csv"
    power_df = pd.read_csv(power_data_path)
    power_df['DATE_TIME'] = pd.to_datetime(power_df['DATE_TIME'])

    # Sidebar - Date selector
    selected_date = st.sidebar.date_input("Select a date", min_value=power_df['DATE_TIME'].min().date(), max_value=power_df['DATE_TIME'].max().date())

    # Filter power data by selected date
    filtered_power_df = power_df[power_df['DATE_TIME'].dt.date == selected_date]

    # Calculate money generated
    money_generated = filtered_power_df['AC_POWER'] * 0.218 / 100  # Convert to Ringgit
    total_earning = money_generated.sum()

    # Load consumption forecast data
    consumption_data_path = "data/updated_consumption_Predictions.csv"
    consumption_df = pd.read_csv(consumption_data_path)
    consumption_df['DATE_TIME'] = pd.to_datetime(consumption_df['hour'])

    # Filter consumption data by selected date
    filtered_consumption_df = consumption_df[consumption_df['DATE_TIME'].dt.date == selected_date]

    # Checkbox for selecting data
    st.sidebar.subheader("Select Data to Display")
    display_ac_power = st.sidebar.checkbox("AC Power")
    display_module_temp = st.sidebar.checkbox("Module Temperature")
    display_irradiation = st.sidebar.checkbox("Irradiation")
    display_power_consumption = st.sidebar.checkbox("Power Consumption")
    display_money_generated = st.sidebar.checkbox("Money Generated")

    # Plot
    st.subheader("Power Forecast for {}".format(selected_date))
    col1, col2 = st.columns(2)
    with col1:
        if display_ac_power:
            st.subheader("AC Power (Predicted)")
            st.write("AC Power represents the electrical power output from the solar panels.")
            st.area_chart(filtered_power_df[['DATE_TIME', 'AC_POWER']].set_index('DATE_TIME'))
        if display_module_temp:
            st.subheader("Module Temperature (Predicted)")
            st.write("Module Temperature represents the temperature of the solar panels.")
            st.area_chart(filtered_power_df[['DATE_TIME', 'MODULE_TEMPERATURE']].set_index('DATE_TIME'))

    with col2:
        if display_irradiation:
            st.subheader("Irradiation (Predicted)")
            st.write("Irradiation represents the solar energy received per unit area.")
            st.area_chart(filtered_power_df[['DATE_TIME', 'IRRADIATION']].set_index('DATE_TIME'))
        if display_power_consumption:
            st.subheader("Power Consumption (Predicted)")
            st.write("Power Consumption represents the electrical power usage.")
            try:
                st.area_chart(filtered_consumption_df[['DATE_TIME', 'power consumption']].set_index('DATE_TIME'))
            except KeyError:
                st.error("Column 'power consumption' not found in the consumption data.")
        if display_money_generated:
            st.subheader("Money Generated (Predicted)")
            st.write("The amount of money generated based on the AC power data (0.218 per kWh), in Ringgit.")
            st.line_chart(pd.DataFrame({'DATE_TIME': filtered_power_df['DATE_TIME'], 'Money Generated (kiloRinggit)': money_generated}).set_index('DATE_TIME'))
            st.write("Total earnings for the day: RM {:.2f} Ringgit".format(total_earning))

    st.write("**Note:** All displayed data are predicted values.")

    # Retrieve settings from settingUI.py using st.session_state
    christmas_mode = st.session_state.christmas_mode
    # Check if Christmas mode is enabled
    if christmas_mode:
        st.snow()

if __name__ == "__main__":
    main()
