#!/usr/bin/env python
# coding: utf-8

# This takes periods as found by RW, NDL and combines them to find an established period

# Created 2022 May 22 by E.S.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_name = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/input_periods_all_stars_master.csv"

df = pd.read_csv(file_name)

# initialize
df["err_diff_NDL"] = np.nan
df["err_tot"] = np.nan

# find final periods: simple average across NDL values
cols = ['T_KELT_NDL', 'T_TESS_NDL', 'T_other']
df["T_final"] = df[cols].mean(axis=1)

'''
# How to find errors?

1. case where both KELT-based and TESS-based periods are available (T_KELT_NDL, T_TESS_NDL, T_TESS_RW, err_T_TESS_RW):

	T_final = 0.5 * [ T_TESS_NDL + T_KELT_NDL ] 	# simple average

	err_tot**2 = err_TESS_RW**2  + ( T_TESS_NDL - T_TESS_RW )**2 + ( T_TESS_NDL - T_KELT_NDL )**2 


2. case where only TESS-based period available (T_TESS_NDL, T_TESS_RW, err_T_TESS_RW):

	T_final = T_TESS_NDL

    err_tot**2 = err_T_TESS_RW**2 + ( T_TESS_NDL - T_TESS_RW )**2


3. case where only KELT-based period available ( T_KELT_RW, T_KELT_NDL, err_T_KELT_RW ):

	T_final = T_KELT_NDL

	err_tot**2 = ( T_KELT_RW - T_KELT_NDL )**2  + err_T_KELT_RW**2

4. case where neither TESS nor KELT periods are available:

	T_final = avg[ T_final ]

    average of the other errors
'''
import ipdb; ipdb.set_trace()
# 1. case where both KELT-based and TESS-based periods are available:
for i in range(0,len(df)):
    #print(i)
    # check if there are periods from both KELT and TESS
    T_TESS_NDL = df["T_TESS_NDL"].iloc[i]
    T_KELT_NDL = df["T_KELT_NDL"].iloc[i]
    T_TESS_RW = df["T_TESS_RW"].iloc[i]
    err_T_TESS_RW = df["err_T_TESS_RW"].iloc[i]

    if (~np.isnan(T_TESS_NDL) and ~np.isnan(T_KELT_NDL)) and (~np.isnan(T_TESS_RW) and ~np.isnan(err_T_TESS_RW)):

        # T_final = 0.5 * [ T_TESS_NDL + T_KELT_NDL ] 	# simple average, already done further above
        # err_tot**2 = err_TESS_RW**2  + ( T_TESS_NDL - T_TESS_RW )**2 + ( T_TESS_NDL - T_KELT_NDL )**2 

        df["err_tot"].loc[i] = np.sqrt( df["err_T_TESS_RW"].loc[i]**2 + (df["T_TESS_NDL"].loc[i]-df["T_TESS_RW"].loc[i])**2 + (df["T_TESS_NDL"].loc[i]-df["T_KELT_NDL"].loc[i])**2  ) 

        # for checking
        print("------")
        print('case 1')
        print("star", df["star"].iloc[i])
        print("T_final", df["T_final"].loc[i])
        print("err_tot", df["err_tot"].loc[i])
        import ipdb; ipdb.set_trace()

for i in range(0,len(df)):
    # check if there are errors from both KELT and TESS
    # check if there are periods from both KELT and TESS
    T_TESS_NDL = df["T_TESS_NDL"].iloc[i]
    T_KELT_NDL = df["T_KELT_NDL"].iloc[i] # should be nan
    T_TESS_RW = df["T_TESS_RW"].iloc[i]
    err_T_TESS_RW = df["err_T_TESS_RW"].iloc[i]

    # 2. case where only TESS-based period available:
    if (~np.isnan(T_TESS_NDL) and np.isnan(T_KELT_NDL)) and (~np.isnan(T_TESS_RW) and ~np.isnan(err_T_TESS_RW)):
        # err_tot**2 = err_T_TESS_RW**2 + ( T_TESS_NDL - T_TESS_RW )**2

        df["err_tot"].loc[i] = np.sqrt( df["err_T_TESS_RW"].loc[i]**2 + (df["T_TESS_NDL"].loc[i]-df["T_TESS_RW"].loc[i])**2 )

        # for checking
        print("------")
        print('case 2')
        print("star", df["star"].iloc[i])
        print("T_total", df["T_final"].loc[i])
        print("err_tot", df["err_tot"].loc[i])

    # 3. case where only KELT-based period available:
    elif (np.isnan(T_TESS_NDL) and np.isnan(T_KELT_NDL)) and (np.isnan(T_TESS_RW) and np.isnan(err_T_TESS_RW)):
        # err_tot**2 = ( T_KELT_RW - T_KELT_NDL )**2  + err_T_KELT_RW**2
        
        df["err_tot"].loc[i] = np.sqrt( df["err_T_KELT_RW"].loc[i]**2 + (df["T_KELT_RW"].loc[i]-df["T_KELT_NDL"].loc[i])**2 )

        # for checking
        print("------")
        print('case 3')
        print("star", df["star"].iloc[i])
        print("T_total", df["T_final"].loc[i])
        print("err_tot", df["err_tot"].loc[i])


# average total error so far
avg_err_tot_empirical = np.nanmean(df["err_tot"])

for i in range(0,len(df)):
    # 4. case where neither TESS nor KELT periods are available:
    T_TESS_NDL = df["T_TESS_NDL"].iloc[i]
    T_KELT_NDL = df["T_KELT_NDL"].iloc[i]
    if np.isnan(T_TESS_NDL) and np.isnan(T_KELT_NDL):
        df["err_tot"].loc[i] = avg_err_tot_empirical

output_file_name = "junk.csv"
df.reset_index(drop=True, inplace=True)
df.to_csv(output_file_name, index=False)
print("Wrote ",output_file_name)
