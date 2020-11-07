# %%
# Import the modules we will use

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
# use conda install -c anaconda scipy
from scipy.stats import bernoulli

# %%                     )
# Replace parts of my url with variables
site = '09506000'
start = '1989-01-01'
end = '2020-10-31'
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
# adding precipt data to compare
url = "https://daymet.ornl.gov/single-pixel/api/data" \
      "?lat=34.9455&lon=-113.2549&vars=prcp&years=&format=csv"
data2 = pd.read_table(url, delimiter=',', skiprows=6)
# starts data at same time as our flow data
data2 = data2[3285:]
# restarts index from 0
# so data2 is starts at 0 so .join works
data2 = data2.reset_index(drop=True)
data = data.join(data2['prcp (mm/day)'])

# %%
# Aggregate flow values to weekly
flow_weekly = data.resample("W", on='datetime').mean()

# %%
# got rid of extreme outliers
# we can adjust this how we want
#  in order to get better accuracy
flow_weekly = flow_weekly[
        (flow_weekly.flow <= 400)]
# %%
# looking for dates I wanted
# used to find training periods
# open to changes to make model more acurate
flow_weekly.iloc[1386]
# %%
# creation of lag timed series
# the loop names each column flow_tm%i and shifts it by i
for i in range(1, 4):
    flow_weekly['flow_tm%s' % i] = flow_weekly['flow'].shift(i)


# making my training period 2010-2015
# could adjust training period to better rep results
train = flow_weekly[974:1205][['flow', 'flow_tm1',
                               'flow_tm2', 'flow_tm3', 'prcp (mm/day)']]
# making testing from 2015-2020
test = flow_weekly[1205:1385][['flow', 'flow_tm1',
                               'flow_tm2', 'flow_tm3', 'prcp (mm/day)']]


# %%
# linear regression with 4 time lags as inputs to the model
# you don't need to change training period (2010-2015)
model4 = LinearRegression()
y = train['flow'].values
x4 = train[['flow_tm1', 'flow_tm2', 'flow_tm3', 'prcp (mm/day)']]
model4.fit(x4, y)
r_sq = model4.score(x4, y)
print('coefficient of determination:', np.round(r_sq, 2))
print('intercept:', np.round(model4.intercept_, 2))
print('slope:', np.round(model4.coef_, 2))

# generate preditions for training phase and testing phase
# (training phase is used to generate coefecients and intercepts)
q_pred4_train = model4.predict(train[['flow_tm1', 'flow_tm2',
                                      'flow_tm3', 'prcp (mm/day)']])
q_pred4_test = model4.predict(test[['flow_tm1', 'flow_tm2',
                                    'flow_tm3', 'prcp (mm/day)']])

# %%
# projecting 2 weeks into the future using 4 time lags
# lists that start with the 3 most recent entries flow entries
# precip is manually input we can
# check weather and decide what to put
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
# print(weeklypred_4)
# %%
# a code that generates monthly mean after 2010
# years can be fine tuned how we'd like
# also we could use lower quantiles and stuff
monthly_precip = []
for i in range(8, 13):
    monthly_precip.append(data2['prcp (mm/day)'][(data2['prcp (mm/day)'] > 0) &
                          (data.year > 2010) & (data.month == i)].mean())
    monthly_precip[i-8] = np.round(monthly_precip[i-8], decimals=1)
    print(np.round(monthly_precip[i-8], decimals=1))
# %%
# projecting 16 weeks into the future
# The + 10 is added to start at 8/21
# I manually inserted the weekly mean from usgs info
# maybe we can streamline this
wk_num = 10
precip = [2.00]
lastweekx3 = [flow_weekly.flow[-(3 + wk_num)]]
lastweekx2 = [flow_weekly.flow[-(2 + wk_num)]]
lastweek = [flow_weekly.flow[-(1 + wk_num)]]
weeklypred = []
for wk in range(16):
    wk1 = lastweek[wk]
    wk2 = lastweekx2[wk]
    wk3 = lastweekx3[wk]
    wk4 = precip[wk]
    lastweekx2.append(wk1)
    lastweekx3.append(wk2)
    # added a bernoulli variable multiplied by monthly mean
    # this way we can simulate how rain would affect model
    # we can mess with bernouli p to afect frequency of rain
    if wk == 0:
        precip.append(monthly_precip[0]*(bernoulli.rvs(size=1, p=0.1)))
    elif wk <= 5:
        precip.append(monthly_precip[1]*(bernoulli.rvs(size=1, p=0.1)))
    elif wk <= 9:
        precip.append(monthly_precip[2]*(bernoulli.rvs(size=1, p=0.1)))
    elif wk <= 13:
        precip.append(monthly_precip[3]*(bernoulli.rvs(size=1, p=0.1)))
    else:
        precip.append(monthly_precip[4]*(bernoulli.rvs(size=1, p=0.1)))
    prediction = model4.intercept_ + model4.coef_[0] * wk1 + model4.coef_[1] \
        * wk2 + model4.coef_[2] * wk3 + model4.coef_[3] * wk4
    lastweek.append(prediction)
    weeklypred.append(prediction)
# print(weeklypred)
# %%
# shows a plot of 16 week prediction
# Note: This changes each time you run the model
# due to the bernouli distribution
# creates unique name list of each week from 1 to 16
weeks = []
for i in range(16):
    weeks.append('week# ' '%s' % (i+1))
# creates a plot of my prediction for each week of the semester

plt.style.use('seaborn-whitegrid')


plt.scatter(x=weeks, y=weeklypred, marker='o', label='predicted flow')
plt.scatter(x=weeks[0:wk_num],
            y=flow_weekly.flow[(flow_weekly.year == 2020)
            & (flow_weekly.month >= 8) & (flow_weekly.day >= 20) |
            (flow_weekly.year == 2020) & (flow_weekly.month >= 9)],
            marker='o', label='observed')

plt.ylabel('Flow (cfs)')
plt.ylim([0, 200])
plt.title('Weekly Discharge Prediction')
plt.xticks(rotation=45, fontsize=10)
plt.legend()
plt.savefig('Discharge_Prediction.png')
# %%
# shows a plot of post 2005 data for the training period, and testing period
fig, ax = plt.subplots()
ax.plot(flow_weekly['flow'], label='full')
ax.plot(train['flow'], 'r:', label='training')
ax.plot(test['flow'], color='orange', linestyle='--', label='testing')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
       xlim=[datetime.date(2005, 1, 1), datetime.date(2020, 8, 23)])
ax.legend()
plt.savefig('Observed_flow.png')

# %%
# Scatter plot of t vs t-1 flow with normal axes
# I'd like this to show how it compares to precip
# but can't figure it out
fig, ax = plt.subplots()
ax.scatter(train['flow_tm1'], train['flow'], marker='p',
           color='blueviolet', label='observations')
ax.set(xlabel='flow t-1', ylabel='flow t')
ax.plot(np.sort(train['flow_tm1']), np.sort(q_pred4_train), label='AR model')
ax.legend()
plt.savefig('AR_model.png')
# %%
# prints the prediction that you will use
print(f'The prediction for week 1 is {str(weeklypred_4[0].round(2))} cfs '
      f'and week 2 is {str(weeklypred_4[1].round(2))} cfs')

# %%
