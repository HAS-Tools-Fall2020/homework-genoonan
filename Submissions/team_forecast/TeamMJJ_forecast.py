# %%
# Import the modules we will use

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import mjj_func as mf
import urllib

# %%
# Step 1: Import USGS flow data

# Replace parts of url with variables
site = '09506000'
start = '1989-01-01'
end = '2020-11-07'  # Update end date each week to Saturday

url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + \
    site + "&referred_module=sw&period=&begin_date=" + start + "&end_date=" + \
    end
data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                              'datetime', 'flow', 'code'],
                     parse_dates=['datetime'])

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# %%
# Step 2: Import Daymet precip data as csv and join to flow data frame

base_url = "https://daymet.ornl.gov/single-pixel/api/data"

args1 = {
    'lat': '34.4483',
    'lon': '-111.7892',
    'vars': 'prcp',
    'start': '1989-01-01',
    'end': '2019-12-31',
    }
apiString1 = urllib.parse.urlencode(args1)

fullUrl1 = base_url + '?' + apiString1 + "&format=csv"

precip_data = pd.read_table(fullUrl1, delimiter=',', skiprows=6)

# Join precip data to existing dataframe
data = data.join(precip_data['prcp (mm/day)'])

# %%
# Step 3: Import Daymet max temp data as csv and join to flow data frame

args2 = {
    'lat': '34.4483',
    'lon': '-111.7892',
    'vars': 'tmax',
    'start': '1989-01-01',
    'end': '2019-12-31',
    }
apiString2 = urllib.parse.urlencode(args2)

fullUrl2 = base_url + '?' + apiString2 + "&format=csv"

tmax_data = pd.read_table(fullUrl2, delimiter=',', skiprows=6)

# Join precip data to existing dataframe
data = data.join(tmax_data['tmax (deg c)'])

# %%
# Step 4: Create weekly dataset for model

# Weekly resample
flow_weekly = data.resample("W-SAT", on='datetime').mean()

# Get rid of extreme outliers (We can adjust cutoff)
flow_weekly = flow_weekly[(flow_weekly.flow <= 345)]

# %%
# Step 5: Use iloc to look for dates of training period
# Open to changes to make model more acurate
flow_weekly.iloc[1373]

# %%
# Step 6: Create lag timed series for regression model

# This loop names each column flow_tm%i and shifts it by i
for i in range(1, 4):
    flow_weekly['flow_tm%s' % i] = flow_weekly['flow'].shift(i)
# done for temp as well
for i in range(1, 3):
    flow_weekly['tmax (deg c)%s' % i] = flow_weekly['tmax (deg c)'].shift(i)

# %%
# Step 7: Create regression model

# First create model training and testing datasets
# Mekha training: 1282:1373 (2017-2018)
# Jake training: 974:1205 (2010-2015)
# Could also remove flow_tm2, flow_tm3
train = flow_weekly[974:1353][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3',
                               'prcp (mm/day)', 'tmax (deg c)',
                               'tmax (deg c)1']]

# Next create regression model based on training period above
model4 = LinearRegression()
y = train['flow'].values
y = train['flow'].values
x4 = train[['flow_tm1', 'flow_tm2', 'flow_tm3',
            'prcp (mm/day)', 'tmax (deg c)', 'tmax (deg c)1']]
model4.fit(x4, y)
r_sq = model4.score(x4, y)

# Print model parameters and r2
print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model4.intercept_, 2))
print('slope:', np.round(model4.coef_, 2))

# %%
# Step 8: Generate 1 wk and 2 wk preditions based on model above
# creates list of monthly precipt 5th percentile
monthly_precip = []
for i in range(8, 13):
    monthly_precip.append(data['prcp (mm/day)']
                          [(data['prcp (mm/day)'] > 0) &
                          (data.year > 2010) &
                          (data.month == i)].quantile(0.05))
    monthly_precip[i-8] = np.round(monthly_precip[i-8], decimals=1)
    # print('month#%s 5 percent precipt is (mm) '%i
    #       +str(np.round(monthly_precip[i-8], decimals=1)))

# creates a list of 90th percentile temperatures (because its been hot)
weeklytemp = []
for i in range(8, 13):
    weeklytemp.append(data['tmax (deg c)'][(data.year > 2010) &
                                           (data.month == i)
                                           & (data.day <= 7)].quantile(0.9))
    weeklytemp.append(data['tmax (deg c)'][(data.year > 2010) &
                                           (data.month == i) & (data.day > 7) &
                                           (data.day <= 14)].quantile(0.9))
    weeklytemp.append(data['tmax (deg c)'][(data.year > 2010) &
                                           (data.month == i) & (data.day > 14)
                                           & (data.day <= 21)].quantile(0.9))
    weeklytemp.append(data['tmax (deg c)'][(data.year > 2010) &
                                           (data.month == i)
                                           & (data.day >= 22)].quantile(0.9))
# trimming to match weeks of the semester
weeklytemp = weeklytemp[3:19]
# copied then temp 1 week prior to semester start
# is inserted at begining of list
weeklytemp2 = weeklytemp.copy()
weeklytemp2[0:0] = [41.2]
# rounding
weeklytemp = np.round(weeklytemp, decimals=2)
weeklytemp2 = np.round(weeklytemp, decimals=2)

# %%
# variables block
# the week number of the semester
wk_num = 11
# initial precipt value
precip = [0.762]
# flow for the last 3 weeks prior to semester start
lastweek = [flow_weekly.flow[-(1 + wk_num)]]
lastweekx2 = [flow_weekly.flow[-(2 + wk_num)]]
lastweekx3 = [flow_weekly.flow[-(3 + wk_num)]]
# empty list where predictions are input
weeklypred = []

mf.pred_sem(wk_num, lastweek, lastweekx2, lastweekx3,
            precip, weeklytemp, weeklytemp2, monthly_precip,
            model4.intercept_, model4.coef_, weeklypred, flow_weekly)

# %%
# variable block
wk = 2
# precip (mm) projection next 2 weeks [P1, P2]
precip = [1.8, 0]
lastweek = [flow_weekly.flow[-1]]
lastweekx2 = [flow_weekly.flow[-2]]
lastweekx3 = [flow_weekly.flow[-3]]
# temp next 2 weeks [T1,T2]
temp = [19.83, 22.28]
# temp this week
temp2 = [29.44]
weeklypred = []

# This function is similar but does not graph
# and depends on forecasted inputs of precipitation and temperature
mf.prediction(wk, lastweek, lastweekx2, lastweekx3,
              precip, temp, temp2, model4.intercept_, model4.coef_, weeklypred)

# %%
# Step 10: # Generate long term forecast based on historical minimums

# First aggregate flow values to weekly MINIMUM
data_week_min = data.resample("W-SAT", on='datetime').min()

# Reset index to be first day of week instead of last
data_week_min = data_week_min.set_index("datetime")

# %%

# Plot historical weekly flows for each forecast week
# Use functions 'weekly_min1' or 'weekly_min2' to grab historical minimum flow

# %%
# Set empty list
seasonal_list = list()

# Wk1 historical min (8/22 - 8/29)
month1 = 8
day_more = 22
day_less = 29
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk2 historical min (8/30 - 9/5)
month1 = 8
day1 = 30
month2 = 9
day2 = 5
mf.weekly_min2(data_week_min, month1, day1, month2, day2, seasonal_list)

# Wk3 historical min (9/6 - 9/12)
month1 = 9
day_more = 6
day_less = 12
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk4 historical min (9/13 - 9/19)
month1 = 9
day_more = 13
day_less = 19
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk5 historical min (9/20 - 9/26)
month1 = 9
day_more = 20
day_less = 26
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk6 historical min (9/27 - 10/3)
month1 = 9
day1 = 27
month2 = 10
day2 = 3
mf.weekly_min2(data_week_min, month1, day1, month2, day2, seasonal_list)

# Wk7 historical min (10/4 - 10/10)
month1 = 10
day_more = 4
day_less = 10
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk8 historical min (10/11 - 10/17)
month1 = 10
day_more = 11
day_less = 17
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk9 historical min (10/18 - 10/24)
month1 = 10
day_more = 18
day_less = 24
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk10 historical min (10/25 - 10/31)
month1 = 10
day_more = 25
day_less = 31
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk11 historical min (11/1 - 11/7)
month1 = 11
day_more = 1
day_less = 7
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk12 historical min (11/8 - 11/14)
month1 = 11
day_more = 8
day_less = 14
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk13 historical min (11/15 - 11/21)
month1 = 11
day_more = 15
day_less = 21
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk14 historical min (11/22 - 11/28)
month1 = 11
day_more = 22
day_less = 28
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk15 historical min (11/29 - 12/5)
month1 = 11
day1 = 29
month2 = 12
day2 = 5
mf.weekly_min2(data_week_min, month1, day1, month2, day2, seasonal_list)

# Wk16 historical min (12/6 - 12/12)
month1 = 12
day_more = 6
day_less = 12
mf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# %%
print("Seasonal forecast list =", seasonal_list)

# %%
