#!/usr/bin/env python
# coding: utf-8

# This reads in a rrlfe output file from an application of the calibration,
# and calculates a net error for a star given the scatter of

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

stem = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/"
filename = stem + "data/retrieved_mcd_incl_corrxn_20230606.csv"

df = pd.read_csv(filename)

# remove values that did not converge
df = df[df.feh_retrieved > -900]

df["star_id"] = df["realization_spec_file_name"].str[:6]

df_mean = df.groupby("star_id", as_index=False).mean()
df_mean["err_feh_retrieved_single"] = df_mean["err_feh_retrieved"]

df_stdev = df.groupby("star_id").std()["feh_retrieved"]

cols_relevant = ["star_id", "feh_retrieved", "err_feh_retrieved_single"]

df_aggregate = df_mean[cols_relevant]

df_aggregate["err_feh_retrieved_stdev"] = df_stdev.values

pd.set_option('display.max_rows', 1000)

print("---------")
print("feh_retrieved: average Fe/H across all spectra for that star")
print("err_feh_retrieved_single: average error in Fe/H across all spectra for that star (i.e., random error)")
print("err_feh_retrieved_stdev: error term from scatter in Fe/H between spectra of the same star (i.e., accounts for systematic differences between spectra")
print("---------")
print(df_aggregate)

file_name = 'junk_aggregate_retrieved.csv'
df_aggregate.to_csv(file_name)
print('Wrote',file_name)
