import streamlit as st
battery_percentage_min = 20
battery_percentage_max = 80
def get_battery_percentage_min():
    return battery_percentage_min
def get_battery_percentage_max():
    return battery_percentage_max
def set_battery_percentage_min(value):
    global battery_percentage_min
    battery_percentage_min = value
def set_battery_percentage_max(value):
    global battery_percentage_max
    battery_percentage_max = value

def main():
    st.title("Settings")

    # Initialize session_state variables if not already present
    if 'offgrid' not in st.session_state:
        st.session_state.offgrid = False
    if 'battery_percentage' not in st.session_state:
        st.session_state.battery_percentage = (20, 80)
    if 'opt_out' not in st.session_state:
        st.session_state.opt_out = False
    if 'christmas_mode' not in st.session_state:
        st.session_state.christmas_mode = False

    st.subheader("Offgrid Option")
    offgrid = st.toggle("Offgrid", key="offgrid_toggle", value=st.session_state.offgrid)
    st.session_state.offgrid = offgrid
    if offgrid:
        st.write("Offgrid mode enabled. This mode strictly uses battery and solar power until empty and won't draw power from the grid.")

    st.subheader("Battery Conservation")
    battery_percentage = st.slider("Battery Percentage", 0, 100, st.session_state.battery_percentage, key="battery_percentage_slider")
    st.session_state.battery_percentage = battery_percentage
    st.write(f"Conserve battery between {battery_percentage[0]}% and {battery_percentage[1]}% before selling.")
    set_battery_percentage_min(battery_percentage[0])
    set_battery_percentage_max(battery_percentage[1])

    st.subheader("User Experience and Data Collection")
    opt_out = st.toggle("Opt Out", key="opt_out_toggle", value=st.session_state.opt_out)
    st.session_state.opt_out = opt_out
    if opt_out:
        st.write("Opting out of user experience and data collection.")

    st.subheader("Christmas Mode")
    christmas_mode = st.toggle("Christmas Mode", key="christmas_mode_toggle", value=st.session_state.christmas_mode)
    st.session_state.christmas_mode = christmas_mode
    if christmas_mode:
        st.write("Christmas Mode enabled. Snowflakes will appear each time anything is pressed.")
        st.snow()

if __name__ == "__main__":
    main()
