#!/usr/bin/env python
# coding: utf-8

# This populates a pipeline input file with the final phases of our McD spectra

# Created 2022 Aug. 3 by E.S.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# input file template (will not be overwritten) and phase data
input_template = "/src/mcd_beta_phases_ascii_files_all_v2.list"
table_final_phases = "/notebooks_for_development/data/phases_all_master_no_repeat_fits.csv"
df_input = pd.read_csv(stem + input_template)
df_phases = pd.read_csv(stem + table_final_phases)

# change 'fits' to 'dat' (necessary for matching)
df_phases["orig_spec_file_name"] = df_phases["file"].str.replace("fits","dat")

# merge
df_merged = df_input.merge(df_phases, how="outer", on="orig_spec_file_name")

# get rid of unimportant stuff
cols_relevant = ["orig_spec_file_name","phase","my_phase","subtype","feh","err_feh"]
df_relevant = df_merged[cols_relevant]

'''
# to check

plt.scatter(df_relevant["phase"], df_relevant["my_phase"])
plt.show()
'''

# rename
df_relevant["phase"] = df_relevant["my_phase"]

# write
cols_2_write = ["orig_spec_file_name","subtype","phase","feh","err_feh"]
df_2_write = df_relevant[cols_2_write]

import ipdb; ipdb.set_trace()
df_2_write.to_csv("junk.csv", index=False)
