# %%
# Import the modules we will use

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import urllib.request as req
import urllib
import scipy

# %%


def weekly_min1(month1, day_more, day_less):

    '''Function (weekly_min1):
    This function is for time windows within the same month.
    It pulls values out of the data_week_min dataframe which
    is aggregated by weekly minimum value.  The historical minimums are
    plotted over the data time period.  It then pulls the
    minimum historical value from the weekly minimum values
    for the given month, day time period.  It removes 2020 data so that
    the historical forecast only uses data prior to the forecast period.

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
            last day of the time window
    Returns
    ------
    wk_min : dataframe
            Outputs a dataframe with only data for specified time period
            and prints the output minimum flow value
    '''
    wk_min = data_week_min[(data_week_min.index.month == month1)
                           & (data_week_min.index.day >= day_more)
                           & (data_week_min.index.day <= day_less)
                           & (data_week_min.index.year != 2020)]

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

    seasonal_list.append(wk_min.flow.min())


def weekly_min2(month1, day1, month2, day2):

    '''Function (weekly_min2):
    This function is for time windows spanning two months.
    It pulls values out of the data_week_min dataframe which
    is aggregated by weekly minimum value.  The historical minimums are
    plotted over the data time period.  It then pulls the
    minimum historical value from the weekly minimum values
    for the given month, day time period.  It removes 2020 data so that
    the historical forecast only uses data prior to the forecast period.

    Parameters
    ----------
    month1: int
            Input variable with one value representing
            first month of the time window
    day1: int
            Input variable with one value representing
            first day of the time window
    month2: int
            Input variable with one value representing
            second month of the time window
    day2: int
            Input variable with one value representing
            last day of the time window
    Returns
    ------
    wk_min : dataframe
            Outputs a dataframe with only data for specified time period
            and prints the output minimum flow value'''

    wk_min = data_week_min[((data_week_min.index.month == month1)
                           & (data_week_min.index.day >= day1)
                           | (data_week_min.index.month == month2)
                           & (data_week_min.index.day <= day2))
                           & (data_week_min.index.year != 2020)]

    print("")
    print("Plotted historical weekly minimum flows for ", month1, "-", day1,
          "to", month2, "-", day2)
    wk_min.reset_index().plot(x="datetime",
                              y="flow",
                              title="Historical Flow Weekly Minimums",
                              kind="scatter")
    plt.show()

    print("The overall historical weekly minimum flow for ", month1, "-", day1,
          "to", month2, "-", day2, " is",
          wk_min.flow.min(), "cfs")

    seasonal_list.append(wk_min.flow.min())


# %%
# Step 1: Import USGS flow data

# Replace parts of url with variables
site = '09506000'
start = '1989-01-01'
end = '2020-10-31'  # Update end date each week to Saturday

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
# Step 10: # Generate long term forecast based on historical minimums

# First aggregate flow values to weekly MINIMUM
data_week_min = data.resample("W-SAT", on='datetime').min()

# Reset index to be first day of week instead of last
data_week_min = data_week_min.set_index("datetime")

# %%

# Plot historical weekly flows for each forecast week
# Use function 'weekly_min' to grab historical minimum flow
# Get overall minumum of these flows for all time

# %%
# Set empty list
seasonal_list = list()

# Wk1 historical min (8/22 - 8/29)
month1 = 8
day_more = 22
day_less = 29
weekly_min1(month1, day_more, day_less)

# Wk2 historical min (8/30 - 9/5)(spans two months so does not use function)
month1 = 8
day1 = 30
month2 = 9
day2 = 5
weekly_min2(month1, day1, month2, day2)

# Wk3 historical min (9/6 - 9/12)
month1 = 9
day_more = 6
day_less = 12
weekly_min1(month1, day_more, day_less)

# Wk4 historical min (9/13 - 9/19)
month1 = 9
day_more = 13
day_less = 19
weekly_min1(month1, day_more, day_less)

# Wk5 historical min (9/20 - 9/26)
month1 = 9
day_more = 20
day_less = 26
weekly_min1(month1, day_more, day_less)

# Wk6 historical min (9/27 - 10/3) (spans two months so does not use function)
month1 = 9
day1 = 27
month2 = 10
day2 = 3
weekly_min2(month1, day1, month2, day2)

# Wk7 historical min (10/4 - 10/10)
month1 = 10
day_more = 4
day_less = 10
weekly_min1(month1, day_more, day_less)

# Wk8 historical min (10/11 - 10/17)
month1 = 10
day_more = 11
day_less = 17
weekly_min1(month1, day_more, day_less)

# Wk9 historical min (10/18 - 10/24)
month1 = 10
day_more = 18
day_less = 24
weekly_min1(month1, day_more, day_less)

# Wk10 historical min (10/25 - 10/31)
month1 = 10
day_more = 25
day_less = 31
weekly_min1(month1, day_more, day_less)

# Wk11 historical min (11/1 - 11/7)
month1 = 11
day_more = 1
day_less = 7
weekly_min1(month1, day_more, day_less)

# Wk12 historical min (11/8 - 11/14)
month1 = 11
day_more = 8
day_less = 14
weekly_min1(month1, day_more, day_less)

# Wk13 historical min (11/15 - 11/21)
month1 = 11
day_more = 15
day_less = 21
weekly_min1(month1, day_more, day_less)

# Wk14 historical min (11/22 - 11/28)
month1 = 11
day_more = 22
day_less = 28
weekly_min1(month1, day_more, day_less)

# Wk15 historical min (11/29 - 12/5)(spans two months so does not use function)
month1 = 11
day1 = 29
month2 = 12
day2 = 5
weekly_min2(month1, day1, month2, day2)

# Wk16 historical min (12/6 - 12/12)
month1 = 12
day_more = 6
day_less = 12
weekly_min1(month1, day_more, day_less)

# %%
print("Seasonal forecast list =", seasonal_list)

# %%
