#Gillian Noonan - Homework 5

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('data', filename)
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# %%
# See what we've got going on in the dataframe "data"
data.head(3)

# %%
#1) Provide a summary of the data frames properties.
data.shape

#%%
# What are the column names?
data.columns

#%%
# # What is its index?
data.index

#%%
# What data types do each of the columns have?
data.info()

#%%
#2) Provide a summary of the flow column including the min, mean, max, standard deviation and quartiles.
data[["flow"]].describe()

#%%
# #3) Provide the same information but on a monthly basis. (Note: you should be able to do this with one or two lines of code)
data.groupby("month")["flow"].describe()

#%%
#4)Provide a table with the 5 highest and 5 lowest flow values for the period of record. Include the date, month and flow values in your summary
data.sort_values(by="flow", ascending=False).head(5)[['datetime', 'month', 'flow']]

#%%
data.sort_values(by="flow", ascending=False).tail(5)[['datetime', 'month', 'flow']]

#%%
#5)Find the highest and lowest flow values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in
flow_by_month=data.groupby(["month"])[["flow"]].describe()
flow_by_month.columns=flow_by_month.columns.droplevel(0)
flow_by_month


#PULLING OUT YEARS For Min and Max Flow
#%%
for x in range(12):
        print(x)
        x = x + 1
        flow_by_year = data[data["month"] == x]
        print(flow_by_year.sort_values(by = "flow", 
                ascending = False).tail(1)[["year", "flow"]])
        print(flow_by_year.sort_values(by = "flow", ascending = False).head(1)[["year", "flow"]])

#%%
# Plot Max Monthly Flow
f, ax = plt.subplots()

ax.bar(flow_by_month.index,
        flow_by_month["max"],
        color="purple")

ax.set(title="Max Monthly Flow")
plt.show()

#%%
# Plot Min Monthly Flow
f, ax = plt.subplots()

ax.bar(flow_by_month.index,
        flow_by_month["min"],
        color="purple")

ax.set(title="Min Monthly Flow")
plt.show()

#%%
#6)Provide a list of historical dates with flows that are within 10% of your week 1 forecast value. If there are none than increase the %10 window until you have at least one other value and report the date and the new window you used

# Get upper and lower range values
w1_value = 56.2
percent_var = 0.1

w1_value_ten_upper = w1_value + (w1_value*percent_var) 
print(w1_value_ten_upper)

w1_value_ten_lower = w1_value - (w1_value*percent_var) 
print(w1_value_ten_lower)

#%%
#getting list of values within 10%
data[(data["flow"] < w1_value_ten_upper) &
         (data["flow"] > w1_value_ten_lower)][["datetime", "flow"]]



# %%
#WEEKLY FORECAST WEEK 5
# 1week forecast - look at last 7 days
data_weekly = data.tail(7)
data_weekly

#%%
data_weekly[["flow"]].describe()

# %%
# look at weekly trend
f, ax = plt.subplots()

ax.plot(data_weekly.day, data_weekly.flow)

ax.set(title="One week flow trend")
plt.show()


# 2week forecast
#AGAIN, THIS IS SOOOO CLUNKY.  HOW CAN I MAKE THIS MORE EFFICIENT - WITH CONDIDTIONALS MAYBE? CAN'T GET THEM TO WORK IN THE FILTER
# %%
#data_Oct = data[data["month"]==10]
# data_Oct

#%%
# data1_Oct_4_10 = data_Oct[data_Oct["day"]>=4]     
# data1_Oct_4_10 
# %%
# data2_Oct_4_10 = data1_Oct_4_10[data1_Oct_4_10["day"]<=10]
# data2_Oct_4_10
# %%
# Get historical stats for October 4-10
# data2_Oct_4_10[["flow"]].describe()

# %%
# TRYING TO UNCLUNK IT 
# UPDATE - SUCCESS!!
month = 10
day_less = 10
day_more = 4
data_Oct_two_week = data[(data["month"]==month) & (data["day"] <=day_less) & (data["day"] >=day_more)]
data_Oct_two_week["flow"].min()

# %%
#seasonal wk6 9/27-10/3
month1 = 9
day1 = 27
month2 = 10
day2 = 3
data_seasonal_6 = data[((data["month"]==month1) & (data["day"] >=day1)) | ((data["month"] ==month2) & (data["day"] <=day2))]
data_seasonal_6["flow"].min()

# %%
#seasonal wk7 10/4-10/10
month = 10
day_less = 10
day_more = 4
data_Oct_two_week = data[(data["month"]==month) & (data["day"] <=day_less) & (data["day"] >=day_more)]
data_Oct_two_week["flow"].min()

# %%
#seasonal wk8 10/11-10/17
month = 10
day_less = 17
day_more = 11
data_Oct_two_week = data[(data["month"]==month) & (data["day"] <=day_less) & (data["day"] >=day_more)]
data_Oct_two_week["flow"].min()
# %%
