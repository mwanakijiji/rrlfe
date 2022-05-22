#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This takes periods as found by RW, NDL and combines them to find an established period

# Created 2022 May 22 by E.S.


# In[13]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[14]:


file_name = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/periods_all_stars.csv"


# In[15]:


df = pd.read_csv(file_name)


# In[16]:


# initialize

df["err_diff"] = np.nan
df["err_tot"] = np.nan


# In[18]:


# find final periods: simple average across values

cols = ['T_KELT', 'T_TESS', 'T_other']

df["T_final"] = df[cols].mean(axis=1)


# In[19]:


'''
1. case where both KELT-based and TESS-based periods are available:

	err_diff = abs(T_NDL - T_RW)

	err_tot**2 = err_RW**2  + err_diff**2


2. case where only TESS-based period available:

	err_diff_avg = avg[  err_diff  ]

	err_tot**2 = err_RW**2  + err_diff_avg**2


3. case where only KELT-based period available:

	err_diff_avg = avg[  err_diff  ]
	err_RW_avg = avg[  err_RW ]

	err_tot**2 = err_RW_avg**2  + err_diff_avg**2
    
4. case where neither TESS nor KELT periods are available:

    just take average of the others
'''


# In[20]:


# 1. case where both KELT-based and TESS-based periods are available:
for i in range(0,len(df)):
    #print(i)
    # check if there are periods from both KELT and TESS
    T_TESS = df["T_TESS"].iloc[i]
    T_KELT = df["T_KELT"].iloc[i]
    err_T_TESS = df["err_T_TESS"].iloc[i]
    #print(T_TESS, T_KELT)

    if ~np.isnan(T_TESS) and ~np.isnan(T_KELT):
        #print('i')
        err_diff = np.abs(np.subtract(T_TESS,T_KELT))
        df["err_diff"].loc[i] = err_diff
        
        # propagating error for an average gives 0.5*sqrt(err_1**2 + err_2**2), but here 
        # we don't have the error from KELT; so coefficient of 1 (instead of 0.5) here may be overestimate
        df["err_tot"].loc[i] = np.sqrt(np.add(np.power(err_T_TESS,2.),np.power(err_diff,2.)))


# In[22]:


for i in range(0,len(df)):
    # check if there are errors from both KELT and TESS
    T_TESS = df["T_TESS"].iloc[i]
    T_KELT = df["T_KELT"].iloc[i]
    err_T_TESS = df["err_T_TESS"].iloc[i]

    # 2. case where only TESS-based period available:
    if ~np.isnan(T_TESS) and np.isnan(T_KELT):
        err_diff_avg = np.nanmean(df["err_diff"])
        df["err_tot"].loc[i] = np.sqrt(np.add(np.power(err_T_TESS,2.),np.power(err_diff_avg,2.)))
        
    # 3. case where only KELT-based period available:
    elif np.isnan(T_TESS) and ~np.isnan(T_KELT):
        err_TESS_avg = np.nanmean(df["err_T_TESS"])
        df["err_tot"].loc[i] = np.sqrt(np.add(np.power(err_TESS_avg,2.),np.power(err_diff_avg,2.)))

# average total error so far
avg_err_tot_empirical = np.nanmean(df["err_tot"])

for i in range(0,len(df)):
    # 4. case where neither TESS nor KELT periods are available:
    T_TESS = df["T_TESS"].iloc[i]
    T_KELT = df["T_KELT"].iloc[i]
    if np.isnan(T_TESS) and np.isnan(T_KELT):
        df["err_tot"].loc[i] = avg_err_tot_empirical


# In[9]:


output_file_name = "junk.csv"
df.to_csv(output_file_name)
print("Wrote ",output_file_name)


# In[23]:


df


# In[ ]:




