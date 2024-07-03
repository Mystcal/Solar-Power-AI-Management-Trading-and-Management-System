#%%
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Input
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
from model_2 import train_model,prepare_data,train_consumption_model

power_data = pd.read_csv("Power_Generation_Data.csv")
weather_data = pd.read_csv("Weather_Sensor_Data.csv")

power_data['DATE_TIME'] = pd.to_datetime(power_data['DATE_TIME'], format="%d/%m/%Y %H:%M")  # Ensure DATE_TIME is datetime type
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'], format="%d/%m/%Y %H:%M")  # Ensure DATE_TIME is datetime type

# Convert DATE_TIME columns to datetime objects
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'], format='%d/%m/%Y %H:%M')
power_data['DATE_TIME'] = pd.to_datetime(power_data['DATE_TIME'], format='%d/%m/%Y %H:%M')

# Group the Power Generation Data by DATE_TIME and calculate mean for DC_POWER and AC_POWER
grouped_power_data = power_data.groupby('DATE_TIME', as_index=False)[['DC_POWER', 'AC_POWER']].mean()

# Merge the grouped Power Generation Data with Weather Sensor Data
merged_data_grouped = pd.merge(grouped_power_data, weather_data, on='DATE_TIME', how='inner')

# Extract time-based features
merged_data_grouped['HOUR'] = merged_data_grouped['DATE_TIME'].dt.hour
merged_data_grouped['DAY_OF_WEEK'] = merged_data_grouped['DATE_TIME'].dt.dayofweek
merged_data_grouped['MONTH'] = merged_data_grouped['DATE_TIME'].dt.month

# Calculate rolling means and sums
window_size = 4  # Example window size
merged_data_grouped['ROLLING_DC_POWER_MEAN'] = merged_data_grouped['DC_POWER'].rolling(window=window_size, min_periods=1).mean()
merged_data_grouped['ROLLING_AC_POWER_MEAN'] = merged_data_grouped['AC_POWER'].rolling(window=window_size, min_periods=1).mean()
merged_data_grouped['ROLLING_MODULE_TEMP_MEAN'] = merged_data_grouped['MODULE_TEMPERATURE'].rolling(window=window_size, min_periods=1).mean()
merged_data_grouped['ROLLING_IRRADIATION_MEAN'] = merged_data_grouped['IRRADIATION'].rolling(window=window_size, min_periods=1).mean()

# Display the first few rows of the final dataset
print(merged_data_grouped.head())

# Function to prepare data


# Define the DC Power features
features_dc = ['MODULE_TEMPERATURE', 'IRRADIATION', 'HOUR', 'DAY_OF_WEEK', 'MONTH',
            'ROLLING_DC_POWER_MEAN', 'ROLLING_MODULE_TEMP_MEAN', 'ROLLING_IRRADIATION_MEAN']
target_dc = 'DC_POWER'

# Define the AC Power features
features_ac = ['MODULE_TEMPERATURE', 'IRRADIATION', 'HOUR', 'DAY_OF_WEEK', 'MONTH',
            'ROLLING_AC_POWER_MEAN', 'ROLLING_MODULE_TEMP_MEAN', 'ROLLING_IRRADIATION_MEAN']
target_ac = 'AC_POWER'

#%%
train_data_power = merged_data_grouped[(merged_data_grouped['DATE_TIME'] >= '2020-05-15') & (merged_data_grouped['DATE_TIME'] <= '2020-05-31')]
train_data_power.reset_index(drop=True, inplace=True)

# train_data_weather = weather_data[(weather_data['DATE_TIME'] >= '2020-05-15') & (weather_data['DATE_TIME'] <= '2020-05-31')]
# train_data_weather.reset_index(drop=True, inplace=True)

best_ac_model,best_dc_model,train_dc_predictions,test_dc_predictions = train_model(features_ac, target_ac, features_dc, target_dc, train_data_power)

# %%

# predict for the next week (1/6/2020 to 7/6/2020)
summary_df = pd.DataFrame(columns=['Start', 'End', 'Accuracy'])

test_data_power = merged_data_grouped[(merged_data_grouped['DATE_TIME'] >= '2020-06-01') & (merged_data_grouped['DATE_TIME'] <= '2020-06-07')]
test_data_power.reset_index(drop=True, inplace=True)
X_train_lstm, X_test_lstm, y_train, y_test = prepare_data(features_dc, target_dc, test_data_power)
prediction_dc = best_dc_model.predict(X_train_lstm)

X_train_lstm, X_test_lstm, y_train, y_test = prepare_data(features_ac, target_ac , test_data_power)
prediction_ac = best_ac_model.predict(X_train_lstm)

# new df to save average prediction value for each week
df = pd.DataFrame(columns=['FROM_DATE','TO_DATE','ACCURACY' ,'TYPE'])

# week 6/1/2020 to 6/7/2020 dc power
new_row = pd.DataFrame({'FROM_DATE': '2020-06-01',
                            'TO_DATE': '2020-06-07',
                            'ACCURACY': prediction_dc.mean(),
                            'TYPE': 'DC_POWER'}, index=[0])
df = pd.concat([new_row, df]).reset_index(drop = True)

# week 6/1/2020 to 6/7/2020 ac power
new_row = pd.DataFrame({'FROM_DATE': '2020-06-01',
                            'TO_DATE': '2020-06-07',
                            'ACCURACY': prediction_ac.mean(),
                            'TYPE': 'AC_POWER'}, index=[0])
df = pd.concat([new_row, df]).reset_index(drop = True)

# train the model including the predicted week
train_data_power = merged_data_grouped[(merged_data_grouped['DATE_TIME'] >= '2020-05-15') & (merged_data_grouped['DATE_TIME'] <= '2020-06-07')]
train_data_power.reset_index(drop=True, inplace=True)
best_ac_model,best_dc_model,train_dc_predictions,test_dc_predictions = train_model(features_ac, target_ac, features_ac, target_ac , train_data_power)

# predict for the next week (8/6/2020 to 14/6/2020)
test_data_power = merged_data_grouped[(merged_data_grouped['DATE_TIME'] >= '2020-06-08') & (merged_data_grouped['DATE_TIME'] <= '2020-06-14')]
test_data_power.reset_index(drop=True, inplace=True)
X_train_lstm, X_test_lstm, y_train, y_test = prepare_data(features_dc, target_dc, test_data_power)
prediction_dc = best_dc_model.predict(X_train_lstm)

X_train_lstm, X_test_lstm, y_train, y_test = prepare_data(features_ac, target_ac , test_data_power)
prediction_ac = best_ac_model.predict(X_train_lstm)

new_row = pd.DataFrame({'FROM_DATE': '2020-06-08',
                            'TO_DATE': '2020-06-14',
                            'ACCURACY': prediction_dc.mean(),
                            'TYPE': 'DC_POWER'}, index=[0])
df = pd.concat([new_row, df]).reset_index(drop = True)

new_row = pd.DataFrame({'FROM_DATE': '2020-06-08',
                            'TO_DATE': '2020-06-14',
                            'ACCURACY': prediction_ac.mean(),
                            'TYPE': 'AC_POWER'}, index=[0])
df = pd.concat([new_row, df]).reset_index(drop = True)

# train the model including the predicted week
train_data_power = merged_data_grouped[(merged_data_grouped['DATE_TIME'] >= '2020-05-15') & (merged_data_grouped['DATE_TIME'] <= '2020-06-14')]
train_data_power.reset_index(drop=True, inplace=True)
best_ac_model,best_dc_model,train_dc_predictions,test_dc_predictions = train_model(features_ac, target_ac, features_ac, target_ac , train_data_power)

# predict for the next week (15/6/2020 to 17/6/2020)
test_data_power = merged_data_grouped[(merged_data_grouped['DATE_TIME'] >= '2020-06-15') & (merged_data_grouped['DATE_TIME'] <= '2020-06-17')]
test_data_power.reset_index(drop=True, inplace=True)
X_train_lstm, X_test_lstm, y_train, y_test = prepare_data(features_dc, target_dc, test_data_power)
prediction_dc = best_dc_model.predict(X_train_lstm)

X_train_lstm, X_test_lstm, y_train, y_test = prepare_data(features_ac, target_ac , test_data_power)
prediction_ac = best_ac_model.predict(X_train_lstm)

new_row = pd.DataFrame({'FROM_DATE': '2020-06-15',
                            'TO_DATE': '2020-06-17',
                            'ACCURACY': prediction_dc.mean(),
                            'TYPE': 'DC_POWER'}, index=[0])
df = pd.concat([new_row, df]).reset_index(drop = True)

new_row = pd.DataFrame({'FROM_DATE': '2020-06-15',
                            'TO_DATE': '2020-06-17',
                            'ACCURACY': prediction_ac.mean(),
                            'TYPE': 'AC_POWER'}, index=[0])
df = pd.concat([new_row, df]).reset_index(drop = True)

df.to_csv('power_prediction.csv', index=False)

# %% accuracy testing with actual values
# mean of the actual values group by date
# Convert 'DATE_TIME' to datetime
power_data['DATE_TIME'] = pd.to_datetime(power_data['DATE_TIME'])
# Extract week from 'DATE_TIME'
power_data['WEEK'] = power_data['DATE_TIME'].dt.to_period('W')
# Group by 'WEEK' and calculate mean 'DC_POWER'
actual_dc_weekly = power_data.groupby('WEEK')['DC_POWER'].mean().reset_index()
actual_dc_weekly

# %%
# Load the predicted data
df = pd.read_csv('power_prediction.csv')

# Convert 'FROM_DATE' and 'TO_DATE' to datetime
df['FROM_DATE'] = pd.to_datetime(df['FROM_DATE'])
df['TO_DATE'] = pd.to_datetime(df['TO_DATE'])

# Extract week from 'FROM_DATE' and 'TO_DATE'
df['WEEK'] = df['FROM_DATE'].dt.to_period('W')

# Filter rows where 'TYPE' is 'DC_POWER'
df_dc = df[df['TYPE'] == 'DC_POWER']

# Merge the predicted and actual data
merged = pd.merge(df, actual_dc_weekly, on='WEEK', how='inner')

# Calculate the Mean Absolute Error (MAE)
mae = np.mean(np.abs(merged['ACCURACY'] - merged['DC_POWER']))

mae
# %%
# Group by 'WEEK' and calculate mean 'AC_POWER'
actual_ac_weekly = power_data.groupby('WEEK')['AC_POWER'].mean().reset_index()


# Filter rows where 'TYPE' is 'AC_POWER'
df = df[df['TYPE'] == 'AC_POWER']

# Merge the predicted and actual data
merged = pd.merge(df, actual_ac_weekly, on='WEEK', how='inner')

# Calculate the Mean Absolute Error (MAE)
mae = np.mean(np.abs(merged['ACCURACY'] - merged['AC_POWER']))

mae
#%% Consumption prediction
import pandas as pd
from model_2 import train_consumption_model, create_sequences

df1 = pd.read_csv("powerconsumption.csv")
df1['power consumption'] = df1[['PowerConsumption_Zone1', 'PowerConsumption_Zone2', 'PowerConsumption_Zone3']].mean(axis=1)
print(df1.head())

# Assuming your DataFrame is named df
df1['Datetime'] = pd.to_datetime(df1['Datetime'])
df1.set_index('Datetime', inplace=True)

# Optional: Create additional time features
df1['hour'] = df1.index.hour
df1['day_of_week'] = df1.index.dayofweek
# Add more as needed

# Select features and target
features1 = df1[['Temperature', 'Humidity', 'WindSpeed', 'GeneralDiffuseFlows', 'DiffuseFlows', 'hour', 'day_of_week']] # Add or remove features based on your Step 3 decisions
target1 = df1['power consumption']

# train the model 01/01/2017 to 30/11/2017
features1_train = features1[(features1.index >= '2017-01-01') & (features1.index <= '2017-11-30')]
target1_train = target1[(target1.index >= '2017-01-01') & (target1.index <= '2017-11-30')]
model,scaler = train_consumption_model(features1_train,target1_train)


# %% predict for the next week (1/12/2017 to 7/12/2017)
features1_test = features1[(features1.index >= '2017-12-01') & (features1.index <= '2017-12-07')]
target1_test = target1[(target1.index >= '2017-12-01') & (target1.index <= '2017-12-07')]

scaled_features = scaler.fit_transform(features1_test)
scaled_target = scaler.fit_transform(target1_test.values.reshape(-1,1))
X1, y1 = create_sequences(scaled_features, scaled_target, sequence_length=3)
prediction_consumption = model.predict(X1)


# %%
