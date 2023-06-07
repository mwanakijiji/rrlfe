#!/usr/bin/env python
# coding: utf-8

# 1. Reads in specObj-dr17.fits 
# 2. Cross-checks spectra with list of RA,DEC of RR Lyrae stars in Li+ 2023
# 3. Writes out file of FITS file name strings for an rsync download
# (See instructions from SDSS help desk further below)

from astropy.io import fits
from astropy.table import Table
import pandas as pd
import numpy as np

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read in Li+ 2023 text file
df_lietal2023_results = pd.read_csv(stem + "notebooks_for_development/data/RRLyraes_final_lietal_beers_2023apr.csv",
                              usecols=["source_id", "R.A.", "Decl.","[Fe/H]_PHOT"])

# read in FITS file of params of all specs in SDSS DR17
# takes 2.5 min to load
dat_sdss = Table.read(stem + 'notebooks_for_development/data/specObj-dr17.fits', format='fits')

# vestigial; can truncate here for troubleshooting
dat_tbl = dat_sdss

# filter out multidimensional columns that we don't care about
names = [name for name in dat_tbl.colnames if len(dat_tbl[name].shape) <= 1]
df_specobj_dr17 = dat_tbl[names].to_pandas()
#df_specobj_dr17 = dat_test.to_pandas()

# give some cols same name and round, so we can merge on them
df_specobj_dr17["ra_round"] = np.round(df_specobj_dr17["PLUG_RA"],3)
df_specobj_dr17["dec_round"] = np.round(df_specobj_dr17["PLUG_DEC"],3)

df_lietal2023_results["ra_round"] = np.round(df_lietal2023_results["R.A."],3)
df_lietal2023_results["dec_round"] = np.round(df_lietal2023_results["Decl."],3)

# merge on RA, DEC
merged_df = pd.merge(
                    df_specobj_dr17, 
                    df_lietal2023_results, 
                    how="inner", on=["ra_round","dec_round"]
                    )

# extract the (plate, mjd, fiberid, run2d) for all matches
# RUN2D: an integer denoting the version of extraction and redshift-finding used

'''
parameters of interest:
'PLATE'
'MJD'
'FIBERID'

'PLUG_RA'
'PLUG_DEC'
'''

pmfr_of_interest = merged_df.rename(columns={"PLATE": "plate", "MJD": "mjd", "FIBERID": "fiberid"})
# convert a column of byte objects to strings
pmfr_of_interest['run2d'] = pmfr_of_interest['RUN2D'].str.decode("utf-8").str.strip()
#pmfr_of_interest = merged_df[['plate','mjd','fiberid','run2d']]

# write combinations of interest to file
with open("junk.txt", "a") as myfile:

    # loop over all matches
    for index, row in pmfr_of_interest.iterrows():

        plate = row['plate']
        mjd = row['mjd']
        fiberid = row['fiberid']
        run2d = row['run2d']

        # write the combos into strings:
        row_this_string = '/sdss/spectro/redux/'+str(run2d)+'/spectra/full/'+ \
                            str(plate)+'/spec-'+str(plate)+'-'+str(mjd)+'-'+f'{fiberid:04}' + '.fits' + '\n'

        # append to file
        myfile.write(row_this_string)

'''
--Email from SDSS help desk, June 6, 2023:--

Since you already have a list of objects with RA and Dec, one way to do this would be for you first 
download the (latest, for e.g.) specObj-dr17.fits file from the SPECTRO_REDUX folder on the SAS to 
crossmatch the coordinates yourself to collect the corresponding plate, mjd, fiberid and run2d values.  
Once you have those values, you can then turn it into a download_bulk.txt file with the values substituted 
into the pattern for the file’s location as follows:

/sdss/spectro/redux/{run2d}/spectra/lite/{plate}/spec-{plate}-{mjd}-{fiberid:0>4}.fits

for spec lite files, or replate lite -> full if you plan to use the individual exposures.

Once you have a download_bulk.txt file containing the strings of the locations as above, then you can run 
the following rsync command to download the file locations from the data release you’re using (e.g. dr17):

rsync -avzL --files-from=download_bulk.txt rsync://dtn.sdss.org/dr17  dr17
'''

