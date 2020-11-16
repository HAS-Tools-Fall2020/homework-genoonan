# Gillian Noonan HW12 - Reanalysis NetCDF

# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Noonan_func as nf
import xarray as xr

print("successful import")

# %%
# STEP 1: Import USGS flow data
# Expand the dates to year month day

# Replace parts of url with variables
site = '09506000'
start = '1989-01-01'
end = '2020-11-12'  # Update end date each week to Saturday

url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + \
    site + "&referred_module=sw&period=&begin_date=" + start + "&end_date=" + \
    end
data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                              'datetime', 'flow', 'code'],
                     parse_dates=['datetime'])

data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek
data.set_index('datetime')
data

# %%
# STEP 2: Read in NetCDF - air temp
# historical temp (1989-present) 'NCEP Reanalysis Daily Averages - Temp'
# pull out "air" data
data_path = os.path.join('data',
                         'NCEP Reanalysis Daily Averages - Temp',
                         'X73.24.236.124.319.15.0.37.nc')
dataset1 = xr.open_dataset(data_path)
airtemp = dataset1['air']

lat = dataset1["air"]["lat"].values[0]
lon = dataset1["air"]["lon"].values[0]
print("Long, Lat values:", lon, lat)

air_pt = dataset1["air"].sel(lat=lat, lon=lon)
air_pt.plot.line()

# %%
# Convert to pandas dataframe
air_df = air_pt.to_dataframe()
air_df

# %%
# convert to Fahrenheit and add column
# (K − 273.15) × 9/5 + 32 = °F)
air_df["air-F"] = ((air_df["air"] - 273) * 1.8 + 32)
air_df

# %%
# STEP 3: Read in NetCDF - precip
# historical precip (1989-present) 'CPC Global Precipitation'
# pull out "precip" data
data_path = os.path.join('data',
                         'CPC Global Precipitation',
                         'X73.24.236.124.319.15.45.4.nc')
dataset2 = xr.open_dataset(data_path)
precip = dataset2['precip']

lat = dataset2["precip"]["lat"].values[0]
lon = dataset2["precip"]["lon"].values[0]
print("Long, Lat values:", lon, lat)

precip_pt = dataset2["precip"].sel(lat=lat, lon=lon)
precip_pt.plot.line()

# %%
# Convert to pandas dataframe
precip_df = precip_pt.to_dataframe()
precip_df

# %%
# Join airtemp data to existing dataframe
# WHY DO THESE COME IN AS NaN VALUES?
# alldata = data.join(air_df['air'])
# alldata2 = alldata.join(precip_df['precip'])
# alldata2

# %%
# Grab last two weeks - streamflow
two_wk_flow = data.tail(14)
print(two_wk_flow)

# %%
# Grab last two weeks - air
two_wk_air = air_df.tail(14)
print(two_wk_air)

# %%
# Grab last two weeks - precip
two_wk_precip = precip_df.tail(14)
print(two_wk_precip)

# %%
# Time Series of Flow and Air Temp
fig, ax1 = plt.subplots()
color = 'fuchsia'
ax1.set_xlabel('Datetime')
ax1.set_ylabel('Flow (cfs)', color=color)
ax1.set(title="Two-week Flow and Air Temp")
ax1.plot(data["datetime"].tail(14), data["flow"].tail(14),
         color=color)
ax1.tick_params(axis='y', labelcolor=color, labelsize=10)
ax1.tick_params(axis='x', labelcolor="black", labelsize=8, rotation=45)

ax2 = ax1.twinx()
color = 'darkgreen'
ax2.set_ylabel('Air temp (F))', color=color)
ax2.plot(two_wk_air.index, two_wk_air["air-F"],
         color=color)
ax2.tick_params(axis='y', labelcolor=color, labelsize=10)

plt.show()
fig.savefig("Flow_and_AirTemp.png")

# %%
# Time Series of Flow and Precip
fig, ax1 = plt.subplots()
color = 'fuchsia'
ax1.set_xlabel('Datetime')
ax1.set_ylabel('Flow (cfs)', color=color)
ax1.set(title="Two-week Flow and Precip")
ax1.plot(data["datetime"].tail(14), data["flow"].tail(14),
         color=color)
ax1.tick_params(axis='y', labelcolor=color, labelsize=10)
ax1.tick_params(axis='x', labelcolor="black", labelsize=8, rotation=45)

ax2 = ax1.twinx()
color = 'darkblue'
ax2.set_ylabel('Precip (mm/day)', color=color)
ax2.bar(two_wk_precip.index, two_wk_precip["precip"],
        color=color)
ax2.tick_params(axis='y', labelcolor=color, labelsize=10)

plt.show()
fig.savefig("Flow_and_Precip.png")

# //////////////////////////////
# WEEKLY FORECAST
# ---------------------------

# Jill's Code forecast
# %%
# Look at historical minumums for one-week and two-week forecast periods
# Input dates to grab and print historical min for one-week forecast period
month = 11
day_more = 8
day_less = 14

hist_min = data[(data["month"] == month)
                & (data["day"] >= day_more) & (data["day"] <= day_less)]
print("The historical minimum flow for the week of", month, "-", day_more,
      "to", month, "-", day_less, " is",
      hist_min["flow"].min(), "cfs")

month = 11
day_more = 15
day_less = 21

hist_min = data[(data["month"] == month)
                & (data["day"] >= day_more) & (data["day"] <= day_less)]
print("The historical minimum flow for the week of", month, "-", day_more,
      "to", month, "-", day_less, " is",
      hist_min["flow"].min(), "cfs")

# %%
# # Look at tables of statistics for last 7 and 14 days
# Save tables of statistics as PNG files for markdown
data_weekly = data.tail(7)
data_two_wks = data.tail(14)

df1 = data_weekly[["flow"]].describe()
print("Last week's flow statistics")
print(df1)
df2 = data_two_wks[["flow"]].describe()
print("Last two week's flow statistics")
print(df2)

# %%
# Get one-week and two-week mean values
mean_1wk = round(np.mean(data_weekly)["flow"], 2)
print("The mean flow for the last 7 days is:", mean_1wk)

mean_2wk = round(np.mean(data_two_wks)["flow"], 2)
print("The mean flow for the last 14 days is:", mean_2wk)

# %%
# Get beginning and end flow values for one-week and two-week periods
print("One-week Beginning and End Flow Values")
first_val1 = data_weekly.flow.iloc[0]
last_val1 = data_weekly.flow.iloc[-1]
print(first_val1)
print(last_val1)

print("Two-week Beginning and End Flow Values")
first_val2 = data_two_wks.flow.iloc[0]
last_val2 = data_two_wks.flow.iloc[-1]
print(first_val2)
print(last_val2)

# %%
# Overall flow flucuation for last 7 and 14 days
# Calculate flucuation from start to end of last 7 days
perc_chng_total_1wk = ((last_val1 - first_val1)/first_val1)*100
print("Overall flow fluctuation in past 7 days was",
      round(perc_chng_total_1wk, 2), "percent.")

# Calculate flucuation from start to end of last 14 days
perc_chng_total_2wk = ((last_val2 - first_val2)/first_val2)*100
print("Overall flow fluctuation in past 14 days was",
      round(perc_chng_total_2wk, 2), "percent.")

# %%
# Trend-based prediction for one-week and two-week/
# forecast values (Jill's Code)
# Based on percent change total from above code block.  If trend is upward,
# forecast a percentage higher, if trend is downward, forecast a
# percentage lower
if perc_chng_total_1wk > 0:
    Jill_1wk = mean_1wk + (mean_1wk * (perc_chng_total_1wk/100))
    print("The one-week flow prediction using Jill's code"
          " [JILL-1WK] is", round(Jill_1wk, 1), "cfs")
else:
    Jill_1wk = mean_1wk - (mean_1wk * (perc_chng_total_1wk/100))
    print("The one-week flow prediction using Jill's code"
          " [JILL-1WK] is", round(Jill_1wk, 1), "cfs")

if perc_chng_total_2wk > 0:
    Jill_2wk = mean_2wk + (mean_2wk * (perc_chng_total_2wk/100))
    print("The two-week flow prediction using Jill's code"
          " [JILL-2WK] is", round(Jill_2wk, 1), "cfs")
else:
    Jill_2wk = mean_2wk - (mean_2wk * (perc_chng_total_2wk/100))
    print("The two-week flow prediction using Jill's code"
          " [JILL-2WK] is", round(Jill_2wk, 1), "cfs")

# ///////////////////////////////////////////////
# LONG-TERM FORECAST
# %%
# Step 12: Create dataset to generate long term forecast
# based on historical minimums

# First aggregate flow values to weekly MINIMUM
data_week_min = data.resample("W-SAT", on='datetime').min()

# Reset index to be first day of week instead of last day
data_week_min = data_week_min.set_index("datetime")

# Plot historical weekly flows for each forecast week
# Use functions 'weekly_min1' or 'weekly_min2' to grab historical minimum flow

# Set empty list
seasonal_list = list()

# Wk1 historical min (8/22 - 8/29)
month1 = 8
day_more = 22
day_less = 29
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk2 historical min (8/30 - 9/5)
month1 = 8
day1 = 30
month2 = 9
day2 = 5
nf.weekly_min2(data_week_min, month1, day1, month2, day2, seasonal_list)

# Wk3 historical min (9/6 - 9/12)
month1 = 9
day_more = 6
day_less = 12
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk4 historical min (9/13 - 9/19)
month1 = 9
day_more = 13
day_less = 19
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk5 historical min (9/20 - 9/26)
month1 = 9
day_more = 20
day_less = 26
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk6 historical min (9/27 - 10/3)
month1 = 9
day1 = 27
month2 = 10
day2 = 3
nf.weekly_min2(data_week_min, month1, day1, month2, day2, seasonal_list)

# Wk7 historical min (10/4 - 10/10)
month1 = 10
day_more = 4
day_less = 10
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk8 historical min (10/11 - 10/17)
month1 = 10
day_more = 11
day_less = 17
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk9 historical min (10/18 - 10/24)
month1 = 10
day_more = 18
day_less = 24
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk10 historical min (10/25 - 10/31)
month1 = 10
day_more = 25
day_less = 31
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk11 historical min (11/1 - 11/7)
month1 = 11
day_more = 1
day_less = 7
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk12 historical min (11/8 - 11/14)
month1 = 11
day_more = 8
day_less = 14
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk13 historical min (11/15 - 11/21)
month1 = 11
day_more = 15
day_less = 21
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk14 historical min (11/22 - 11/28)
month1 = 11
day_more = 22
day_less = 28
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Wk15 historical min (11/29 - 12/5)
month1 = 11
day1 = 29
month2 = 12
day2 = 5
nf.weekly_min2(data_week_min, month1, day1, month2, day2, seasonal_list)

# Wk16 historical min (12/6 - 12/12)
month1 = 12
day_more = 6
day_less = 12
nf.weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list)

# Print 16 week forecast values
print("Seasonal forecast list =", seasonal_list)

# %%
