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
df_retrieved = pd.read_csv(stem + "notebooks_for_development/data/retrieved_catalina_20230515_vals_corrected.csv")

# SSPP values (from YSL)

## COADDED spectra
df_sspp = pd.read_csv(stem + "notebooks_for_development/data/NEWEST_SDSS_RRLYRAE_ECKHARD/coadded/ssppOut-RRLyae.param.csv", usecols=[1,8,65,67,173,175],
                 names=["coadded_spec_name","TEFF_ADOP","FEH_ADOP","FEH_ADOP_UNC","FEH_SPEC","FEH_SPEC_UNC"])
# make column for merging
df_sspp["name_match"] = df_sspp["coadded_spec_name"]
df_sspp["name_match"] = df_sspp["name_match"].str.strip()
df_retrieved["junk3"] = df_retrieved["orig_spec_file_name"].str.split(pat="g", expand=True)[0].str.split(pat="spec-", expand=True)[1]
df_retrieved["junk0"] = df_retrieved["orig_spec_file_name"].str.split(pat="-", expand=True)[0]
df_retrieved["junk1"] = df_retrieved["orig_spec_file_name"].str.split(pat="-", expand=True)[1]
df_retrieved["junk2"] = df_retrieved["orig_spec_file_name"].str.split(pat="-", expand=True)[2]
df_retrieved["junk3"] = df_retrieved["junk3"].str.split(pat="-", expand=True)[2].str[1:]
# make name_match col
df_retrieved["name_match"] = df_retrieved["junk1"]+"-"+df_retrieved["junk2"]+"-"+df_retrieved["junk3"]
df_merged = df_retrieved.merge(df_sspp, on="name_match", how="outer", indicator=True)
# remove crazy points
idx_sane = (np.isfinite(df_merged["FEH_ADOP"]) & np.isfinite(df_merged["feh_retrieved"])) & \
    ((np.abs(df_merged["feh_retrieved"]) < 5.) & (np.abs(df_merged["FEH_ADOP"]) < 5.))
# best-fit coeffs
coeffs = np.polyfit(df_merged["FEH_ADOP"][idx_sane], df_merged["feh_retrieved"][idx_sane], deg=1)

## SINGLE-EPOCH spectra
df_sspp_singleepoch = pd.read_csv(stem + "notebooks_for_development/data/NEWEST_SDSS_RRLYRAE_ECKHARD/single_epoch/ssppOut-RRL_all.param.csv", usecols=[1,8,65,67,173,175],
                 names=["coadded_spec_name","TEFF_ADOP","FEH_ADOP","FEH_ADOP_UNC","FEH_SPEC","FEH_SPEC_UNC"])
df_sspp_singleepoch["name_match_single_epoch"] = df_sspp_singleepoch["coadded_spec_name"]
df_sspp_singleepoch["name_match_single_epoch"] = df_sspp_singleepoch["name_match_single_epoch"].str.strip()
# make column for merging
df_retrieved["junk0"] = df_retrieved["orig_spec_file_name"].str.split(pat="spec-", expand=True)[1]
df_retrieved["junk1"] = df_retrieved["junk0"].str.split(pat=".dat", expand=True)[0]
df_retrieved["name_match_single_epoch"] = df_retrieved["junk1"].str.replace(r"g", "")
df_merged_single_epoch = df_retrieved.merge(df_sspp_singleepoch, on="name_match_single_epoch", how="outer", indicator=True)
# remove crazy points
idx_sane_single_epoch = (np.isfinite(df_merged_single_epoch["FEH_ADOP"]) & np.isfinite(df_merged_single_epoch["feh_retrieved"])) & \
    ((np.abs(df_merged_single_epoch["feh_retrieved"]) < 5.) & (np.abs(df_merged_single_epoch["FEH_ADOP"]) < 5.))
# best-fit coeffs
coeffs_single_epoch = np.polyfit(df_merged_single_epoch["FEH_ADOP"][idx_sane_single_epoch], df_merged_single_epoch["feh_retrieved"][idx_sane_single_epoch], deg=1)

print("coeffs, coadded", coeffs)
print("coeffs, single epoch", coeffs_single_epoch)

# plot: coadded spectra
plt.clf()
plt.figure(figsize=(10,5))
plt.plot([-4.0,0.5],[-4.0,0.5], linestyle="--", color="black", zorder=0) # one-to-one
# if we want to compare Feh
plt.scatter(df_merged["FEH_ADOP"][idx_sane], df_merged["feh_retrieved"][idx_sane],
            c=df_merged["TEFF_ADOP"][idx_sane], cmap="Greens", s=20, alpha=1.0, label="Teff", edgecolors="k")
plt.plot([-4.0,0.5],[coeffs[0]*(-4.0)+coeffs[1],coeffs[0]*(0.5)+coeffs[1]], linestyle="-", label="best-fit, RRabs and cs (coadded)", zorder=0) # line of best fit, both types
plt.xlabel("[Fe/H], SSPP (coadded spectra)", fontsize=25)
plt.ylabel("[Fe/H], rrlfe (single epoch)", fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#plt.xlim(-4.,0.5)
#plt.ylim(-4.,0.5)
cbar = plt.colorbar()
cbar.set_label("Teff",fontsize=20)
cbar.ax.tick_params(labelsize=20)
plt.tight_layout()
file_name_write_feh = "junk_coadded.pdf"
plt.savefig(file_name_write_feh)
print("Wrote",file_name_write_feh)

# plot: single-epoch spectra
plt.clf()
plt.figure(figsize=(10,5))
plt.plot([-4.0,0.5],[-4.0,0.5], linestyle="--", color="black", zorder=0) # one-to-one
# if we want to compare Feh
plt.scatter(df_merged_single_epoch["FEH_ADOP"][idx_sane_single_epoch], df_merged_single_epoch["feh_retrieved"][idx_sane_single_epoch],
            c=df_merged_single_epoch["TEFF_ADOP"][idx_sane_single_epoch], cmap="Greens", s=20, alpha=1.0, label="Teff", edgecolors="k")
plt.plot([-4.0,0.5],[coeffs_single_epoch[0]*(-4.0)+coeffs_single_epoch[1],coeffs_single_epoch[0]*(0.5)+coeffs_single_epoch[1]], linestyle="-", label="best-fit, RRabs and cs (single-epoch)", zorder=0) # line of best fit, both types
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

# hexplot of all RRLs: coadded
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged["FEH_ADOP"][idx_sane] # idx_finite, idx_sane, idx_sane
y = df_merged["feh_retrieved"][idx_sane]
hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.plot([-3.5,0.5],[-3.5,0.5], linestyle="--", color="white", zorder=1, label="1-to-1")
ax.plot([-3.0,0.0],[coeffs[0]*(-3.0)+coeffs[1],coeffs[0]*(0.0)+coeffs[1]], linestyle="-", color="k", zorder=1, label="best fit, all")
plt.title("Hexbin of RRabs and RRcs, coadded spectra as run by Young Sun")
ax.set_xlabel("Fe/H, nSSPP")
ax.set_ylabel("Fe/H, rrlfe")
ax.set_xlim([-3.5,0.5])
ax.set_ylim([-3.5,0.5])
cb = fig.colorbar(hb, ax=ax)
cb.set_label('counts')
fig.legend()
file_name_write_feh2 = "junk_all_hex_young_coadded.png"
plt.savefig(file_name_write_feh2)
print("Wrote",file_name_write_feh2)

# hexplot of all RRLs: single epoch
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged_single_epoch["FEH_ADOP"][idx_sane_single_epoch] # idx_finite, idx_sane, idx_sane
y = df_merged_single_epoch["feh_retrieved"][idx_sane_single_epoch]
hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.plot([-3.5,0.5],[-3.5,0.5], linestyle="--", color="white", zorder=1, label="1-to-1")
ax.plot([-3.0,0.0],[coeffs_single_epoch[0]*(-3.0)+coeffs_single_epoch[1],coeffs_single_epoch[0]*(0.0)+coeffs_single_epoch[1]], linestyle="-", color="k", zorder=1, label="best fit, all")
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
text_file_name = "junk_coadded.csv"
df_merged.rename(
    columns=({ "FEH_ADOP": "feh_sspp_coadded", "feh_retrieved": "feh_rrlfe"}), 
    inplace=True,
)
header = ["feh_sspp_coadded", "feh_rrlfe"]
df_merged.to_csv(text_file_name, columns = header, index=False)
print("Wrote",text_file_name)

text_file_name = "junk_single.csv"
df_merged_single_epoch.rename(
    columns=({ "FEH_ADOP": "feh_sspp_single", "feh_retrieved": "feh_rrlfe"}), 
    inplace=True,
)
header = ["feh_sspp_single", "feh_rrlfe"]
df_merged_single_epoch.to_csv(text_file_name, columns = header, index=False)
print("Wrote",text_file_name)