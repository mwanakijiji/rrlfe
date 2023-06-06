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
df_phases = pd.read_csv(stem + "/src/mcd_final_phases_ascii_files_all_pub_20230606.list")

# retrieved values
df_teff = pd.read_csv(stem + "notebooks_for_development/data/retrieved_mcd_incl_corrxn_20230606.csv")

# merge by spectrum name
df_net = pd.merge(df_phases, df_teff, on=["orig_spec_file_name","orig_spec_file_name"])

# add column for star name
df_net["star_name_temp"] = df_net["orig_spec_file_name"].str.split(".").str[0]
df_net["star_name"] = df_net["star_name_temp"].str[:6]

# sort by phase to make the line plot work right
df_net.sort_values("phase", inplace=True)

star_name_array = df_net["star_name"].drop_duplicates().tolist()
star_name_array.sort() # to make names alphabetical in legend

i=1
idx = df_net.index[df_net["star_name"] == star_name_array[i]].tolist()

plt.clf()
fig, ax = plt.subplots(3, 1, sharex=True, figsize=(11,7))
for i in range(0,len(star_name_array)):
    
    print("---")
    print(i)
    print(star_name_array[i])
    # find right star, and make sure retrieved Fe/H converged
    idx = df_net.index[np.logical_and(df_net["star_name"] == star_name_array[i],df_net["feh_retrieved"]>-10)].tolist()
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

    ax[0].plot(df_net["phase"][idx], df_net["teff_retrieved"][idx], marker='o',
             markersize=5, fillstyle=fill_style, linestyle=linestyle, label=star_name_array[i].replace("_"," "))
    '''
    ax[1].plot(df_net["phase"][idx], df_net["EW_Balmer"][idx], marker='o',
             markersize=5, fillstyle=fill_style, linestyle=linestyle, label=star_name_array[i].replace("_"," "))
    '''
    ax[1].plot(df_net["phase"][idx], df_net["EW_CaIIK"][idx], marker='o',
             markersize=5, fillstyle=fill_style, linestyle=linestyle, label=star_name_array[i].replace("_"," "))
    ax[2].plot(df_net["phase"][idx], df_net["feh_retrieved"][idx], marker='o',
             markersize=5, fillstyle=fill_style, linestyle=linestyle, label=star_name_array[i].replace("_"," "))

ax[0].set_ylabel("Retrieved Teff (K)", fontsize=15)
#ax[1].set_ylabel("Balmer EW ($\AA$)", fontsize=25)
ax[1].set_ylabel("Ca II K EW ($\AA$)", fontsize=15)
ax[2].set_ylabel("Retrieved [Fe/H]", fontsize=15)

ax[2].set_xlabel("Phase", fontsize=15)

ax[0].set_xlim([0.0,1.0])

#ax[2].set_xticks(fontsize=15)
#plt.yticks(fontsize=15)
plt.legend(ncol=1, fontsize=15, bbox_to_anchor=(1.21, 3.5))
plt.subplots_adjust(left=0.08, right=0.84, top=0.95, bottom=0.1)
#plt.tight_layout()

file_name_write = "junk.pdf"
plt.savefig(file_name_write)
print("Wrote", file_name_write)
