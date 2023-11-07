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

#stem = '/suphys/espa3021/Documents/'
stem = "/Users/bandari/Documents/git.repos/DO_NOT_USE_rrlfe/"
#file_list_read = glob.glob(stem + "lietal_spectra/03_red_blue_fused/" + "*csv")
#file_list_read = glob.glob(stem + "notebooks_for_development/data/lietal2023_raw_spectra/03_red_blue_fused/" + "*csv")
file_list_read = glob.glob(stem + "src/sdss_cosmic_rays_removed/" + "*dat")
dir_write = stem + "notebooks_for_development/sdss_chopped_3911_to_4950/"

# initialize a table for file names, RA, DEC, to write out separately from the spectrum itself
#df_ra_dec = pd.DataFrame(np.zeros([len(file_list_read),4]), columns=["file_name","ra","dec","emp_snr"])

for file_num in range(0,len(file_list_read)):

    print(str(file_num) + " out of " + str(len(file_list_read)))

    df = pd.read_csv(file_list_read[file_num], names=["wavel", "flux", "noise_net"], delim_whitespace=True)
    # wavel,flux_net,noise_net

    # chop by wavelength and drop old indices
    df = df.where( np.logical_and(df['wavel'] >= 3911., df['wavel'] <= 4950.) ).dropna().reset_index(drop=True)
    #idx = np.logical_and(hdu[0].data[2,:] >= 3911., hdu[0].data[2,:] <= 4950.) # McD data chopped to this
    df.to_csv(dir_write + os.path.basename(file_list_read[file_num]).split(".")[0]+".dat",
                        sep=" ", index=False, header=False)