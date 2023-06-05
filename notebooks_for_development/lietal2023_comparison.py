#!/usr/bin/env python
# coding: utf-8

# Takes lietal2023 spectra compares retrievals between rrlfe and from the catalog in
# Table 6 of Liu+ 2020 ApJSS 247:68 'Probing the Galactic Halo with RR Lyrae Stars. I. The Catalog'.

# Created 2023 Jan. 5 by E.S.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from astropy.io import fits
import os

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read in Liu+ catalog
# note we need to use col '[Fe/H]_PHOT', NOT '[Fe/H]', based on comparisons with machine-readable file posted on https://zenodo.org/record/7471144
df_lietal2023_stars = pd.read_csv(stem + "notebooks_for_development/data/RRLyraes_final_lietal_beers_2023apr.csv",
                              usecols=["source_id", "R.A.", "Decl.","[Fe/H]_PHOT"]) 

# read in our retrieved Fe/H for SDSS spectra and splice stuff to enable matching
#df_our_data = pd.read_csv(stem + "bin/20230120_all_spectra_retrieved_vals.csv")
df_our_data = pd.read_csv(stem + "notebooks_for_development/data/retrieved_lietal2023_vals_corrected_20230605.csv")

# retrieve RA, DEC of stars from their FITS files
# (see lietal2023_make_ra_dec_table.ipynb)
df_lietal2023_specs_ra_dec = pd.read_csv(stem + "notebooks_for_development/data/sdss_spectra_radec_overlap_w_lietal2023.csv")

# give some cols same name, so we can merge on them
df_lietal2023_stars["ra"] = df_lietal2023_stars["R.A."]
df_lietal2023_stars["dec"] = df_lietal2023_stars["Decl."]

# get obj_id strings so that we can merge file names with RA, DEC, and retrievals
df_our_data['obj_id_name_match'] = df_our_data['orig_spec_file_name'].str.split('_g',expand=True)[0]
df_lietal2023_specs_ra_dec['obj_id_name_match'] = df_lietal2023_specs_ra_dec['file_name'].str.split('.',expand=True)[0]

# merge (based on obj_id) to get our retrievals, with RA and DEC info
df_our_data_w_ra_dec = df_our_data.merge(df_lietal2023_specs_ra_dec, on='obj_id_name_match', how='inner')

# some rounding is necessary to enable matching

df_lietal2023_stars["ra_round"] = np.round(df_lietal2023_stars["ra"],3)
df_our_data_w_ra_dec["ra_round"] = np.round(df_our_data_w_ra_dec["ra"],3)
df_lietal2023_stars["dec_round"] = np.round(df_lietal2023_stars["dec"],3)
df_our_data_w_ra_dec["dec_round"] = np.round(df_our_data_w_ra_dec["dec"],3)
'''
df_lietal2023_stars["ra_round"] = np.round(df_lietal2023_stars["ra"],2)
df_our_data_w_ra_dec["ra_round"] = np.round(df_our_data_w_ra_dec["ra"],2)
df_lietal2023_stars["dec_round"] = np.round(df_lietal2023_stars["dec"],2)
df_our_data_w_ra_dec["dec_round"] = np.round(df_our_data_w_ra_dec["dec"],2)
'''
# this merges tables based on RA, DEC, and leaves the Liu FeH in the final table
# (but our FeH is still missing)
merged_df_lietal2023_feh = pd.merge(df_our_data_w_ra_dec, df_lietal2023_stars, how="inner", on=["ra_round","dec_round"])
import ipdb; ipdb.set_trace()
# for clarity
merged_df_lietal2023_feh["feh_liu"] = merged_df_lietal2023_feh["FeH"]

# some info
print("Number of stars in Liu:",len(df_lietal2023_stars.drop_duplicates()))
print("Number of lietal2023 spectra:",len(df_lietal2023_specs_ra_dec.drop_duplicates()))
print("Number of Liu-lietal2023 matches:",len(merged_df_lietal2023_feh.drop_duplicates()))

# now read in our own retrievals, and merge with the above by file name
df_lietal2023_rrlfe_retrievals = pd.read_csv(stem + "/bin/20230120_all_spectra_retrieved_vals.csv")

# for clarity
df_lietal2023_rrlfe_retrievals["feh_rrlfe"] = df_lietal2023_rrlfe_retrievals["feh_retrieved"]

# for matching
merged_df_lietal2023_feh["match_name"] = merged_df_lietal2023_feh["file_name"].str.split(".",1).str[0]
df_lietal2023_rrlfe_retrievals["match_name"] = df_lietal2023_rrlfe_retrievals["orig_spec_file_name"].str.split(".",1).str[0]

# merge our retrievals onto Liu etc.
merged_df_lietal2023_rrlfe = pd.merge(merged_df_lietal2023_feh, df_lietal2023_rrlfe_retrievals, how="inner", on=["match_name"])

# drop rows with '-999' retrievals in Liu
lietal2023_bad = merged_df_lietal2023_rrlfe["feh_liu"] < -900
print("Unphysical Liu values:",np.sum(lietal2023_bad))
merged_df_lietal2023_rrlfe_good_liu = merged_df_lietal2023_rrlfe.drop(merged_df_lietal2023_rrlfe.loc[merged_df_lietal2023_rrlfe["feh_liu"] < -900].index, inplace=False)

# drop rows with '> 50' retrievals from rrlfe (there was only 1 when I did this)
rrlfe_bad = merged_df_lietal2023_rrlfe_good_liu["feh_rrlfe"] > 50
print("Unphysical rrlfe values:",np.sum(rrlfe_bad))
merged_df_lietal2023_rrlfe_good_all = merged_df_lietal2023_rrlfe_good_liu.drop(merged_df_lietal2023_rrlfe_good_liu.loc[merged_df_lietal2023_rrlfe_good_liu["feh_rrlfe"] > 50].index, inplace=False)

# drop any remaining NaN values
merged_df_lietal2023_rrlfe_good_all = merged_df_lietal2023_rrlfe_good_all[merged_df_lietal2023_rrlfe_good_all["feh_rrlfe"].notna()]

# find best fit, using non-NaN values
coeffs_poly = np.polyfit(merged_df_lietal2023_rrlfe_good_all["feh_liu"], merged_df_lietal2023_rrlfe_good_all["feh_rrlfe"], deg=1)

print("Coeffs of best fit:",coeffs_poly)

plt.scatter(merged_df_lietal2023_rrlfe_good_all["feh_liu"],merged_df_lietal2023_rrlfe_good_all["feh_rrlfe"], alpha=0.2)
plt.plot([-4.0,4.0],np.add(np.multiply(coeffs_poly[0],[-4.0,4.0]),coeffs_poly[1]),color="k", label="best fit")
plt.plot([-4.0,4.0],[-4.0,4.0], linestyle="--", color="grey", label="1-to-1")
plt.ylabel("[Fe/H], rrlfe")
plt.xlabel("[Fe/H], Liu+")
plt.legend()
file_name_placeholder = "junk.png"
plt.savefig("junk.png")

print("Wrote " + file_name_placeholder)

# write out data as csvs (rename cols for clarity)
text_file_name = "junk_liu.csv"
header = ["feh_liu", "feh_rrlfe"]
merged_df_lietal2023_rrlfe_good_all.to_csv(text_file_name, columns = header, index=False)
print("Wrote",text_file_name)

'''
# check to see if data points along vertical lines represent multiple single-epoch spectra
# answer: no! they're different stars
np.sum(merged_df_lietal2023_rrlfe_good_all["feh_liu"] == -2.2)
df_lietal2023_stars.where(df_lietal2023_stars["FeH"] == -2.2).dropna()
'''
