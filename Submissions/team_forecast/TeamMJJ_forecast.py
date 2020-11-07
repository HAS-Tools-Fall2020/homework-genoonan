# %%
# Import the modules we will use

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import urllib.request as req
import urllib

# %%
# To-do for Jake - move function into a separate script and import to this script
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
            last day of the time window
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
flow_weekly = data.resample("W", on='datetime').mean()

# Get rid of extreme outliers (We can adjust cutoff)
flow_weekly = flow_weekly[(flow_weekly.flow <= 400)]

# %%
# Step 5: Use iloc to look for dates of training period
# Open to changes to make model more acurate
flow_weekly.iloc[1373]

# %%
# Step 6: Create lag timed series for regression model

# This loop names each column flow_tm%i and shifts it by i
for i in range(1, 4):
    flow_weekly['flow_tm%s' % i] = flow_weekly['flow'].shift(i)

# %%
# Step 7: Create regression model

# First create model training and testing datasets
# Mekha training: 1282:1373 (2017-2018)
# Jake training: 974:1205 (2010-2015)
# Could also remove flow_tm2, flow_tm3
train = flow_weekly[974:1205][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3',
                               'prcp (mm/day)', 'tmax (deg c)']]

test = flow_weekly[1205:][['flow', 'flow_tm1', 'flow_tm2', 'flow_tm3',
                           'prcp (mm/day)', 'tmax (deg c)']]

# Next create regression model based on training period above
model4 = LinearRegression()
y = train['flow'].values
x4 = train[['flow_tm1', 'flow_tm2', 'flow_tm3',
            'prcp (mm/day)', 'tmax (deg c)']]
model4.fit(x4, y)
r_sq = model4.score(x4, y)

# Print model parameters and r2
print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model4.intercept_, 2))
print('slope:', np.round(model4.coef_, 2))

# %%
# Step 8: Generate 1 wk and 2 wk preditions based on model above

# First create prediction functions
q_pred4_train = model4.predict(train[['flow_tm1', 'flow_tm2', 'flow_tm3',
                                      'prcp (mm/day)', 'tmax (deg c)']])
q_pred4_test = model4.predict(test[['flow_tm1', 'flow_tm2', 'flow_tm3',
                                    'prcp (mm/day)', 'tmax (deg c)']])

# Next predict 2 weeks into the future using 4 time lags
# Precip and tmax are manually input based on weather outlook

# NOTE: Jake could you add the tmax data? Also, could you explain
# where we manually enter precip and temp for projections?
precip = [0]
lastweekx3 = [flow_weekly.flow[-3]]
lastweekx2 = [flow_weekly.flow[-2]]
lastweek = [flow_weekly.flow[-1]]

# empty list for predictions
weeklypred_4 = []

for i in range(2):
    wk1 = lastweek[i]
    wk2 = lastweekx2[i]
    wk3 = lastweekx3[i]
    wk4 = precip[i]

    # appends to last week so that they refer to next time step
    lastweekx2.append(wk1)
    lastweekx3.append(wk2)

    # precip.appends(#) the next weeks expected rainfall mm
    precip.append(0)

    # the prediction for week # i
    prediction = model4.intercept_ + model4.coef_[0] * wk1 + model4.coef_[1] \
        * wk2 + model4.coef_[2] * wk3 + model4.coef_[3] * wk4
    lastweek.append(prediction)

    # creates a list of just my predictions for week 1 then week 2
    weeklypred_4.append(prediction)
print(weeklypred_4)

# %%
# Step 10: # Generate long term forecast based on historical minimums

# First aggregate flow values to weekly MINIMUM
data_week_min = data.resample("W-SAT", on='datetime').min()

# Reset index to be first day of week instead of last
data_week_min = data_week_min.set_index("datetime")

# Plot historical weekly flows for each forecast week
# Use function 'weekly_min' to grab historical minimum flow
# Get overall minumum of these flows for all time

# NOTE: Jill to add weeks 1-10

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