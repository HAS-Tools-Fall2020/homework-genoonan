# Modified starter code from Laura

# %%
# Step 1: Import modules used in this script
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import json 
import urllib.request as req
import urllib
import dataretrieval.nwis as nwis

# %%
# Step 2: Read in USGS streamflow data and create dataframe of avg weekly flow
# Used nwis.get_record function instead of saving a local file

# Change stop_date each week
station_id = "09506000"
USGS_start = "1989-01-01"
USGS_stop = "2020-10-31"

data_flow = nwis.get_record(sites=station_id, service='dv',
                          start=USGS_start, end=USGS_stop,
                          parameterCd='00060')

# Rename columns
data_flow.columns = ['flow', 'code', 'site_no']

# Make index a recognized datetime format instead of string
data_flow.index = data_flow.index.strftime('%Y-%m-%d')

data_flow['datetime'] = pd.to_datetime(data_flow.index)
data_flow['year'] = pd.DatetimeIndex(data_flow['datetime']).year
data_flow['month'] = pd.DatetimeIndex(data_flow['datetime']).month
data_flow['day'] = pd.DatetimeIndex(data_flow['datetime']).day
data_flow['dayofweek'] = pd.DatetimeIndex(data_flow['datetime']).dayofweek

# Aggregate flow values to weekly
flow_weekly = data_flow.resample("W-SAT", on='datetime').mean()

# %%
# Step 3: Read in daymet precip data

# Read daymet precip data in as a json file

url = "https://daymet.ornl.gov/single-pixel/api/data?lat=34.4483&lon=-111.7892"  \
       "&vars=prcp&start=1989-01-01&end=2019-12-31&format=json"
response = req.urlopen(url)
# Look at the keys and use this to grab out the data
responseDict = json.loads(response.read())
responseDict['data'].keys()
year = responseDict['data']['year']
yearday = responseDict['data']['yday']
precip = responseDict['data']['prcp (mm/day)']

# Make a dataframe from the data
data_precip = pd.DataFrame({'year': year,
                     'yearday': yearday, "precip": precip})

data_precip['datetime'] = pd.to_datetime(data_precip['year'] * 1000 + data_precip['yearday'], format='%Y%j')

# Aggregate precip values to weekly
precip_weekly = data_precip.resample("W-SAT", on='datetime').mean()

# %%
# Step 4: Read in daymet max temperature data

# Read daymet tmax data in as a json file

url = "https://daymet.ornl.gov/single-pixel/api/data?lat=34.4483&lon=-111.7892"  \
       "&vars=tmax&start=1989-01-01&end=2019-12-31&format=json"
response = req.urlopen(url)
# Look at the keys and use this to grab out the data
responseDict = json.loads(response.read())
responseDict['data'].keys()
year = responseDict['data']['year']
yearday = responseDict['data']['yday']
tmax = responseDict['data']['tmax (deg c)']

# Make a dataframe from the data
data_temp = pd.DataFrame({'year': year,
                     'yearday': yearday, "maxtemp": tmax})

data_temp['datetime'] = pd.to_datetime(data_temp['year'] * 1000 + data_temp['yearday'], format='%Y%j')

# Aggregate precip values to weekly
temp_weekly = data_temp.resample("W-SAT", on='datetime').mean()

# %%
# Step 5: Combine datasets into one dataframe
data = flow_weekly.copy()
data['precip'] = precip_weekly['precip']
data['maxtemp'] = temp_weekly['maxtemp']

# %%
# Step 6: Setup the arrays used to build regrssion model
# This model uses a single 1 week time lag of flow, precip, and max temp

data['flow_tm1'] = data['flow'].shift(1)

# %%
# Step 7 - Pick what portion of the time series to use as training data
# For this model, training = 2017-2018, testing = 2019-2020
# LC - you could define these numbers as variables based on dates. 
train = data[1461:1566][['flow', 'flow_tm1', 'precip', 'maxtemp']]
test = data[1566:][['flow', 'flow_tm1', 'precip', 'maxtemp']]

# %%
# Step 8: Fit linear regression model
model = LinearRegression()
x3 = train[['flow_tm1', 'precip', 'maxtemp']]
y = train['flow'].values
model.fit(x3, y)
r_sq = np.round(model.score(x3, y), 2)

print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

# %%
# Step 9: Generate plots to visualize regression model and datasets
# This step is optional, not neccessary to generate the forecasts.

# Set plot style and sublot layout
plt.style.use('classic')
fig, ax = plt.subplots(2, 2, figsize=(10, 8))
ax = ax.flatten()
fig.tight_layout()
plt.subplots_adjust(hspace=0.5, wspace=0.2)

# PLOT 1: Timeseries of observed flow, highlight training and testing periods
ax[0].plot(train['flow'], 'orange', label='training period', linewidth=6)
ax[0].plot(test['flow'], 'greenyellow', label='testing period', linewidth=6)
ax[0].plot(data['flow'], 'b', label='observed flow', linewidth=1)
ax[0].set(title="Observed Flow for Model Build (2017-2020)",
          xlabel="Date", ylabel="Weekly Avg Flow [cfs]", yscale='log',
          xlim=['2017-01-01', '2020-11-01'])
ax[0].legend(fontsize=8)
plt.setp(ax[0].get_xticklabels(), rotation=45)

# PLOT 2: Lagged Flows (Predictive Variables)
ax[1].plot(data['flow'], 'navy', label='observed flow')
ax[1].plot(data['flow_tm1'], 'forestgreen', label='1 week time lag')
ax[1].set(title="Time Lagged Flows for Training Period", xlabel="Date",
          ylabel="Weekly Avg Flow [cfs]", yscale='log',
          xlim=['2017-01-01', '2019-01-01'])
ax[1].legend(fontsize=8)
plt.setp(ax[1].get_xticklabels(), rotation=45)

# PLOT 3: Weekly Average precip
ax[2].plot(data['precip'], color='cornflowerblue', linewidth=2,
           label='observed precip')
ax[2].set(title="Observed Weekly Avg Precip", xlabel="Date",
          ylabel="Weekly Avg Precip [mm]", ylim=[0,12],
          xlim=['2017-01-01', '2019-12-31'])
ax[2].legend(fontsize=8)
plt.setp(ax[2].get_xticklabels(), rotation=45)

# PLOT 3: Weekly Average max temp
ax[3].plot(data['maxtemp'], color='r', linewidth=2,
           label='observed max temp')
ax[3].set(title="Observed Weekly Avg Max Temp", xlabel="Date",
          ylabel="Weekly Avg Max Temp [C]",
          xlim=['2017-01-01', '2019-12-31'])
ax[3].legend(fontsize=8)
plt.setp(ax[3].get_xticklabels(), rotation=45)

plt.show()

# Save Figure
fig.savefig("Regression_Model_Data", bbox_inches='tight')

# %%
# Step 10: WORK IN PROGRESS
# Need to make prediction with regression model, but the daymet data
# only goes through the end of 2019. For next week, I will instead try
# importing data from another source like mesonet that has current data

# %%
# Step 11: Make predictions for forecast entries outside of model

# Timeseries of observed flow values shows past 8 weeks have seen increasing trend
fig, ax = plt.subplots()
ax.plot(data['flow'].iloc[-8:],'b', label='observed flow', linewidth = 1, marker='o')
ax.set(title="Observed Flow for Forecast Period", xlabel="Date", 
       ylabel="Weekly Avg Flow [cfs]", ylim=[40,120])
ax.legend()
plt.show()

# Time series shows we have seen about an 8 cfs per week increase over past 6 weeks
# Based predictions recent trend
myprediction_1wk = data['flow'].iloc[-1:].values[0].round(0) + 8
myprediction_2wk = myprediction_1wk + 8

# Submit these values as forecast entries
print("My prediction for 1 week forecast: ", myprediction_1wk, 'cfs')
print("My prediction for 2 week forecast: ", myprediction_2wk, 'cfs')

# %%
# Step 12: Make predictions for 16 week forecast
# Predictions will be based on weekly flow in 2019, which was a low flow year
# For this year, I will assume max weekly flow of 200 cfs

flow_2019 = data["2019-08-31":"2019-12-14"]

lt_forecast = np.zeros(16)
for i in range(0, 16):
    if flow_2019['flow'].iloc[i] <= 200:
        lt_forecast[i] = flow_2019['flow'].iloc[i].round(0)
        print('lt_week', i+1, ' = ', flow_2019['flow'].iloc[i].round(0))
    else:
        lt_forecast[i] = 200
        print('lt_week', i+1, ' = 200 cfs')
# %%
