#!/usr/bin/env python
# coding: utf-8

# This reads in a list of file names and phases, and a file output by the pipeline
# which includes calculated Teff, and plots them.

# Created 2021 Nov. 18 by E.S.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# phases
df_phases = pd.read_csv(stem + "/src/mcd_final_phases_ascii_files_all.list")

# retrieved values
df_teff = pd.read_csv(stem + "rrlfe_io_20220803_01/bin/retrieved_vals_20220803.csv")

# merge by spectrum name
df_net = pd.merge(df_phases, df_teff, on=["orig_spec_file_name","orig_spec_file_name"])

# add column for star name
df_net["star_name_temp"] = df_net["orig_spec_file_name"].str.split(".").str[0]
df_net["star_name"] = df_net["star_name_temp"].str[:6]

# sort by phase to make the line plot work right
df_net.sort_values("phase", inplace=True)

star_name_array = df_net["star_name"].drop_duplicates().tolist()

i=1
idx = df_net.index[df_net["star_name"] == star_name_array[i]].tolist()

plt.clf()
plt.figure(figsize=(12,7))
for i in range(0,len(star_name_array)):
    print("---")
    print(i)
    print(star_name_array[i])
    idx = df_net.index[df_net["star_name"] == star_name_array[i]].tolist()
    # determine subtype for plot
    if df_net["subtype"][idx[0]] == "ab":
        linestyle = "-"
    elif df_net["subtype"][idx[0]] == "c":
        linestyle = "--"
    # marker fill/nofill to avoid repeat
    if i<=9:
        fill_style="full"
    else:
        fill_style="none"
    plt.plot(df_net["phase"][idx], df_net["teff_retrieved"][idx], marker='o',
             markersize=5, fillstyle=fill_style, linestyle=linestyle, label=star_name_array[i].replace("_"," "))

plt.ylabel("Retrieved Teff", fontsize=25)
plt.xlabel("Phase", fontsize=25)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(ncol=1, fontsize=15, bbox_to_anchor=(1.2, 1.0))
plt.tight_layout()

file_name_write = "junk.pdf"
plt.savefig(file_name_write)
print("Wrote", file_name_write)
