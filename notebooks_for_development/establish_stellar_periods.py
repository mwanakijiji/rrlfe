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

1. case where both KELT-based (from NDL) and TESS-based (also from NDL) periods are available:

	T_total = 0.5 * [ T_TESS_NDL + T_KELT_NDL ] 	# simple average

	err_diff_NDL = abs(T_TESS_NDL - T_KELT_NDL)     # if there is a TESS val from NDL, there will be one from RW too

	err_tot**2 = err_TESS_RW**2  + err_diff_NDL**2 ## ## but if RW also has a period, this should get folded in to error


2. case where only TESS-based period available:

	T_total = T_TESS_NDL

	err_diff_avg = avg[  err_diff  ]            # from err_diff vals of other stars further above

	err_tot**2 = err_TESS_RW**2  + err_diff_avg**2 ## ## but if NDL also has a period, this should get folded in to error


3. case where only KELT-based period available (from NDL, and therefore no error):

	T_total = T_KELT_NDL

	err_diff_avg = avg[  err_diff  ]			# from err_diff vals of other stars further above
	err_RW_avg = avg[  err_TESS_RW   ]			# from err_TESS_RW vals further above

	err_tot**2 = err_RW_avg**2  + err_diff_avg**2

4. case where neither TESS nor KELT periods are available:

	T_total = T_other

    just take average of the other errors
'''
import ipdb; ipdb.set_trace()
# 1. case where both KELT-based and TESS-based periods are available:
for i in range(0,len(df)):
    #print(i)
    # check if there are periods from both KELT and TESS (but TESS has no error)
    T_TESS_NDL = df["T_TESS_NDL"].iloc[i]
    T_KELT_NDL = df["T_KELT"].iloc[i]
    err_T_TESS_RW = df["err_T_TESS_RW"].iloc[i]
    #print(T_TESS, T_KELT)

    if ~np.isnan(T_TESS_NDL) and ~np.isnan(T_KELT_NDL):
        #print('i')
        err_diff_NDL = np.abs(np.subtract(T_TESS_NDL,T_KELT_NDL))
        df["err_diff_NDL"].loc[i] = err_diff_NDL

        # propagating error for an average gives 0.5*sqrt(err_1**2 + err_2**2), but here
        # we don't have the error from KELT; so coefficient of 1 (instead of 0.5) here may be overestimate
        df["err_tot"].loc[i] = np.sqrt(np.add(np.power(err_T_TESS_RW,2.),np.power(err_diff_NDL,2.)))

        # for checking
        print("------")
        print("star", df["star"].iloc[i])
        print("err_diff_NDL", err_diff_NDL)
        print("err_T_TESS_RW", err_T_TESS_RW)
        print("T_total", df["T_final"].loc[i])
        print("err_tot", df["err_tot"].loc[i])

for i in range(0,len(df)):
    # check if there are errors from both KELT and TESS
    T_TESS_NDL = df["T_TESS_NDL"].iloc[i]
    T_KELT_NDL = df["T_KELT"].iloc[i]
    err_T_TESS_RW = df["err_T_TESS_RW"].iloc[i]

    # 2. case where only TESS-based period available:
    if ~np.isnan(T_TESS_NDL) and np.isnan(T_KELT_NDL):
        err_diff_NDL_avg = np.nanmean(df["err_diff_NDL"])
        df["err_tot"].loc[i] = np.sqrt(np.add(np.power(err_T_TESS_RW,2.),np.power(err_diff_NDL_avg,2.)))

        # for checking
        print("------")
        print("star", df["star"].iloc[i])
        print("err_diff_NDL_avg", err_diff_NDL_avg)
        print("err_T_TESS_RW", err_T_TESS_RW)
        print("T_total", df["T_final"].loc[i])
        print("err_tot", df["err_tot"].loc[i])

    # 3. case where only KELT-based period available:
    elif np.isnan(T_TESS_NDL) and ~np.isnan(T_KELT_NDL):
        err_TESS_RW_avg = np.nanmean(df["err_T_TESS_RW"])
        df["err_tot"].loc[i] = np.sqrt(np.add(np.power(err_TESS_RW_avg,2.),np.power(err_diff_NDL_avg,2.)))

        # for checking
        print("------")
        print("star", df["star"].iloc[i])
        print("err_diff_NDL_avg", err_diff_NDL_avg)
        print("err_TESS_RW_avg", err_TESS_RW_avg)
        print("T_total", df["T_final"].loc[i])
        print("err_tot", df["err_tot"].loc[i])


# average total error so far
avg_err_tot_empirical = np.nanmean(df["err_tot"])

for i in range(0,len(df)):
    # 4. case where neither TESS nor KELT periods are available:
    T_TESS_NDL = df["T_TESS_NDL"].iloc[i]
    T_KELT_NDL = df["T_KELT"].iloc[i]
    if np.isnan(T_TESS_NDL) and np.isnan(T_KELT_NDL):
        df["err_tot"].loc[i] = avg_err_tot_empirical

output_file_name = "junk.csv"
df.reset_index(drop=True, inplace=True)
df.to_csv(output_file_name, index=False)
print("Wrote ",output_file_name)
