# %%
import numpy as np

# %%
avg_monthly_precip = np.array([0.70, 0.75, 1.85])

print(avg_monthly_precip)
# %%
precip_2002_2013 = np.array([[1.07, 0.44, 1.50],[0.27, 1.13, 1.72]])

print(precip_2002_2013)
# %%
import os
import numpy as np
import earthpy as et
# %%

# %%
monthly_precip_url = 'https://ndownloader.figshare.com/files/12565616'
et.data.get_data(url=monthly_precip_url)
# %%
# Import necessary packages
import os
import numpy as np
import earthpy as et
# %%
# Download .txt with avg monthly precip (inches)
monthly_precip_url = 'https://ndownloader.figshare.com/files/12565616'
et.data.get_data(url=monthly_precip_url)

# Download .csv of precip data for 2002 and 2013 (inches)
precip_2002_2013_url = 'https://ndownloader.figshare.com/files/12707792'
et.data.get_data(url=precip_2002_2013_url)
# %%
# Set working directory to earth-analytics
os.chdir(os.path.join(et.io.HOME, 'earth-analytics'))
# %%
# Import average monthly precip to numpy array
fname = os.path.join("data", "earthpy-downloads",
                     "avg-monthly-precip.txt")

avg_monthly_precip = np.loadtxt(fname)

print(avg_monthly_precip)
# %%
# Import monthly precip for 2002 and 2013 to numpy array
fname = os.path.join("data", "earthpy-downloads",
                     "monthly-precip-2002-2013.csv")

precip_2002_2013 = np.loadtxt(fname, delimiter = ",")

print(precip_2002_2013)
# %%
# Check dimensions of avg_monthly_precip
avg_monthly_precip.ndim
# %%
# Check dimensions of precip_2002_2013
precip_2002_2013.ndim
# %%
# Check shape of precip_2002_2013
precip_2002_2013.shape
# %%
# Check shape of avg_monthly_precip
avg_monthly_precip.shape
# %%
avg_monthly_precip.shape
avg_monthly_precip[11]

# %%
avg_monthly_precip.shape

# %%
precip_2002_2013.shape

# %%
