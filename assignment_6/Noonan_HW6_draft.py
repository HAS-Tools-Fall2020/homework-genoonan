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
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).dayofweek
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

#%%
# View data format - data
data.head(3)

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
flow_weekly

#%%
#TEST 1
# set training and test data sets for one-week forecast - 10/4 to 10/10
# train period is September data for 2015 - 2019
#test period is September 2020
# grabbing these dates historically 
month1 = 9
year_trainmin = 2017
year_trainmax = 2019
year_test1 = 2020
train = flow_weekly[(flow_weekly["month"]==month1) & (flow_weekly["year"] >=year_trainmin)&(flow_weekly["year"] <=year_trainmax)][['month','flow', 'flow_tm1', 'flow_tm2']]
test = flow_weekly[(flow_weekly["month"]==month1) & (flow_weekly["year"] == 2020)][['month', 'flow', 'flow_tm1', 'flow_tm2']]

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

#%%
# you could also predict the q for just a single value like this
last_week_flow = 56
prediction = model.intercept_ + model.coef_ * last_week_flow
print(prediction)

# #%%
# for i in range(len(flow_weekly)):
#         if "month" == 9:
#                 print(flow_weekly['flow'].min())
        
#%%
# 3. Line  plot comparison of predicted and observed flows
fig, ax = plt.subplots()
ax.plot(train['flow'], '-k', linewidth=2, label='observed')
ax.plot(train.index, q_pred_train, ':r', linewidth=3, 
        label='simulated')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log')
ax.legend()
plt.rc('xtick', labelsize=4) 
fig.savefig('One-week(Test1)_Predict-vs-observed.png')

# 5. Scatter plot of t vs t-1 flow with normal axes
#%%
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='p',
              color='blueviolet', label='observations')
ax.set(xlabel='flow t-1', ylabel='flow t')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred_train), label='AR model')
ax.legend()
fig.savefig('One-week(Test1)_(t-vs-(t-1)).png')

# For your written assignment provide the following. Your submission should include at least 3 different types of plots (see the note at the end of the previous section for how to add these into your markdown file if you are not sure how to do that):

# A summary of the AR model that you ended up building, including (1) what you are using as your prediction variables, (2) the final equation for your model and (3) what you used as your testing and training periods. In your discussion please include graphical outputs that support why you made the decisions you did with your model.

# Provide an analysis of your final model performance. This should include at least one graph that shows the historical vs predicted streamflow and some discussion of qualitatively how you think your model is good or bad.

# Finally, provide discussion on what you actually used for your forecast. Did you use your AR model, why or why not? If not how did you generate your forecast this week?

# %%
