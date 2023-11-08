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
df_liu_stars = pd.read_csv(stem + "notebooks_for_development/data/liu_etal_2020_lamost_rrlfe_comparison_20231108/catalog_liu_et_al_2020_lamost.txt",
                              skiprows=65, delim_whitespace=True, usecols=[0,1,2,11,12,13,14,31],
                               names=["ID","RAdeg","DEdeg","VType","SNR","FeH","e_FeH","Num"])

# read in our retrieved Fe/H for LAMOST spectra and splice stuff to enable matching
#df_our_data = pd.read_csv(stem + "bin/20230120_all_spectra_retrieved_vals.csv")
df_our_data = pd.read_csv(stem + "notebooks_for_development/data/liu_etal_2020_lamost_rrlfe_comparison_20231108/retrieved_vals_corrected_liu_etal_2020_lamost_20231108.csv")

# read in S/N of the SDSS spectra

#df_s2n = pd.read_csv(stem + "notebooks_for_development/data/liuetal2020_s2n.csv")

# now read in our own retrievals, and merge with the above by file name
#df_lamost_rrlfe_retrievals = pd.read_csv(stem + "/bin/20230120_all_spectra_retrieved_vals.csv")

# merge with S/N
#df_lamost_rrlfe_retrievals['file_name_s2n_match'] = df_lamost_rrlfe_retrievals["orig_spec_file_name"].str.split("_net", 0, expand=True)[0]
#df_s2n['file_name_s2n_match'] = df_s2n['file_name'].str.split("_net", 0, expand=True)[0]
#df_lamost_rrlfe_retrievals = df_lamost_rrlfe_retrievals.merge(df_s2n, on='file_name_s2n_match', how='inner')


# retrieve LAMOST RA, DEC
df_lamost_specs_ra_dec = pd.read_csv(stem + "notebooks_for_development/data/lamost_ra_dec_spec_file_names.txt")



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
merged_df_liu_feh["error_feh_liu"] = merged_df_liu_feh["e_FeH"]

# some info
print("Number of stars in Liu:",len(df_liu_stars.drop_duplicates()))
print("Number of LAMOST spectra:",len(df_lamost_specs_ra_dec.drop_duplicates()))
print("Number of Liu-LAMOST matches:",len(merged_df_liu_feh.drop_duplicates()))

# for clarity
df_our_data["feh_rrlfe"] = df_our_data["feh_corrected"]
df_our_data["error_feh_rrlfe"] = df_our_data["err_feh_retrieved"]

# for matching
merged_df_liu_feh["match_name"] = merged_df_liu_feh["file_name"].str.split(".",1).str[0]
df_our_data["match_name"] = df_our_data["orig_spec_file_name"].str.split(".",1).str[0]


# merge our retrievals onto Liu etc.
merged_df_liu_rrlfe = pd.merge(merged_df_liu_feh, df_our_data, how="inner", on=["match_name"])


plt.scatter(merged_df_liu_rrlfe["feh_liu"],merged_df_liu_rrlfe["feh_rrlfe"], alpha=0.2)
plt.plot([-4.0,4.0],[-4.0,4.0], linestyle="--", color="grey", label="1-to-1")
plt.ylabel("[Fe/H], rrlfe")
plt.xlabel("[Fe/H], Liu+")
plt.legend()

file_name_placeholder = "junk.png"
plt.savefig("junk.png")

print("Wrote " + file_name_placeholder)

# write out data as csvs (rename cols for clarity)
text_file_name = "junk_liu.csv"
header = ["orig_spec_file_name", "feh_liu", "error_feh_liu", "feh_rrlfe", "error_feh_rrlfe"]
merged_df_liu_rrlfe.to_csv(text_file_name, columns = header, index=False)
print("Wrote",text_file_name)