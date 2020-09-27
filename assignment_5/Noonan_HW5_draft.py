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
# Sorry no more helpers past here this week, you are on your own now :) 
# Hints - you will need the functions: describe, info, groupby, sort, head and tail.

# See what we've got going on in the dataframe "data"
data.head(3)

#%%
data.shape

# %%
# TESTING 
# PANDAS .plot() method
f, ax = plt.subplots()
data.plot(x="month", y="flow", title="flow vs. month", ax=ax)
plt.show()

# %%
# TESTING 
# MATPLOTLIB TO DO SAME (more flexible approach) - BUT HOW TO GET X AND Y LABELS?
f, ax = plt.subplots()
ax.plot(data.month,
        data.flow)
ax.set(title="flow vs. month")
plt.show()

# %%
# TESTING 
# MATPLOTLIB ax.bar() method
f, ax = plt.subplots()
ax.bar(x=data.month,
       height=data.flow)
plt.show()

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
# HOW TO GET RID OF THE UNWANTED COLUMNS OR PULL OUT ONLY DESIRED COLUMNS FROM TABLE?
data2 = data.sort_values(by="flow", ascending=False)
data2.head(5)
#%%
data2.tail(5)

#%%
#5)Find the highest and lowest flow values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in
# THERE HAS GOT TO BE A MORE EFFICIENT WAY TO DO THIS.....
# HOW TO GET YEAR??
flow_by_month=data.groupby(["month"])[["flow"]].describe()
flow_by_month

#%%
# # max_flow_by_month=data.groupby(["month"])[["flow"]].max()
# max_flow_by_month
#%%
# min_flow_by_month=data.groupby(["month"])[["flow"]].min()
# min_flow_by_month

#%%
flow_by_month.columns=flow_by_month.columns.droplevel(0)
flow_by_month

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
x = 158
data[data["flow"] == x]



#%%
#6)Provide a list of historical dates with flows that are within 10% of your week 1 forecast value. If there are none than increase the %10 window until you have at least one other value and report the date and the new window you used


# %%
