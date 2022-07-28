#!/usr/bin/env python
# coding: utf-8

# This reads in my and NDL's phase analysis outputs and compares them

# Create 2022 May 28 by E.S.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in NDL
df_ndl_epochs = pd.read_csv("./data/spectra_epochs_lc.csv")
df_ndl_phases = pd.read_csv("./data/phases_ndl.csv")

# read in mine
df_mine = pd.read_csv("./data/spectra_my_bjds_20220726.csv")
import ipdb; ipdb.set_trace()
# make specific
df_mine["my_spec_bjd"] = np.subtract(df_mine["bjd"],2400000) # subtract to compare with NDL
df_mine["my_phase"] = df_mine["phasemod"]
df_mine["spec_file"] = df_mine["file"] # the original spectrum file name
df_ndl_epochs["spec_file"] = df_ndl_epochs["filenames"] # the original spectrum file name (no change by NDL)
df_ndl_epochs["ndl_spec_bjd"] = df_ndl_epochs["bjd"]
df_ndl_phases["ndl_phase"] = df_ndl_phases["Phases"]
ipdb.set_trace()
# remove redundant rows with "c.fits" in filenames col
df_ndl_epochs = df_ndl_epochs.loc[df_ndl_epochs["filenames"].str.contains(".c.fits")==False]
# convert to ints
df_ndl_epochs["number_cur"] = df_ndl_epochs["#"].astype(int)

# extract the "cur" number from NDL's other table
df_ndl_phases["number_cur"] = df_ndl_phases["#Name"].str.split("_").str[-1]
#df_ndl_phases["number_cur"] = df_ndl_phases["#Name"].str.extract('(\d+)')
df_ndl_phases["number_cur"] = df_ndl_phases["number_cur"].astype(int)
ipdb.set_trace()
# extract the star name
df_ndl_epochs["star_name"] = df_ndl_epochs["filenames"].str[:6]
df_ndl_phases["star_name"] = df_ndl_phases["#Name"].str[:6]

# merge NDL's tables with each other based on star name and cur number
df_ndl_merged = df_ndl_epochs.merge(df_ndl_phases, on=["star_name","number_cur"], suffixes=(None,"_y"))
ipdb.set_trace()
# match NDL net table to my results by spectrum number (#)
df_all_merged = df_mine.merge(df_ndl_merged, how='outer', on=["spec_file"])

# find NDL time baselines, for checking only
df_all_merged["ndl_time_baselines"] = np.subtract(np.subtract(df_all_merged["Epoch_Max"],2400000),df_all_merged["ndl_spec_bjd"])
df_all_merged["ndl_baseline_div_period"] = np.divide(df_all_merged["ndl_time_baselines"],df_all_merged["period"])
# erro in phase we would expect from NDL
df_all_merged["error_ndl_phase"] = np.multiply(np.abs(df_all_merged["ndl_baseline_div_period"]),df_all_merged["err_tot"])

# for fyi, find error in phases: multiply error in period by number of cycles in the time baseline
df_all_merged["error_my_phase"] = np.multiply(np.abs(df_all_merged["baseline_div_period"]),df_all_merged["err_tot"])

# one last thing: insert star names in rows where no KELT data (i.e., name was left NaN)
#idx_name_nan = df_all_merged["star_name"].isinf()
#df_all_merged[df_all_merged["star_name"].isna()]

'''
# for checking
plt.clf()
plt.hist(df_all_merged["error_my_phase"], bins=100)
plt.show()
'''

'''
# for checking
plt.scatter(df_all_merged["my_spec_bjd"],df_all_merged["ndl_spec_bjd"])
plt.plot([56200,56500],[56200,56500], linestyle=":", color="gray")
plt.show()
'''

'''
# for checking
plt.scatter(df_all_merged["Period"],df_all_merged["T_final"])
plt.plot([0,1],[0,1], linestyle=":", color="gray")
plt.show()
'''

# for comparing NDL and my phases, and troubleshooting disagreement
ipdb.set_trace()
plt.clf()
plt.scatter(df_all_merged["my_phase"],df_all_merged["ndl_phase"])

for i in range(0,len(df_all_merged)):


    plt.annotate(df_all_merged["spec_file"].loc[i],
                 xy=(df_all_merged["my_phase"].loc[i],df_all_merged["ndl_phase"].loc[i]))

    '''
    plt.annotate(np.round(df_all_merged["ndl_baseline_div_period"].loc[i],2),
                 xy=(df_all_merged["my_phase"].loc[i],df_all_merged["ndl_phase"].loc[i]))
    '''
#plt.scatter(np.subtract(1.,df_all_merged["my_phase"]),df_all_merged["ndl_phase"])
plt.plot([0,1],[0,1], linestyle=":", color="gray")
plt.xlabel("Eckhart phase")
plt.ylabel("Nathan phase")
plt.title("dashed line: 1-to-1")
plt.show()



output_file_name = './data/junk.csv'
df_all_merged.to_csv(output_file_name)
print("Wrote ", output_file_name)
