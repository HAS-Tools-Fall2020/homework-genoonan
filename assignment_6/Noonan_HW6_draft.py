#Gillian Noonan - Homework 6
# Review the starter code provided to see how to build an autoregressive(AR) model. Then build your own model, you can modify the starter model in any way for example changing the number of time steps used for prediction or changing the testing and training data periods. The only rule is that you must make some modifications to make the model your own.

# %%
# Import modules
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime

# %%
# Set file name and path
filename = 'streamflow_week6.txt'
filepath = os.path.join('data', filename)
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

#%%
# Expand the dates to year month day 
# **corrected third line to ".day"
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

#%%
# View data format - data
data.head(15)

#%%
# Aggregate flow values to weekly 
flow_weekly = data.resample("W", on='datetime').mean()

# Building the autoregressive model 
#%%
#set up arrays for lagged timeseries
flow_weekly['flow_tm1'] = flow_weekly['flow'].shift(1)
flow_weekly['flow_tm2'] = flow_weekly['flow'].shift(2)

#%%
# View flow_weekly format
# 1658 rows x 8 columns
flow_weekly

#%%
#TEST 1
# set training and test data sets for one-week forecast - 10/4 to 10/10
# train period is September data only for 2017 - 2019
# using last 10 weeks for test data
month1 = 9
year_trainmin = 2017
year_trainmax = 2019
train = flow_weekly[(flow_weekly["month"]==month1) & (flow_weekly["year"] >=year_trainmin)&(flow_weekly["year"] <=year_trainmax)][['month','flow', 'flow_tm1', 'flow_tm2']]
test = flow_weekly[1648:][['flow', 'flow_tm1', 'flow_tm2']]
print ("good luck!")

#%%
# view train period data
train

#%%
# view test period data
test

#%%
# Fit a linear regression model using sklearn
model = LinearRegression()
x=train['flow_tm1'].values.reshape(-1,1) 
y=train['flow'].values
model.fit(x,y)

#%%
# r^2 values
r_sq = model.score(x, y)
print('coefficient of determination:', np.round(r_sq,2))

#%%
#print the intercept and the slope 
print('intercept:', np.round(model.intercept_, 2))
print('slope:', np.round(model.coef_, 2))

#%%
plt.style.use('ggplot')
plt.rc('xtick', labelsize=8) 
plt.rc('ytick', labelsize=8) 
fig, ax = plt.subplots()
ax.plot(train['flow'], '--k', label='train', linewidth=3)
ax.plot(test['flow'], '-r', label='test')
ax.set(title="One-Week Prediction Training Test 1", xlabel="Date", 
        ylabel="Weekly Avg Flow [cfs]", xlim=[datetime.date(2017, 1, 1), datetime.date(2021, 1, 1)])
ax.legend(loc = 'upper right', frameon=True, fancybox=True, shadow=True, ncol=2)
fig.savefig('One-week(Test1).png')

#%%
# Step 4 Make a prediction with your model 
# Predict the model response for a  given flow value
q_pred_train = model.predict(train['flow_tm1'].values.reshape(-1,1))
q_pred_test = model.predict(test['flow_tm1'].values.reshape(-1,1))
print(q_pred_test)

#%%
# you could also predict the q for just a single value like this
last_week_flow = 56
prediction = model.intercept_ + model.coef_ * last_week_flow
print(prediction)
        
#%%
# 3. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], '-k', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, ':r', linewidth=3, 
        label='simulated')
ax.set(title="Observed Flow vs. Simulated Flow", xlabel="Model Duration Period", ylabel="Weekly Avg Flow [cfs]")
ax.legend(frameon=True, fancybox=True, shadow=True)

fig.savefig('One-week(Test1)_Predict-vs-observed.png')

# 5. Scatter plot of t vs t-1 flow with normal axes
#%%
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='o',
              color='mediumvioletred', label='observations')
ax.set(xlabel='flow t-1', ylabel='flow t', title="AR Model Fit")
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model', linewidth=3, color = 'black')
ax.text(50, 175, "x(t) = 0.7 * x(t-1) + 31.95", fontsize=10)
ax.text(50, 155, "r^2 = 0.76", fontsize=10)
ax.legend(frameon=True, fancybox=True, shadow=True)
fig.savefig('One-week(Test1)_(t-vs-(t-1)).png')





# %%
#WEEKLY FORECAST WEEK 6
#import dataframe_image to export tables to png
import dataframe_image as dfi
#%%
data

# 1week forecast - look at last 7 days
# %%
data_weekly = data.tail(7)
data_weekly

#%%
# look at prior week stats
df = data_weekly[["flow"]].describe()
print(df)
dfi.export(df, "Last7days-stats.png")

# %%
# look at trend over last two weeks
data_two_wks = data.tail(14)
fig, ax = plt.subplots()

ax.plot(data_two_wks.datetime, data_two_wks.flow)
ax.set(title="Two-week flow trend")
ax.set(xlabel='Date', ylabel='Daily Flow (cfs)')
plt.rc('xtick', labelsize=7)
plt.show()
fig.savefig('Two-week-Trend_(Old-Code).png')

#%%
# 2week forecast - Oct11-17 min
month = 10
day_more = 11
day_less = 17

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk6 historical min
month1 = 9
day1 = 27
month2 = 10
day2 = 3
data_seasonal_6 = data[((data["month"]==month1) & (data["day"] >=day1)) | ((data["month"] ==month2) & (data["day"] <=day2))]
data_seasonal_6["flow"].min()

# %%
#seasonal wk7 historical min
month = 10
day_more = 4
day_less = 10

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk8 historical min
month = 10
day_more = 11
day_less = 17

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk9 historical min
month = 10
day_more = 18
day_less = 24

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk10 historical min
month = 10
day_more = 25
day_less = 31

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk11 historical min
month = 11
day_more = 1
day_less = 7

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk12 historical min
month = 11
day_more = 8
day_less = 14

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk13 historical min
month = 11
day_more = 15
day_less = 21

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk14 historical min
month = 11
day_more = 22
day_less = 28

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
#seasonal wk15 historical min
month1 = 11
day1 = 29
month2 = 12
day2 = 5
data_seasonal_6 = data[((data["month"]==month1) & (data["day"] >=day1)) | ((data["month"] ==month2) & (data["day"] <=day2))]
data_seasonal_6["flow"].min()

# %%
#seasonal wk15 historical min
month = 12
day_more = 6
day_less = 12

data_two_week = data[(data["month"]==month) & (data["day"] >=day_more) & (data["day"] <=day_less)]
data_two_week["flow"].min()

# %%
