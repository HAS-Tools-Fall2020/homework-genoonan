#Noonan - HW3.py
#%%
print("This is Gillian Noonan's HW3")

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
filename = 'streamflow_week3.txt'
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

#make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)


#%%
#Jill's homework code
#Answers to question 1 
print ("Flow is the type object:", type(flow))
print ("Flow contains the object type:", type(flow[1]))

print ("Year is the type object:",type(year))
print ("Year contains the object type:",type(year[1]))

print ("Month is the type object:",type(month))
print ("Month contains the object type:", type(month[1]))

print ("Day is the type object:", type(day))
print ("Day contains the object type:",type(day[1]))

print ("the length of the flow list is:", len(flow))
print ("the length of the year list is:", len(year))
print ("the length of the month list is:", len(month))
print ("the length of the day list is:", len(day))

# %%
#just practicing - or can do this:
lists = [flow, date, year, month, day]
for dlist in lists:
        print ("the length of the variable 'dlist' is:", len(dlist))


# %%
# Calculating some basic properites - added text string to practice
print("minimum flow of streamflow3.txt is", min(flow))
print("maximum flow of streamflow3.txt is", max(flow))
print("mean flow of streamflow3.txt is", np.mean(flow))
print("standard deviation of streamflow3.txt is", np.std(flow))


# JILL's ATTEMPT at modifiying the Starter Code
#question #2
#%%
#making an empty list
ilist = []

#%%
#looping through flow list to obtain data of interest - 
#How many flow rates were greater than my prediction for month of september
ilist = [i for i in range(len(month)) if flow[i] > 60 and month[i]==9]
print(len(ilist))

#%%
#making an empty list
ilist2 = []

#%%
#looping through flow list to obtain data of interest - 
#How many flow rates have been recorded total for month of september since 1989
ilist2 = [i for i in range(len(month)) if month[i]==9]
print(len(ilist2))

#%%
#Getting number of times daily flow was greater as a percentage (since 1989)
v1 = len(ilist)
v2 = len(ilist2)
print (v1/v2*100)

#%%
#Question #3 Part 1
#making a new empty list
ilist3 = []

#%%
#looping through flow list to obtain data of interest - 
#How many flow rates were greater than my prediction for month of september for years <= 2000
ilist3 = [i for i in range(len(month)) if flow[i] > 60 and month[i]==9 and year[i] <=2000]
print(len(ilist3))

#%%
#making an empty list
ilist4 = []

#%%
#looping through flow list to obtain data of interest - 
#How many flow rates have been recorded total for month of september for years <= 2000
ilist4 = [i for i in range(len(month)) if year[i]<=2000 and month[i] == 9]
print(len(ilist4))

#%%
#Getting number of times daily flow was greater as a percentage, for years <=2000
v1 = len(ilist3)
v2 = len(ilist4)
print (v1/v2*100)# %%

# %%
#Question #3 Part2
#making a new empty list
ilist5 = []

#%%
#looping through flow list to obtain data of interest - 
#How many flow rates were greater than my prediction for month of september for years >=2010
ilist5 = [i for i in range(len(month)) if flow[i] > 60 and month[i]==9 and year[i] >=2010]
print(len(ilist5))

#%%
#making an empty list
ilist6 = []

#%%
#looping through flow list to obtain data of interest - 
#How many flow rates have been recorded total for month of september for years >= 2010
ilist6 = [i for i in range(len(month)) if year[i]>=2010 and month[i] == 9]
print(len(ilist6))

#%%
#Getting number of times daily flow was greater as a percentage, for years <==2000
v1 = len(ilist5)
v2 = len(ilist6)
print (v1/v2*100)# %%


#%%
#making an empty list
ilist7 = []

#%%
#looping through flow list to obtain data of interest - 
#what is mean daily flow for first half of september (day<16)
ilist7 = [i for i in range(len(flow)) if month[i] == 9 and day[i]<16]
subset7 = [flow[i] for i in ilist7]
print (np.mean(subset7))

#%%
#making an empty list
ilist8 = []

#%%
#looping through flow list to obtain data of interest - 
#what is mean daily flow for second half of september (day>=16)
ilist8 = [i for i in range(len(flow)) if month[i] == 9 and day[i]>=16]
subset8 = [flow[i] for i in ilist8]
print (np.mean(subset8))


# %%
# #This is just me trying out plots for flow by month and day
# Import necessary plot package
import matplotlib.pyplot as plt


#%% 
# flow vs. month 
# Result: works, but, Comparing in excel, I think it's plotting max flow value for each month 
fig, ax = plt.subplots(figsize=(12, 12))
ax.bar(month, 
       flow, 
       color="pink")
ax.set(title="Flow vs. month",
       xlabel="month", 
       ylabel="flow")
plt.show()

# %%
#trying out plots #2
# flow vs. day 
# Result: works, think it's plotting max flow per day for all months
# Not sure how to isolate september
fig, ax = plt.subplots(figsize=(12, 12))
ax.bar(day, 
       flow, 
       color="red")
ax.set(title="Flow vs. day",
       xlabel="day", 
       ylabel="flow")
plt.show()


#%%
#trying out plots #3
# average flow vs. day 
# this is a fail - it's all just showing the overall all-time data mean of 345.98
## Not sure how to isolate september - won't run with the below
# if month[i] == 9:
fig, ax = plt.subplots(figsize=(12, 12))
ax.bar(day, 
       np.mean(flow), 
       color="blue")
ax.set(title="Avg. Flow vs. day",
       xlabel="day", 
       ylabel="avg. flow")
plt.show()


#%%
#making an empty list
ilist9 = []

#%%
#prints values for subset September flow and mean flow for September
ilist9 = [i for i in range(len(flow)) if month[i] == 9]
subset9 = [flow[i] for i in ilist9]
print (subset9)
print (np.mean(subset9))

#%%
#trying out plots #4
# average september flow vs. day  - this just gives the monthly Sept. mean of (174.4) 
fig, ax = plt.subplots(figsize=(12, 12))
ax.bar(day, 
       np.mean(subset9), 
       color="yellow")
ax.set(title="Avg. sept. Flow vs. day",
       xlabel="day", 
       ylabel="avg. flow")
plt.show()

#%%
print("the end")
     







# %%
