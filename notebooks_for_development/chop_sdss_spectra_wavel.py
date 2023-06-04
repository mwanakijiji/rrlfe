#!/usr/bin/env python
# coding: utf-8

# Takes LAMOST spectra, and
# 1. chops them to the range 3911 to 4950 A
# 2. uses blank space delimiters to make them ingestible into the pipeline
# 3. ... and writes out a separate file with target info

# Created 2022 Jan. 5 by E.S.

import pandas as pd
import glob
import numpy as np
import os
from astropy.io import fits
import matplotlib.pyplot as plt

stem = '/suphys/espa3021/Documents/'
#stem = "/Users/bandari/Documents/git.repos/rrlfe/"

file_list_read = glob.glob(stem + "lietal_spectra/03_red_blue_fused/" + "*csv")
dir_write = stem + "04_chopped_3911_to_4950/"

# initialize a table for file names, RA, DEC, to write out separately from the spectrum itself
#df_ra_dec = pd.DataFrame(np.zeros([len(file_list_read),4]), columns=["file_name","ra","dec","emp_snr"])

for file_num in range(0,len(file_list_read)):

    print(str(file_num) + " out of " + str(len(file_list_read)))

    df = pd.read_csv(file_list_read[file_num])
    # wavel,flux_net,noise_net

    # indices of the desired wavelength range
    import ipdb; ipdb.set_trace()
    idx = df.where( np.logical_and(df['wave'] >= 3911., df['wave'] <= 4950.) )
    #idx = np.logical_and(hdu[0].data[2,:] >= 3911., hdu[0].data[2,:] <= 4950.) # McD data chopped to this

    # initialize new DataFrame to hold spectrum
    df_spec_this = pd.DataFrame(hdu[0].data[2,idx], columns=["wavel"])
    df_spec_this["flux"] = hdu[0].data[0,idx]
    df_spec_this["err_flux"] = np.divide(hdu[0].data[0,:],1./np.sqrt(hdu[0].data[1,:]))[idx]
    #df_spec_this["err_flux"] = hdu[0].data[0,idx]

    # add S/N to table AFTER having chopped the spectra
    df_ra_dec["emp_snr"].loc[file_num] = np.median(np.divide(hdu[0].data[0,idx],1./np.sqrt(hdu[0].data[1,idx])))

    # write out spectrum
    df_spec_this.to_csv(dir_write + os.path.basename(file_list_read[file_num]).split(".")[0]+".dat",
                        sep=" ", index=False, header=False)

    # make FYI plot
    '''
    plt.clf()
    plt.plot(df_spec_this["wavel"], df_spec_this["flux"])
    plt.savefig("junk" + os.path.basename(file_list_read[file_num]).split(".")[0]+".png")
    '''

# write out list of file info for cross-matching
# file_name: lamost_li_file_info.csv
df_ra_dec.to_csv(stem + "notebooks_for_development/data/junk.csv", index=False)
