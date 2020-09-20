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
# Count the number of total values with month ==9 and year <=2000
flow_count_Sep_1989_2000 = np.sum((flow_data[:,1]==9) & (flow_data[:,0]<=2000))
print(flow_count_Sep_1989_2000) 
#calculate percentage
print((flow_count_greater_1989_2000 / flow_count_Sep_1989_2000)*100)

#%%
#In or after 2010: 
# Count the number of values with flow > Wk4prediction and month ==9 and year >=2010
flow_count_greater_2010_2020 = np.sum((flow_data[:,3] > Wk4_prediction) & (flow_data[:,1]==9) & (flow_data[:,0]>=2010))
print(flow_count_greater_2010_2020)
# Count the number of total values with month ==9 and year >=2010
flow_count_Sep_2010_2020 = np.sum((flow_data[:,1]==9) & (flow_data[:,0]>=2010))
print(flow_count_Sep_2010_2020) 
#calculate percentage
print((flow_count_greater_2010_2020 / flow_count_Sep_2010_2020)*100)


#%%
# Calculate the average flow for 1st half of September
print(flow_data)
flow_mean_Sep_begin = np.mean(flow_data[(flow_data[:,1]==9) & (flow_data[:,2]<=15), 3])
print(flow_mean_Sep_begin)

#%%
# Calculate the average flow for 2nd half of September
flow_mean_Sep_begin = np.mean(flow_data[(flow_data[:,1]==9) & (flow_data[:,2]>15), 3])
print(flow_mean_Sep_begin)

# %%
# Make a histogram of data
# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')


#%%
# Attempt: Trying to isolate just September
flow_data_Sep = flow_data[flow_data[:,1] ==9]
mybins = np.linspace(0, 1000, num=20)
plt.hist(flow_data_Sep[:,3], bins = mybins)
plt.title('September Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# %%