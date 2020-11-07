# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import bernoulli

#%%
def weekly_min(data_week_min, month1, day_more, day_less):

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
def prediction(wk, lastweek, lastweekx2, lastweekx3, precip, temp, temp2, intercept_, coef_, weeklypred):
    for i in range(wk):
        wk1 = lastweek[i]
        wk2 = lastweekx2[i]
        wk3 = lastweekx3[i]
        precipt = precip[i]
        T = temp[i]
        T2 = temp2[i]

        # appends to last week so that they refer to next time step
        lastweekx2.append(wk1)
        lastweekx3.append(wk2)

        # precip.appends(#) the second weeks expected rainfall mm
        precip.append(0)

        # temp of second week     is number appended
        temp2.append(temp[i])
        # the prediction for week # i
        prediction = intercept_ + coef_[0] * wk1 + coef_[1] \
            * wk2 + coef_[2] * wk3 + coef_[3] * precipt \
            + coef_[4] * T + coef_[5] * T2
        lastweek.append(prediction)

        # creates a list of just my predictions for week 1 then week 2
        weeklypred.append(prediction)

    # prints the prediction that you will use
    print(f'The prediction for week 1 is {str(weeklypred[0].round(2))} cfs '
          f'and week 2 is {str(weeklypred[1].round(2))} cfs')
# %%
def pred_sem(wk, lastweek, lastweekx2, lastweekx3, precip, temp, temp2, monthly_precip, intercept_, coef_, weeklypred, wk_num, flow_weekly):
    
    for i in range(wk):
        wk1 = lastweek[i]
        wk2 = lastweekx2[i]
        wk3 = lastweekx3[i]
        precipt = precip[i]
        T = temp[i]
        T2 = temp2[i]

        # appends to last week so that they refer to next time step
        lastweekx2.append(wk1)
        lastweekx3.append(wk2)

        # precip.appends(#) the second weeks expected rainfall mm
        if i == 0:
            precip.append(monthly_precip[0]*(bernoulli.rvs(size=1, p=0.01)))
        elif i <= 5:
            precip.append(monthly_precip[1]*(bernoulli.rvs(size=1, p=0.03)))
        elif i <= 9:
            precip.append(monthly_precip[2]*(bernoulli.rvs(size=1, p=0.05)))
        elif i <= 13:
            precip.append(monthly_precip[3]*(bernoulli.rvs(size=1, p=0.05)))
        else:
            precip.append(monthly_precip[4]*(bernoulli.rvs(size=1, p=0.08)))
        
        # the prediction for week # i
        prediction = intercept_ + coef_[0] * wk1 + coef_[1] \
            * wk2 + coef_[2] * wk3 + coef_[3] * precipt \
            + coef_[4] * T + coef_[5] * T2
        lastweek.append(prediction)

        # creates a list of just my predictions for week 1 then week 2
        weeklypred.append(prediction)



    weeks = []
    for i in range(wk):
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
    