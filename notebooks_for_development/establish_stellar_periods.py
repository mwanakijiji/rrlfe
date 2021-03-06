#!/usr/bin/env python
# coding: utf-8

# This takes periods as found by RW, NDL and combines them to find an established period

# Created 2022 May 22 by E.S.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_name = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/input_periods_all_stars.csv"

df = pd.read_csv(file_name)

# initialize
df["err_diff"] = np.nan
df["err_tot"] = np.nan

# find final periods: simple average across values
cols = ['T_KELT', 'T_TESS', 'T_other']
df["T_final"] = df[cols].mean(axis=1)

'''
# How to find errors?

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

# 1. case where both KELT-based and TESS-based periods are available:
for i in range(0,len(df)):
    #print(i)
    # check if there are periods from both KELT and TESS (but TESS has no error)
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

        # for checking
        print("------")
        print("star", df["star"].iloc[i])
        print("err_diff", err_diff)
        print("err_T_TESS", err_T_TESS)
        print("err_tot", df["err_tot"].loc[i])

for i in range(0,len(df)):
    # check if there are errors from both KELT and TESS
    T_TESS = df["T_TESS"].iloc[i]
    T_KELT = df["T_KELT"].iloc[i]
    err_T_TESS = df["err_T_TESS"].iloc[i]

    # 2. case where only TESS-based period available:
    if ~np.isnan(T_TESS) and np.isnan(T_KELT):
        err_diff_avg = np.nanmean(df["err_diff"])
        df["err_tot"].loc[i] = np.sqrt(np.add(np.power(err_T_TESS,2.),np.power(err_diff_avg,2.)))

        # for checking
        print("------")
        print("star", df["star"].iloc[i])
        print("err_diff_avg", err_diff_avg)
        print("err_T_TESS", err_T_TESS)
        print("err_tot", df["err_tot"].loc[i])

    # 3. case where only KELT-based period available:
    elif np.isnan(T_TESS) and ~np.isnan(T_KELT):
        err_TESS_avg = np.nanmean(df["err_T_TESS"])
        df["err_tot"].loc[i] = np.sqrt(np.add(np.power(err_TESS_avg,2.),np.power(err_diff_avg,2.)))

        # for checking
        print("------")
        print("star", df["star"].iloc[i])
        print("err_diff_avg", err_diff_avg)
        print("err_TESS_avg", err_TESS_avg)
        print("err_tot", df["err_tot"].loc[i])


# average total error so far
avg_err_tot_empirical = np.nanmean(df["err_tot"])

for i in range(0,len(df)):
    # 4. case where neither TESS nor KELT periods are available:
    T_TESS = df["T_TESS"].iloc[i]
    T_KELT = df["T_KELT"].iloc[i]
    if np.isnan(T_TESS) and np.isnan(T_KELT):
        df["err_tot"].loc[i] = avg_err_tot_empirical

output_file_name = "junk.csv"
df.reset_index(drop=True, inplace=True)
df.to_csv(output_file_name, index=False)
print("Wrote ",output_file_name)
