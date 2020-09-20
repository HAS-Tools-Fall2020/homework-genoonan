# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('data', filename)
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)



# Jill Question Answering Code
#%%
print(flow_data)
# %%
type(flow_data)

# %%
flow_data.dtype

# %%
flow_data.ndim
# %%
flow_data.shape

# %%
#Set Wk4 predication variable
Wk4_prediction = 55.6
print(Wk4_prediction)

# %%
# Count the number of values with flow > Wk4prediction and month ==9
flow_count_greater = np.sum((flow_data[:,3] > Wk4_prediction) & (flow_data[:,1]==9))
print(flow_count_greater) 
# Count the number of total values with month ==9
flow_count_Sep = np.sum((flow_data[:,1]==9))
print(flow_count_Sep) 
#calculate percentage
print((flow_count_greater / flow_count_Sep)*100)

#%%
#In or before 2000: 
# Count the number of values with flow > Wk4prediction and month ==9 and year <=2000
flow_count_greater_1989_2000 = np.sum((flow_data[:,3] > Wk4_prediction) & (flow_data[:,1]==9) & (flow_data[:,0]<=2000))
print(flow_count_greater_1989_2000)

#%%
# Count the number of total values with month ==9 and year <=2000
flow_count_Sep_1989_2000 = np.sum((flow_data[:,1]==9) & (flow_data[:,0]<=2000))
print(flow_count_Sep_1989_2000) 

#calculate percentage
print((flow_count_greater_1989_2000 / flow_count_Sep_1989_2000)*100)

#%%
#In or before 2000: 
# Count the number of values with flow > Wk4prediction and month ==9 and year <=2000
flow_count_greater_1989_2000 = np.sum((flow_data[:,3] > Wk4_prediction) & (flow_data[:,1]==9) & (flow_data[:,0]<=2000))
print(flow_count_greater_1989_2000)

#%%
# Count the number of total values with month ==9 and year <=2000
flow_count_Sep_1989_2000 = np.sum((flow_data[:,1]==9) & (flow_data[:,0]<=2000))
print(flow_count_Sep_1989_2000) 

#calculate percentage
print((flow_count_greater_1989_2000 / flow_count_Sep_1989_2000)*100)
#%%
# Calculate the average flow for these same criteria 
flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', flow_mean, "when this is true")