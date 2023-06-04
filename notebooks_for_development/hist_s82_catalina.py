#!/usr/bin/env python
# coding: utf-8

# Makes histograms of Strip 82 retrieved Fe/H

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix

stem = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/"
file_name = "retrieved_sdss_20221213_cosmic_rays_removed_automated_3911_to_4950_angstr_vals_corrected.csv"

df_retrievals = pd.read_csv(stem + file_name)

# read in data including RRL types
col_names = ["SDSSname", "hjd", "Sesar phase", "Sesar cycles", "period", "g ephemeris", 
             "g amplitude", "Sesar type", "Drake phase", "Drake cycles", "Drake period", 
             "Drake V ephemeris", "Drake V amp", "Drake type", "Drake2013b chart period", 
             "Drake2013b chart amp", "Drake2013b chart type", "Abbas2014 period", "Abbas2014 amp", 
             "Abbas2014 type", "Catalina DR2 chart period", 
             "Catalina DR2 chart amp", "Catalina DR2 chart type", "Drake MLS chart period", 
             "Drake MLS chart amp", "Drake MLS chart type"]

# RW: phaseampgroupstype -- This is Stacy's final table of all the SDSS RRL variables. 
df_types = pd.read_csv("./data/phaseampgroupstype_modified.dat", names=col_names, delim_whitespace=True)

df_types["orig_spec_file_name"] = df_types["SDSSname"]

# for matching, remove underscores and extension bits
df_retrievals['name_match'] = df_retrievals['orig_spec_file_name'].str.replace('_', '').str.replace('net.csv', '')

df_types['name_match'] = df_types['orig_spec_file_name'].str.replace('.dat', '')

data_ensemble = df_retrievals.merge(df_types,how="inner",on="name_match")

# those that converged

idx_sane = data_ensemble["feh_retrieved"] > -900

matplotlib.rcParams.update({'font.size': 14})

# hist separating the types

'''
plt.hist(data_ensemble["feh_retrieved"].where(idx_ab), bins=100, label="RRabs")
plt.hist(data_ensemble["feh_retrieved"].where(idx_c), bins=100, label="RRcs", alpha=0.5)
plt.title("SDSS stars")
plt.xlabel("Retrieved [Fe/H]")
plt.legend()
plt.show()
'''

# simple hist
file_name_write = 'junk.pdf'
plt.clf()
plt.figure(figsize=(6,3))
plt.hist(data_ensemble["feh_retrieved"].where(idx_sane), bins=500)
plt.tight_layout(pad=1.5)
plt.xlim([-3.5,1.])
plt.xlabel("Retrieved [Fe/H]")
plt.savefig(file_name_write)
print('Wrote',file_name_write)