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


#Histogram Plotting
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
# Attempt: Isolate just September
flow_data_Sep1 = flow_data[flow_data[:,1] ==9]
mybins = np.linspace(0, 2000, num=20)
plt.hist(flow_data_Sep1[:,3], bins = mybins)
plt.title('September Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for last 10 years only
flow_data_Sep2 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]>2010)]
mybins = np.linspace(0, 1000, num=20)
plt.hist(flow_data_Sep2[:,3], bins = mybins)
plt.title('September Streamflow 2010-2020')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for last 2 years only
flow_data_Sep3 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]>2018)]
mybins = np.linspace(0, 200, num=20)
plt.hist(flow_data_Sep3[:,3], bins = mybins)
plt.title('September Streamflow 2018-2020')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for last 10 years only and week of 9/20 - 9/26
flow_data_Sep19_26_2010_2020 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]>2010) & (flow_data[:,2] >=20) & (flow_data[:,2]<=26 )]
mybins = np.linspace(0, 250, num=20)
#mybins = np.linspace(0, np.max(flow_data_Sep19_26), num=20) 
plt.hist(flow_data_Sep19_26_2010_2020[:,3], bins = mybins)
plt.title('September Streamflow 2010-2020, Week of Sep20-26')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for last 2 years only and week of 9/20 - 9/26
flow_data_Sep19_26_2018_2020 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]>=2018) & (flow_data[:,2] >=20) & (flow_data[:,2]<=26 )]
mybins = np.linspace(0, 160, num=10)
#mybins = np.linspace(0, np.max(flow_data_Sep19_26), num=20) 
plt.hist(flow_data_Sep19_26_2018_2020[:,3], bins = mybins)
plt.title('September Streamflow 2018-2020, Week of Sep20-26')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#%%
# Attempt: Isolate just September for 2020
flow_data_Sep2020 = flow_data[(flow_data[:,1] ==9) & (flow_data[:,0]==2020)]
mybins = np.linspace(0, 80, num=10)
#mybins = np.linspace(0, np.max(flow_data_Sep19_26), num=20) 
plt.hist(flow_data_Sep2020[:,3], bins = mybins)
plt.title('September Streamflow 2020')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#Quantiles
# %%
# Get the quantiles of flow
# Two different approaches ---  you should get the same answer
# just using the flow column
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)
# Or computing on a colum by column basis 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
# and then just printing out the values for the flow column
print('Method two flow quantiles:', flow_quants2[:,3])

#%%
#Quantiles and stats for September 2020
flow_quants_Sep2020 = np.quantile(flow_data_Sep2020[:,3], q=[0,0.1, 0.5, 0.9])
print(flow_quants_Sep2020)
print(np.min(flow_data_Sep2020[:,3]))
print(np.max(flow_data_Sep2020[:,3]))
print(np.mean(flow_data_Sep2020[:,3]))
print(np.median(flow_data_Sep2020[:,3]))
#flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])
# %%
