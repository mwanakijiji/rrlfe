#!/usr/bin/env python
# coding: utf-8

# This reads in files of period info, epochs-of-max, and spectra BJDs to
# find the phases as the time the spectra were taken

# Created 2022 May 23 by E.S.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_spectra_epochs = pd.read_csv("./data/spec_bjds.csv")
df_stellar_periods = pd.read_csv("./data/output_periods_all_stars.csv")
df_epochs_of_max = pd.read_csv("./data/bjds_epochs_of_max.csv")


# make column in each dataframe that will be used to match by star
df_spectra_epochs["star_match"] = df_spectra_epochs["file"]
df_spectra_epochs["star_match"] = df_spectra_epochs["star_match"].str.replace("__"," ") # underscore of 2
df_spectra_epochs["star_match"] = df_spectra_epochs["star_match"].str.replace("_"," ") # underscore of 1
df_spectra_epochs["star_match"] = df_spectra_epochs["star_match"].apply(lambda row: row.rsplit(' ',1)[0])

df_epochs_of_max["star_match"] = df_epochs_of_max["star"].str.replace("_"," ")

df_stellar_periods["star_match"] = df_stellar_periods["star"]


# remove some ambiguities
df_epochs_of_max["photo_bjd"] = df_epochs_of_max["bjd"]
df_spectra_epochs["spec_bjd"] = df_spectra_epochs["bjd"]

## ## THE BELOW MERGE REMOVES V535 MON AND V445 OPH; FIX THESE
# df_spectra_epochs["star_match"] == "V 535"
# df_spectra_epochs["star_match"] == "V445 O"
# df_epochs_of_max["star_match"] == "V445 Oph"
# df_epochs_of_max["star_match"] == "V535 Mon"


# combine epochs-of-max and spectral epochs
result = pd.merge(df_spectra_epochs,
                 df_epochs_of_max[['star_match','photo_bjd']],
                 on='star_match')

# combine with periods
result2 = pd.merge(result,
                 df_stellar_periods[['star_match','T_final','err_tot']],
                 on='star_match')

# find phases
result2["phasemod"] = np.nan
result2["baseline_time"] = np.subtract(result2["spec_bjd"],result2["photo_bjd"])
result2["baseline_div_period"] = np.divide(result2["baseline_time"],result2["T_final"])

# for cases where spectra were taken after photometry
#result2["phasemod"] = np.mod(result2["baseline_time"],result2["T_final"])
result2["phasemod"] = [t%1. for t in result2["baseline_div_period"]] # intermediate values which still have to be recalculated
'''
idx_pos = (result2["baseline_time"] > 0)
result2["phasemod"].loc[idx_pos] = np.mod(result2["baseline_time"].where(idx_pos),result2["T_final"].where(idx_pos))

# vice versa
idx_neg = (result2["baseline_time"] < 0)
result2["phasemod"].loc[idx_neg] = np.subtract(1.,
                                                np.mod(result2["baseline_time"].where(idx_neg),
                                                        result2["T_final"].where(idx_neg))
                                                )
'''
result3 = result2.sort_values(by="file").reset_index(drop=True)

import ipdb; ipdb.set_trace()

'''
# fyi print
for t in range(0,len(result3)):
    print(result3["file"].loc[t])
    print(result3["spec_bjd"].loc[t])
    print("----")
'''

result3.to_csv("./data/junk.csv", index=False)
