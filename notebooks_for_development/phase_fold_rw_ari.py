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
file_name_photometry_input = stem + "data/phase_folded_curves/Phased_RW_Ari.dat"
file_name_trendline = stem + "data/phase_folded_curves/LC_RW_Ari.cur_0.spl"
epoch_max = 2459459.500605 # NDL 2022_05_31
period_input =  0.354311408662876 # NDL 2022_05_31

# read in photometry and spline fits
'''
# for KELT photometry in bjd and mag units
df_test2 = pd.read_csv(file_name_photometry_input,
                       names=["bjd","mag","error"], delim_whitespace=True)

# phase-folded data
#df_test2["epoch_start_zero"] = np.subtract(df_test2["bjd"],np.min(df_test2["bjd"]))
df_test2["epoch_start_zero"] = np.subtract(df_test2["bjd"],epoch_max)
df_test2["baseline_div_period"] = np.divide(df_test2["epoch_start_zero"],period_input)
df_phase_folded = pd.DataFrame(data = [t%1. for t in df_test2["baseline_div_period"]], columns=["phase"])
df_phase_folded["mag"] = df_test2["mag"]
df_spline = pd.read_csv(file_name_trendline, names=["phase","mag"], delimiter=",", skiprows=1)
'''
#'''
# for TESS photometry in phase and flux units
df_spline = pd.read_csv(file_name_trendline, names=["phase","flux"], delimiter=",", skiprows=1)
df_spline["mag"] = -2.5*np.log10(np.divide(df_spline["flux"],np.max(df_spline["flux"])))

df_test2 = pd.read_csv(file_name_photometry_input, names=["phase","flux"], delim_whitespace=True)
df_test2["mag"] = -2.5*np.log10(np.divide(df_test2["flux"],np.max(df_spline["flux"])))
df_phase_folded = pd.DataFrame(data = df_test2["phase"], columns=["phase"])
df_phase_folded["mag"] = df_test2["mag"]

#'''

import ipdb; ipdb.set_trace()

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
