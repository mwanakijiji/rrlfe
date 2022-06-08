#!/usr/bin/env python
# coding: utf-8

# Reads in photometry from different sources, normalizes them, and puts them
# onto a BJD time scale

# Created 2021 Dec. 28 by E.S.

import numpy as np
import pandas as pd
from astropy.time import Time
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

stem = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/"
file_name_photometry_input = stem + "data/kelt_raw_photom/RU_Psc_E_small.cur"
file_name_trendline = stem + "data/phase_folded_curves/RU_Psc_E_small.cur_0.spl"
epoch_max = 2456410.378276
period_input = 0.390247669956971 # NDL email June 1 2022

# read in photometry and spline fits
df_test2 = pd.read_csv(file_name_photometry_input,
                       names=["jd","mag","error"], delim_whitespace=True)
df_spline = pd.read_csv(file_name_trendline, names=["phase","mag"], delimiter=",", skiprows=1)


# phase-folded data
#df_test2["epoch_start_zero"] = np.subtract(df_test2["jd"],np.min(df_test2["jd"]))
df_test2["epoch_start_zero"] = np.subtract(df_test2["jd"],epoch_max)
df_test2["baseline_div_period"] = np.divide(df_test2["epoch_start_zero"],period_input)
df_phase_folded = pd.DataFrame(data = [t%1. for t in df_test2["baseline_div_period"]], columns=["phase"])

df_phase_folded["mag"] = df_test2["mag"]

# merge
df_merged = df_phase_folded.merge(df_spline, how="outer", on="phase", suffixes=("_photom","_spline"))

# find where maximum is, and set the phase there to be zero
'''
idx_max = df_phase_folded["mag"] == np.min(df_phase_folded["mag"])
df_phase_folded["phase"] = np.mod(np.subtract(df_phase_folded["phase"],df_phase_folded["phase"].loc[idx_max].values),1.)
'''

# quick plot
plt.clf()
plt.scatter(df_phase_folded["phase"], df_phase_folded["mag"], s=2)
plt.scatter(df_spline["phase"], df_spline["mag"], s=2)
plt.xlim(0.,1.)
#plt.title("Phase-folded curve using ")
plt.gca().invert_yaxis()
plt.show()

# write out
import ipdb; ipdb.set_trace()
file_name_out = "./data/phase_folded_curves/junk.csv"
df_merged.to_csv(file_name_out)
print("Wrote ", file_name_out)
