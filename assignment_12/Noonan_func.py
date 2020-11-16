# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

