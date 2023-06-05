#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 1. Reads in specObj-dr17.fits 
# 2. Cross-checks spectra with list of RA,DEC of RR Lyrae stars in Li+ 2023
# 3. Writes out file of FITS file name strings for an rsync download
# (See instructions from SDSS help desk further below)


# In[1]:


from astropy.io import fits
import pandas as pd


# In[ ]:


stem = "/Users/bandari/Documents/git.repos/rrlfe/"


# In[ ]:


hdul = fits.open(stem + 'notebooks_for_development/data/specObj-dr17.fits')


# In[ ]:


hdul.info()
import ipdb; ipdb.set_trace()


# In[ ]:


# read in Li+ 2023 text file

df_lietal2023_results = pd.read_csv(stem + "notebooks_for_development/data/RRLyraes_final_lietal_beers_2023apr.csv",
                              usecols=["source_id", "R.A.", "Decl.","[Fe/H]_PHOT"])


# In[ ]:


# give some cols same name and round, so we can merge on them

df_lietal2023_results["ra_round"] = np.round(df_lietal2023_stars["R.A."],3)
df_lietal2023_results["dec_round"] = np.round(df_lietal2023_stars["Decl."],3)


# In[ ]:


# round the RA,DEC in the specObj-dr17 file
''' TBD '''    #df_specobj_dr17


# In[ ]:


# merge on RA, DEC

merged_df = pd.merge(
                    df_specobj_dr17, 
                    df_lietal2023_stars, 
                    how="inner", on=["ra_round","dec_round"]
                    )


# In[ ]:


# extract the (plate, mjd, fiberid, run2d) for all matches

'''
pmfr_of_interest = merged_df[['plate','mjd','fiberid','run2d']]

'''


# In[15]:


# write combinations of interest to file

with open("junk.txt", "a") as myfile:

    # loop over all matches
    for combo_interest in range(0,2): #len(pmfr_of_interest)):

        plate = 3851
        mjd = 55302
        fiberid = 1
        run2d = 42

        # write the combos into strings:
        file_this_string = '/sdss/spectro/redux/'+str(run2d)+'/spectra/full/'+ \
                            str(plate)+'/spec-'+str(plate)+'-'+str(mjd)+'-'+f'{fiberid:04}' + '.fits' + '\n'

        # append to file
        myfile.write(file_this_string)


# In[ ]:


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

