# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import bernoulli

# %%


def weekly_min1(data_week_min, month1, day_more, day_less, seasonal_list):

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


def weekly_min2(data_week_min, month1, day1, month2, day2, seasonal_list):

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
            and prints the output minimum flow value
    '''
    
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
# NOTE: Jake, don't forget to add the doc strings for these functions


def prediction(wk, lastweek, lastweekx2, lastweekx3,
               precip, temp, temp2, intercept_, coef_, weeklypred):
    '''Function (prediction):
    This function that makes a prediction that is a specified length.
    The data utilizes a 6 times dependent linear regressive model.
    
    Parameters
    ----------
    wk: list
            How many timesteps you want the model to run for.
    lastweek: list (three parameters)
            Flow values for the last three weeks before model starts.
    precip: list
            is predicted rainfall that is length wk.
    temp: list (two parameters)
            Expected temperatures for the duration of the model
    intercept_: int
            The intercept of the model.
    coef_: list
            Coeficeints of the model (slope).
    Returns
    ------
    Weeklypred: list
            Is where you want the prediction data to be stored.
    '''
    for i in range(wk):
        # appends to last week so that they refer to next time step
        lastweekx2.append(lastweek[i])
        lastweekx3.append(lastweekx2[i])

        # temp of second week is number appended
        temp2.append(temp[i])
        # the prediction for week # i
        prediction = intercept_ + coef_[0] * lastweek[i] + coef_[1] \
            * lastweekx2[i] + coef_[2] * lastweekx3[i] + coef_[3] * precip[i] \
            + coef_[4] * temp[i] + coef_[5] * temp2[i]
        lastweek.append(prediction)

        # creates a list of just my predictions for week 1 then week 2
        weeklypred.append(prediction)

    # prints the prediction that you will use
    print(f'The prediction for week 1 is {str(weeklypred[0].round(2))} cfs '
          f'and week 2 is {str(weeklypred[1].round(2))} cfs')


# %%
def pred_sem(wk, lastweek, lastweekx2, lastweekx3, precip, temp,
             temp2, monthly_precip, intercept_, coef_, weeklypred,
             flow_weekly):
    '''Function (prediction):
    This function that makes a prediction that is a specified length.
    The data utilizes a 6 times dependent linear regressive model.
    Has a probability distribution portion but is 0 by default
    
    Parameters
    ----------
    wk: list
            How many timesteps you want the model to run for.
    lastweek: list (three parameters)
            Flow values for the last three weeks before model starts.
    monthly_precip: list
            Is predicted rainfall that is length wk.
    temp: list (two parameters)
            Expected temperatures for the duration of the model  
    intercept_: int
            The intercept of the model.
    coef_: list
            Coeficeints of the model (slope).
    flow_weekly: dataframe
            A dataframe where flow observed flow comes from 
            by default starts at the week of 8/21/20
    Returns
    ------
    Weeklypred: list
            Is where you want the prediction data to be stored. Along,
            with a graph of observed flow and predicted flow
    '''
    for i in range(wk):
        # appends to last week so that they refer to next time step
        lastweekx2.append(lastweek[i])
        lastweekx3.append(lastweekx2[i])

        # precip.appends(#) the second weeks expected rainfall mm
        # Can incorporate probability at each week if desired by making 
        # p from 0 to 1 hidden because not used for this week
        if i == 0:
            precip.append(monthly_precip[0]*(bernoulli.rvs(size=1, p=0)))
        elif i <= 5:
            precip.append(monthly_precip[1]*(bernoulli.rvs(size=1, p=0)))
        elif i <= 9:
            precip.append(monthly_precip[2]*(bernoulli.rvs(size=1, p=0)))
        elif i <= 13:
            precip.append(monthly_precip[3]*(bernoulli.rvs(size=1, p=0)))
        else:
            precip.append(monthly_precip[4]*(bernoulli.rvs(size=1, p=0)))

        # the prediction for week # i
        prediction = intercept_ + coef_[0] * lastweek[i] + coef_[1] \
            * lastweekx2[i] + coef_[2] * lastweekx3[i] + coef_[3] * precip[i] \
            + coef_[4] * temp[i] + coef_[5] * temp2[i]
        lastweek.append(prediction)

        # creates a list of just my predictions for week 1 then week 2
        weeklypred.append(prediction)

    weeks = []
    for i in range(wk):
        weeks.append('week# ' '%s' % (i+1))
    # creates a plot of my prediction for each week of the semester

    plt.style.use('seaborn-whitegrid')

    plt.scatter(x=weeks, y=weeklypred, marker='o', label='predicted flow')
    plt.scatter(x=weeks,
                y=flow_weekly.flow[(flow_weekly.year == 2020)
                                   & (flow_weekly.month >= 8)
                                   & (flow_weekly.day >= 19) |
                                   (flow_weekly.year == 2020)
                                   & (flow_weekly.month >= 9)],
                marker='o', label='observed')

    plt.ylabel('Flow (cfs)')
    plt.ylim([0, 140])
    plt.title('Weekly Discharge Prediction')
    plt.xticks(rotation=45, fontsize=10)
    plt.legend()
