#!/usr/bin/env python
# coding: utf-8

# Takes LAMOST spectra compares retrievals between rrlfe and from the catalog in
# Table 6 of Liu+ 2020 ApJSS 247:68 'Probing the Galactic Halo with RR Lyrae Stars. I. The Catalog'.

# Created 2023 Jan. 5 by E.S.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from astropy.io import fits
import os

# catalog_liu_et_al.txt: Liu+ retrievals from LAMOST spectra
# lamost_li_file_info.csv: names of LAMOST spectra as downloaded; [file_name,ra,dec,emp_snr]

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read in Liu+ catalog
df_liu_stars = pd.read_csv(stem + "notebooks_for_development/spec_sets_check/lamost/catalog_liu_et_al.txt",
                              skiprows=65, delim_whitespace=True, usecols=[0,1,2,11,12,13,14,31],
                               names=["ID","RAdeg","DEdeg","VType","SNR","FeH","e_FeH","Num"])

# read in our retrieved Fe/H for LAMOST spectra and splice stuff to enable matching
df_our_data = pd.read_csv(stem + "bin/20230120_all_spectra_retrieved_vals.csv")

# standalone (for notebook): make table of spectrum names and their RA, DEC from FITS headers
'''
fits_dir = stem + "notebooks_for_development/spec_sets_check/lamost/spectra/"
fits_file_names = glob.glob(fits_dir + "*fits")
init_array = np.zeros((len(fits_file_names),1), dtype=float)

# initialize DataFrame
df_lamost_specs_ra_dec = pd.DataFrame(fits_file_names, columns=["file_name"])
df_lamost_specs_ra_dec["ra"] = init_array
df_lamost_specs_ra_dec["dec"] = init_array

for file_num in range(0, len(fits_file_names)):

    print(file_num)

    hdul = fits.open(fits_file_names[file_num])

    df_lamost_specs_ra_dec["file_name"].loc[file_num] = os.path.basename(fits_file_names[file_num])
    df_lamost_specs_ra_dec["ra"].loc[file_num] = hdul[0].header["RA"]
    df_lamost_specs_ra_dec["dec"].loc[file_num] = hdul[0].header["DEC"]

df_lamost_specs_ra_dec.to_csv(stem + "notebooks_for_development/spec_sets_check/lamost/junk.csv", index=False)
'''

# retrieve LAMOST RA, DEC
df_lamost_specs_ra_dec = pd.read_csv(stem + "notebooks_for_development/spec_sets_check/lamost/spectra_ra_dec.csv")

# give some cols same name, so we can merge on them
df_liu_stars["ra"] = df_liu_stars["RAdeg"]
df_liu_stars["dec"] = df_liu_stars["DEdeg"]

# some rounding is necessary to enable matching
df_liu_stars["ra_round"] = np.round(df_liu_stars["ra"],3)
df_lamost_specs_ra_dec["ra_round"] = np.round(df_lamost_specs_ra_dec["ra"],3)
df_liu_stars["dec_round"] = np.round(df_liu_stars["dec"],3)
df_lamost_specs_ra_dec["dec_round"] = np.round(df_lamost_specs_ra_dec["dec"],3)

# this merges tables based on RA, DEC, and leaves the Liu FeH in the final table
# (but our FeH is still missing)
merged_df_liu_feh = pd.merge(df_liu_stars, df_lamost_specs_ra_dec, how="inner", on=["ra_round","dec_round"])

# for clarity
merged_df_liu_feh["feh_liu"] = merged_df_liu_feh["FeH"]

# some info
print("Number of stars in Liu:",len(df_liu_stars.drop_duplicates()))
print("Number of LAMOST spectra:",len(df_lamost_specs_ra_dec.drop_duplicates()))
print("Number of Liu-LAMOST matches:",len(merged_df_liu_feh.drop_duplicates()))

# now read in our own retrievals, and merge with the above by file name
df_lamost_rrlfe_retrievals = pd.read_csv(stem + "/bin/20230120_all_spectra_retrieved_vals.csv")

# for clarity
df_lamost_rrlfe_retrievals["feh_rrlfe"] = df_lamost_rrlfe_retrievals["feh_retrieved"]

# for matching
merged_df_liu_feh["match_name"] = merged_df_liu_feh["file_name"].str.split(".",1).str[0]
df_lamost_rrlfe_retrievals["match_name"] = df_lamost_rrlfe_retrievals["orig_spec_file_name"].str.split(".",1).str[0]

# merge our retrievals onto Liu etc.
merged_df_liu_rrlfe = pd.merge(merged_df_liu_feh, df_lamost_rrlfe_retrievals, how="inner", on=["match_name"])

# drop rows with '-999' retrievals in Liu
liu_bad = merged_df_liu_rrlfe["feh_liu"] < -900
print("Unphysical Liu values:",np.sum(liu_bad))
merged_df_liu_rrlfe_good_liu = merged_df_liu_rrlfe.drop(merged_df_liu_rrlfe.loc[merged_df_liu_rrlfe["feh_liu"] < -900].index, inplace=False)

# drop rows with '> 50' retrievals from rrlfe (there was only 1 when I did this)
rrlfe_bad = merged_df_liu_rrlfe_good_liu["feh_rrlfe"] > 50
print("Unphysical rrlfe values:",np.sum(rrlfe_bad))
merged_df_liu_rrlfe_good_all = merged_df_liu_rrlfe_good_liu.drop(merged_df_liu_rrlfe_good_liu.loc[merged_df_liu_rrlfe_good_liu["feh_rrlfe"] > 50].index, inplace=False)

# drop any remaining NaN values
merged_df_liu_rrlfe_good_all = merged_df_liu_rrlfe_good_all[merged_df_liu_rrlfe_good_all["feh_rrlfe"].notna()]

# find best fit, using non-NaN values
coeffs_poly = np.polyfit(merged_df_liu_rrlfe_good_all["feh_liu"], merged_df_liu_rrlfe_good_all["feh_rrlfe"], deg=1)

print("Coeffs of best fit:",coeffs_poly)

plt.scatter(merged_df_liu_rrlfe_good_all["feh_liu"],merged_df_liu_rrlfe_good_all["feh_rrlfe"], alpha=0.2)
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
merged_df_liu_rrlfe_good_all.to_csv(text_file_name, columns = header, index=False)
print("Wrote",text_file_name)

'''
# check to see if data points along vertical lines represent multiple single-epoch spectra
# answer: no! they're different stars
np.sum(merged_df_liu_rrlfe_good_all["feh_liu"] == -2.2)
df_liu_stars.where(df_liu_stars["FeH"] == -2.2).dropna()
'''
