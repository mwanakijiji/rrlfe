#!/usr/bin/env python
# coding: utf-8

# This is to compare with the catalog of Whitten+, as sent by T. Beers on Nov. 26

# Created 2023 Jan. 3 by E.S.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read in Whitten+ retrievals
df_whitten_stars = pd.read_csv("./data/SPLUS_STRIPE82_ebv_retrain.csv")

# read in our retrieved Fe/H
#df_our_data = pd.read_csv(stem + "rrlfe_io_20221220_sdss_test/bin/retrieved_vals.csv")
#df_our_data = pd.read_csv(stem + "notebooks_for_development/data/retrieved_sdss_20221213_cosmic_rays_removed_automated_3911_to_4950_angstr_vals_corrected.csv")
#df_our_data = pd.read_csv(stem + "notebooks_for_development/data/retrieved_catalina_20230515_vals_corrected.csv")
df_our_data = pd.read_csv(stem + "notebooks_for_development/data/retrieved_sdss_20230514_corrected.csv")

# read in S/N of SDSS spectra 
df_s2n = pd.read_csv(stem + "notebooks_for_development/data/s_to_n_sdss_spectra_cosmic_rays_removed_automated_3911_to_4950_angstr.csv")

df_our_data['file_name_s2n_match'] = df_our_data["orig_spec_file_name"].str.split("_net", 0, expand=True)[0]
df_s2n['file_name_s2n_match'] = df_s2n['file_name'].str.split("_net", 0, expand=True)[0]

# merge
df_our_data = df_our_data.merge(df_s2n, on='file_name_s2n_match', how='inner')

# intermediate functionality to read in our SDSS star IDs, remove repeats, and write back out
# so that they can be fed into SDSS SkyServer
'''
#
df_mine = pd.read_csv(stem + "notebooks_for_development/data/spalding_sdss_spectra_for_xmatch_norepeats.csv", delim_whitespace=True)
df_mine_no_repeats = df_mine.drop_duplicates()
df_mine_no_repeats.to_csv(stem + "notebooks_for_development/data/spalding_sdss_spectra_for_xmatch_norepeats.csv", sep=" ", index=False)
df_mine_no_repeats = pd.read_csv(stem + "notebooks_for_development/data/spalding_sdss_spectra_for_xmatch_norepeats.csv", delim_whitespace=True)
'''

# read in RA, DEC info for our stars, as returned by SDSS SkyServer
df_our_sdss_stars = pd.read_csv(stem + "notebooks_for_development/data/Skyserver_CrossID1_4_2023_5_21_47_AM.csv")

# give some cols same name, so we can merge on them
df_whitten_stars["ra"] = df_whitten_stars["RA"]
df_whitten_stars["dec"] = df_whitten_stars["Dec"]

# some rounding is necessary to enable matching
df_whitten_stars["ra_round"] = np.round(df_whitten_stars["ra"],3)
df_our_sdss_stars["ra_round"] = np.round(df_our_sdss_stars["ra"],3)
df_whitten_stars["dec_round"] = np.round(df_whitten_stars["dec"],3)
df_our_sdss_stars["dec_round"] = np.round(df_our_sdss_stars["dec"],3)

# this merges tables based on RA, DEC, and leaves the Whitten FeH in the final table
# (but our FeH is still missing)
merged_df_whitten_feh = pd.merge(df_whitten_stars, df_our_sdss_stars, how="inner", on=["ra_round","dec_round"])

# take out list of retrieved Fe/H and splice stuff to enable matching
split_1 = df_our_data["orig_spec_file_name"].str.split("-", 3, expand=True)
split_2 = split_1[3].str.split("_", 1, expand=True)
df_our_data["plate"] = split_1[1].astype(int)
df_our_data["mjd"] = split_1[2].astype(int)
df_our_data["fiberid"] = split_2[0].astype(int)

# our stars can have multiple FeHs, because of multiple epochs
# (an 'inner' merge in this context means that repeats are allowed, but any rows with NaNs
# left in either FeH column is removed)
merged_df_whitten_and_our_feh = pd.merge(df_our_data, merged_df_whitten_feh, on=["plate", "mjd", "fiberid"],
                                         how="inner")

# drop any remaining NaN values
merged_df_whitten_and_our_feh = merged_df_whitten_and_our_feh[merged_df_whitten_and_our_feh["feh_retrieved"].notna()]
# drop repeats
merged_df_whitten_and_our_feh = merged_df_whitten_and_our_feh.drop_duplicates()
# drop S/N < 10
merged_df_whitten_and_our_feh = merged_df_whitten_and_our_feh.where(merged_df_whitten_and_our_feh['s_to_n']>10.)

# to see S/N
#plt.scatter(merged_df_whitten_and_our_feh["NET_FEH"],merged_df_whitten_and_our_feh["feh_retrieved"],c = merged_df_whitten_and_our_feh["s_to_n"], cmap="viridis")

# best-fit coefficients, where vals are sane (-4.0 to 1.0)
idx_sane_whitten = np.logical_and(merged_df_whitten_and_our_feh["NET_FEH"] > -4.0, merged_df_whitten_and_our_feh["NET_FEH"]<1.0)
idx_sane_rrlfe = np.logical_and(merged_df_whitten_and_our_feh["feh_retrieved"] > -4.0, merged_df_whitten_and_our_feh["feh_retrieved"]<1.0)
idx_sane = np.logical_and(idx_sane_whitten,idx_sane_rrlfe)
coeffs_poly = np.polyfit(merged_df_whitten_and_our_feh["NET_FEH"].loc[idx_sane],merged_df_whitten_and_our_feh["feh_retrieved"].loc[idx_sane], deg=1)
print("Coeffs:")
print(coeffs_poly)

plot_file_name = "junk_whitten.png"
plt.plot([-4.0,4.0],[-4.0,4.0], linestyle="--", color="gray", zorder=0)
plt.scatter(merged_df_whitten_and_our_feh["NET_FEH"],merged_df_whitten_and_our_feh["feh_retrieved"],s=10,color="k")
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.ylabel("[Fe/H], rrlfe")
plt.xlabel("[Fe/H], Whitten+")
plt.savefig(plot_file_name)
print("Wrote",plot_file_name)

# write out data as csvs (rename cols for clarity)
text_file_name = "junk_whitten.csv"
merged_df_whitten_and_our_feh.rename(
    columns=({ "NET_FEH": "feh_whitten", "feh_retrieved": "feh_rrlfe"}), 
    inplace=True,
)
header = ["feh_whitten", "feh_rrlfe", "s_to_n"]
merged_df_whitten_and_our_feh.to_csv(text_file_name, columns = header, index=False)
print("Wrote",text_file_name)