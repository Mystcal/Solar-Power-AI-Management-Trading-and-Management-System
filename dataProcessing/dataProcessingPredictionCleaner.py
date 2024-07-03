import pandas as pd

# Read the CSV file
data = pd.read_csv("data/consumption_Predictions.csv")

# Set the start date to 2024-05-11
start_date = pd.Timestamp("2024-05-11")

# Initialize variables
current_date = start_date
hours = []

# Create a list of hours repeated 6 times each
for hour in range(24):
    hours.extend([f"{hour:02d}:00:00"] * 6)

# Repeat the process for each day
hour_index = 0
for i in range(len(data)):
    if hour_index == len(hours):
        hour_index = 0
        current_date += pd.Timedelta(days=1)
    data.at[i, 'hour'] = pd.Timestamp.combine(current_date, pd.Timestamp(hours[hour_index]).time())
    hour_index += 1

# Save the updated data to a new CSV file
data.to_csv("data/updated_consumption_Predictions.csv", index=False)
