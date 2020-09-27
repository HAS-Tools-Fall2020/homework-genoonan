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
data2 = data[['datetime', 'month', 'flow']]
data2

#%%
data2.sort_values(by="flow", ascending=False)
#%%
data2.head(5)
#%%
data2.tail(5)

#%%
#5)Find the highest and lowest flow values for every month of the year (i.e. you will find 12 maxes and 12 mins) and report back what year these occurred in
# THIS WORKS BUT IT'S CLUNKY AND LOOOOONG.  THERE HAS GOT TO BE A MORE EFFICIENT WAY TO DO THIS I'M SURE!!.....for now, it gives me the answers need though......
flow_by_month=data.groupby(["month"])[["flow"]].describe()
flow_by_month.columns=flow_by_month.columns.droplevel(0)
flow_by_month

#%%
data3= data[["year", "month", "flow"]]
data3

#PAINSTAKINGLY PULLING OUT YEARS 
#%%
x = 1
data_Jan = data3[data3["month"] == x]
print(data_Jan.sort_values(by = "flow", ascending = False).tail(1))
print(data_Jan.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 2
data_Feb = data3[data3["month"] == x]
print(data_Feb.sort_values(by = "flow", ascending = False).tail(1))
print(data_Feb.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 3
data_Mar = data3[data3["month"] == x]
print(data_Mar.sort_values(by = "flow", ascending = False).tail(1))
print(data_Mar.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 4
data_Apr = data3[data3["month"] == x]
print(data_Apr.sort_values(by = "flow", ascending = False).tail(1))
print(data_Apr.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 5
data_May = data3[data3["month"] == x]
print(data_May.sort_values(by = "flow", ascending = False).tail(1))
print(data_May.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 6
data_Jun = data3[data3["month"] == x]
print(data_Jun.sort_values(by = "flow", ascending = False).tail(1))
print(data_Jun.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 7
data_Jul = data3[data3["month"] == x]
print(data_Jul.sort_values(by = "flow", ascending = False).tail(1))
print(data_Jul.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 8
data_Aug = data3[data3["month"] == x]
print(data_Aug.sort_values(by = "flow", ascending = False).tail(1))
print(data_Aug.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 9
data_Sep = data3[data3["month"] == x]
print(data_Sep.sort_values(by = "flow", ascending = False).tail(1))
print(data_Sep.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 10
data_Oct = data3[data3["month"] == x]
print(data_Oct.sort_values(by = "flow", ascending = False).tail(1))
print(data_Oct.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 11
data_Nov = data3[data3["month"] == x]
print(data_Nov.sort_values(by = "flow", ascending = False).tail(1))
print(data_Nov.sort_values(by = "flow", ascending = False).head(1))
#%%
x = 12
data_Dec = data3[data3["month"] == x]
print(data_Dec.sort_values(by = "flow", ascending = False).tail(1))
print(data_Dec.sort_values(by = "flow", ascending = False).head(1))
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


# %%
