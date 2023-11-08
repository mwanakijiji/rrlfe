#!/usr/bin/env python
# coding: utf-8

# Plots SSPP output from Young Sun

# Created 2022 Nov. 21 by E.S.

import pandas as pd
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read in our values
df_retrieved = pd.read_csv(stem + "notebooks_for_development/data/sspp_rrlfe_comparison_sdss_single_epoch_20231108/retrieved_vals_corrected_sdss_single_epoch_20231108.csv")

import ipdb; ipdb.set_trace()

## SINGLE-EPOCH spectra
df_sspp_singleepoch = pd.read_csv(stem + "notebooks_for_development/data/sspp_rrlfe_comparison_sdss_single_epoch_20231108/young_sun_single_epoch/ssppOut-RRL_all.csv", usecols=[1,8,65,67,173,175],
                 names=["coadded_spec_name","TEFF_ADOP","FEH_ADOP","FEH_ADOP_UNC","FEH_SPEC","FEH_SPEC_UNC"])
df_sspp_singleepoch["name_match_single_epoch"] = df_sspp_singleepoch["coadded_spec_name"]
df_sspp_singleepoch["name_match_single_epoch"] = df_sspp_singleepoch["name_match_single_epoch"].str.strip()
# make columns for merging
df_retrieved["junk0"] = df_retrieved["orig_spec_file_name"].str.split(pat="spec-", expand=True)[1]
df_retrieved["junk1"] = df_retrieved["junk0"].str.split(pat=".dat", expand=True)[0]
df_retrieved["name_match_single_epoch"] = df_retrieved["junk1"].str.replace(r"g", "")
df_merged = df_retrieved.merge(df_sspp_singleepoch, on="name_match_single_epoch", how="outer", indicator=True)

import ipdb; ipdb.set_trace()
# separate out plate, mjd, fiberid for obtaining S/N from SDSS website
# ref. https://dr17.sdss.org/optical/spectrum/search
df_merged['plate'] = df_merged['orig_spec_file_name'].str.split('-', expand=True)[1]
df_merged['mjd'] = df_merged['orig_spec_file_name'].str.split('-', expand=True)[2]
df_merged['fiberid'] = df_merged['orig_spec_file_name'].str.split('-', expand=True)[3].str.split('g',expand=True)[0]
header = ["plate", "mjd", "fiberid"]
file_name_1 = "junk_coadded_plate_mjd_fiberid.csv"
df_merged.to_csv(file_name_1, columns = header, index=False)
print("Wrote",file_name_1)
import ipdb; ipdb.set_trace()

# plot: single-epoch spectra
plt.clf()
plt.figure(figsize=(10,5))
plt.plot([-4.0,0.5],[-4.0,0.5], linestyle="--", color="black", zorder=0) # one-to-one
# if we want to compare Feh
plt.scatter(df_merged["FEH_ADOP"], df_merged["feh_retrieved"],
            c=df_merged["TEFF_ADOP"], cmap="Greens", s=20, alpha=1.0, label="Teff", edgecolors="k")
plt.xlabel("[Fe/H], SSPP (single epoch)", fontsize=25)
plt.ylabel("[Fe/H], rrlfe (single epoch)", fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#plt.xlim(-4.,0.5)
#plt.ylim(-4.,0.5)
cbar = plt.colorbar()
cbar.set_label("Teff",fontsize=20)
cbar.ax.tick_params(labelsize=20)
plt.tight_layout()
file_name_write_feh = "junk_single_epoch.pdf"
plt.savefig(file_name_write_feh)
print("Wrote",file_name_write_feh)

'''
# if we want to compare retrieved Teffs
plt.scatter(df_merged_1["teff"], df_merged_1["teff_retrieved"],
            c=df_merged_1["s_to_n"], cmap="Greens", s=50, edgecolors="k")
'''

# hexplot of all RRLs: single epoch
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged["FEH_ADOP"] # idx_finite, idx_sane, idx_sane
y = df_merged["feh_retrieved"]
hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.plot([-3.5,0.5],[-3.5,0.5], linestyle="--", color="white", zorder=1, label="1-to-1")
plt.title("Hexbin of RRabs and RRcs, single epoch spectra as run by Young Sun")
ax.set_xlabel("Fe/H, nSSPP")
ax.set_ylabel("Fe/H, rrlfe")
ax.set_xlim([-3.5,0.5])
ax.set_ylim([-3.5,0.5])
cb = fig.colorbar(hb, ax=ax)
cb.set_label('counts')
fig.legend()
file_name_write_feh2 = "junk_all_hex_young_single_epoch.png"
plt.savefig(file_name_write_feh2)
print("Wrote",file_name_write_feh2)

# write out data as csvs (rename cols for clarity)
import ipdb; ipdb.set_trace()
text_file_name = "junk_single.csv"
df_merged.rename(
    columns=({ "FEH_ADOP": "feh_sspp_single", "FEH_ADOP_UNC": "error_feh_sspp_single", "feh_corrected": "feh_rrlfe_single", "err_feh_retrieved": "error_feh_rrlfe_single"}), 
    inplace=True,
)
header = ["orig_spec_file_name", "plate", "mjd", "fiberid", "feh_sspp_single", "error_feh_sspp_single", "feh_rrlfe_single", "error_feh_rrlfe_single"]
df_merged.to_csv(text_file_name, columns = header, index=False)
print("Wrote",text_file_name)
import ipdb; ipdb.set_trace()