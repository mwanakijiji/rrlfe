#!/usr/bin/env python
# coding: utf-8

# Plots SSPP output from Young Sun

# Created 2022 Nov. 21 by E.S.

import pandas as pd
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read in our Fe/H values
df_retrieved = pd.read_csv(stem + "notebooks_for_development/data/retrieved_vals_sdss_overlapping_lietal2023_20230608.csv")

# read in (RA,DEC) of spectra we did retrievals on
ra_dec_sdss = pd.read_csv(stem + "notebooks_for_development/data/specObj-dr17_files_of_interest_lietal2023.csv")
#ra_dec_sdss = pd.read_csv(stem + "notebooks_for_development/data/ra_dec_sdss_spec_overlapping_lietal2023.csv")

#ra_dec_sdss['file_name'] = 'spec-'+str(plate)+'-'+str(mjd)+'-'+f'{fiberid:04}' + '.fits'
ra_dec_sdss['spec_string_match'] = 'spec-'+ra_dec_sdss['PLATE'].astype({'PLATE':'str'})+'-'+ra_dec_sdss['MJD'].astype({'MJD':'str'})+'-'+ra_dec_sdss['FIBERID'].astype({'FIBERID':'str'}).str.zfill(4)

# read in Li+ 2023 text file
df_lietal2023_results = pd.read_csv(stem + "notebooks_for_development/data/RRLyraes_final_lietal_beers_2023apr.csv",
                              usecols=["source_id", "R.A.", "Decl.","[Fe/H]_PHOT"])

# merge (RA,DEC) and our retrievals by string in spectrum file names
df_retrieved["spec_string_match"] = df_retrieved['realization_spec_file_name'].str.split('_g',expand=True)[0]
#ra_dec_sdss["spec_string_match"] = ra_dec_sdss['file_name'].str.split('.',expand=True)[0]
df_rrlfe_radec = df_retrieved.merge(ra_dec_sdss, on='spec_string_match', how='inner')
# round RA,DEC to merge
df_rrlfe_radec["ra_round"] = np.round(df_rrlfe_radec["R.A."],3)
df_rrlfe_radec["dec_round"] = np.round(df_rrlfe_radec["Decl."],3)

# now merge with Li+ 2023 
df_lietal2023_results["ra_round"] = np.round(df_lietal2023_results["R.A."],3)
df_lietal2023_results["dec_round"] = np.round(df_lietal2023_results["Decl."],3)
merged_rrlfe_lietal2023 = pd.merge(df_rrlfe_radec, df_lietal2023_results, how="inner", on=["ra_round","dec_round"])

# rename some columns for writing to file
merged_rrlfe_lietal2023 = merged_rrlfe_lietal2023.rename(columns={"feh_corrected": "feh_rrlfe", "[Fe/H]_PHOT_x": "feh_lietal2023"})

file_name = 'junk.csv'
merged_rrlfe_lietal2023.to_csv(file_name, columns=['feh_rrlfe','feh_lietal2023'])
print('Wrote',file_name)
