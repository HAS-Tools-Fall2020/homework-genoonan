# Gillian Noonan - Homework 10

# %%
# Import necessary packages and functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import json
import urllib.request as req
import urllib


def weekly_min(month1, day_more, day_less):
    '''Function (weekly_min):
        This function pulls values out of the data_week_min dataframe which
        is aggregated by weekly minimum value.  The historical minimums are
        plotted over the data time period.  It then pulls the
        minimum historical value from the weekly minimum values
        for the given month, day time period.

        Parameters
        ----------
        month1: int
                Input variable with one value representing
                first month of the time window
        day_more: int
                Input variable with one value representing
                first day of the time window
        day_less: int
                Input variable with one value representing
                first day of the time window
        Returns
        ------
        wk_min : dataframe
                Outputs a dataframe with only data for specified time period
                and prints the output minimum flow value
        '''
    wk_min = data_week_min[(data_week_min.index.month == month1)
                           & (data_week_min.index.day >= day_more)
                           & (data_week_min.index.day <= day_less)]

    print("")
    print("Plotted historical weekly minimum flows for ", month1, "-",
          day_more, "to", month1, "-", day_less)
    wk_min.reset_index().plot(x="datetime",
                              y="flow",
                              title="Historical Flow Weekly Minimums",
                              kind="scatter")
    plt.show()

    print("The overall historical weekly minimum flow for ",
          month1, "-", day_more, "to", month1, "-", day_less,
          " is", wk_min.flow.min(), "cfs")


print("successful import")


# ////////
# Streamflow Data
# Task 1 - Set data input and develop dataframe

# %%
# Read the streamflow data into a pandas dataframe via URL
# Expand the dates to year, month, day, dayofweek.
# View format of dataframe data (print first 15 rows)

site = '09506000'
start = '1989-01-01'
end = '2020-10-31'
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + \
       site + "&referred_module=sw&period=&begin_date=" + start + \
      "&end_date=" + end
data = pd.read_table(url, skiprows=30, names=['agency_cd', 'site_no',
                                              'datetime', 'flow', 'code'],
                     parse_dates=['datetime'])

data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

print(data.head(15))

# %%
# Aggregate flow values to weekly
# View new flow_weekly dataframe format (print first 15 rows)
flow_weekly = data.resample("W", on='datetime').mean()

print(flow_weekly.head(100))


# ////////
# WEEKLY FORECAST
# ---------------------------

# Jill's Code forecast
# %%
# Look at historical minumums for one-week and two-week forecast periods
# Input dates to grab and print historical min for one-week forecast period
month = 11
day_more = 1
day_less = 7

hist_min = data[(data["month"] == month)
                & (data["day"] >= day_more) & (data["day"] <= day_less)]
print("The historical minimum flow for the week of", month, "-", day_more,
      "to", month, "-", day_less, " is",
      hist_min["flow"].min(), "cfs")

month = 11
day_more = 8
day_less = 14

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
dfi.export(df1, "Last7days-stats.png")

df2 = data_two_wks[["flow"]].describe()
print("Last two week's flow statistics")
print(df2)
dfi.export(df2, "Last14days-stats.png")

# %%
# Look at visual trend over last two weeks
# Save plot for markdown
fig, ax = plt.subplots()
ax.plot(data_two_wks.datetime, data_two_wks.flow)
ax.set(title="Two-week flow trend")
ax.set(xlabel='Date', ylabel='Daily Flow (cfs)')
plt.show()

fig.savefig('Two-week-Trend.png')

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

# LONGTERM FORECAST [Week 11-15] (historical minimums)
# ---------------------------
# %%
# Aggregate flow values to weekly MINIMUM
data_week_min = data.resample("W", on='datetime').min()
data_week_min = data_week_min.set_index("datetime")
data_week_min

# %%
# Plot historical weekly flows for each forecast week
# Use function 'weekly_min' to grab historical minimum flow
# Get overall minumum of these flows for all time
# Wk11 historical min

month1 = 11
day_more = 1
day_less = 7

weekly_min(month1, day_more, day_less)

# Wk12 historical min
month1 = 11
day_more = 8
day_less = 14

weekly_min(month1, day_more, day_less)

# Wk13 historical min
month1 = 11
day_more = 15
day_less = 21

weekly_min(month1, day_more, day_less)

# Wk14 historical min
month1 = 11
day_more = 22
day_less = 28

weekly_min(month1, day_more, day_less)

# Wk15 historical min (spans two months so does not use function)
month1 = 11
day1 = 29
month2 = 12
day2 = 5

week15_min = data_week_min[(data_week_min.index.month == month1)
                           & (data_week_min.index.day >= day1)
                           | (data_week_min.index.month == month2)
                           & (data_week_min.index.day <= day2)]

print("")
print("Plotted historical weekly minimum flows for ", month1, "-", day1,
      "to", month2, "-", day2)
week15_min.reset_index().plot(x="datetime",
                              y="flow",
                              title="Historical Flow Weekly Minimums",
                              kind="scatter")
plt.show()

print("The overall historical weekly minimum flow for ", month1, "-", day1,
      "to", month2, "-", day2, " is",
      week15_min.flow.min(), "cfs")

# Wk16 historical min
month1 = 12
day_more = 6
day_less = 12

weekly_min(month1, day_more, day_less)

# %%
