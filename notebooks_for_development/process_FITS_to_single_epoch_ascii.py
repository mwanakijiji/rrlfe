#!/usr/bin/env python
# coding: utf-8

# This takes SDSS FITS spectra and separates out the single-epoch spectra and writes them out again as
# individual ascii files

# Created 2022 Dec. 1 by E.S.

from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import glob
import os

'''
stem = "/Users/bandari/Documents/git.repos/rrlfe/src/sdss_original_single_epoch_fits/"
stem_notebooks = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/sdss_processing/01_separated_and_interpolated/"
'''
stem = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/lietal_spectra_test/"
stem_notebooks = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/lietal_spectra_test/01_separated_and_interpolated/"

file_list = glob.glob(stem + "*fits")

'''
FITS headers contain these values:

Name      Type      Comment
flux      float32   coadded calibrated flux [10-17 ergs/s/cm2/Å]
loglam    float32   log10(wavelength [Å])
ivar      float32   inverse variance of flux
and_mask  int32     AND mask
or_mask   int32     OR mask
wdisp     float32   wavelength dispersion in pixel=dloglam units
sky       float32   subtracted sky flux [10-17 ergs/s/cm2/Å]
model     float32   pipeline best model fit used for classification and redshift
'''

# blue end: interpolate between [3850,5970] at intervals of 1.4 angstroms such that 3900.00, 3901.40 [...] 4999.00
# red end: interpolate between [6030:]

for i in range(0,len(file_list)):

    print(i,"out of",len(file_list))

    hdul = fits.open(file_list[i])

    num_spec_total = len(hdul)-4

    # loop over blue-red pairs
    for num_blue in range(int(0.5*num_spec_total)):

        print("-----")

        # blue end
        idx_blue = 4+num_blue
        data_blue = hdul[idx_blue].data
        flux_blue = np.flip(data_blue["flux"]) # flip to make wavelength increasing
        wavel_blue = np.flip(np.power(10.,data_blue["loglam"]))
        sigma_blue = np.flip(np.divide(1.,np.sqrt(data_blue["ivar"])))

        # red end
        idx_red = idx_blue+int(0.5*num_spec_total)
        data_red = hdul[idx_red].data
        flux_red = data_red["flux"]
        wavel_red = np.power(10.,data_red["loglam"])
        sigma_red = np.divide(1.,np.sqrt(data_red["ivar"]))

        # make new abcissae for interpolating the plots
        blue_0 = 3850. # bluest of blue end
        red_1 = 9000. # reddest of red end
        num_steps = int(np.floor((red_1-blue_0)/1.4))
        abcissa_interp = np.add(blue_0-0.4,1.4*np.arange(0,num_steps+2,1)) # -0.4 to get the phase right

        # interpolate the spectra

        # blue region I ultimately want: [3850:5970]
        # red region I ultimately want: [6030:9000]
        # overlap region that needs to be averaged: [5970:6030]

        # indices of data points corresponding to abcissa [3850:6030] (note includes overlap region)
        idx_blue = np.where( np.logical_and(abcissa_interp > 3849., abcissa_interp < 6031.) )
        # indices of data points corresponding to abcissa [5970:9000] (note includes overlap region)
        idx_red = np.where( np.logical_and(abcissa_interp > 5969., abcissa_interp < 9001.) )

        flux_blue_interp = np.interp(x = abcissa_interp[idx_blue], xp = wavel_blue, fp = flux_blue)
        error_flux_blue_interp = np.interp(x = abcissa_interp[idx_blue], xp = wavel_blue, fp = sigma_blue)
        flux_red_interp = np.interp(x = abcissa_interp[idx_red], xp = wavel_red, fp = flux_red)
        error_flux_red_interp = np.interp(x = abcissa_interp[idx_red], xp = wavel_red, fp = sigma_red)

        # write out
        # cols:
        # [0] wavel_interp
        # [1] flux_blue_interp
        # [2] error_flux_blue_interp
        # [3] wavel_red_interp
        # [4] flux_red_interp
        # [5] error_flux_red_interp

        df_blue_write = pd.DataFrame(abcissa_interp[idx_blue], columns=["wavel_blue"])
        df_blue_write["flux_blue"] = flux_blue_interp
        df_blue_write["error_flux_blue"] = error_flux_blue_interp

        df_red_write = pd.DataFrame(abcissa_interp[idx_red], columns=["wavel_red"])
        df_red_write["flux_red"] = flux_red_interp
        df_red_write["error_flux_red"] = error_flux_red_interp

        # write csvs
        file_name_blue_this = stem_notebooks + os.path.basename(file_list[i]).split(".")[0] + '_g{:0>3}'.format(num_blue) + "_color_blue.csv"
        df_blue_write.to_csv(file_name_blue_this, index=False)
        print("Wrote",file_name_blue_this)

        file_name_red_this = stem_notebooks + os.path.basename(file_list[i]).split(".")[0] + '_g{:0>3}'.format(num_blue) + "_color_red.csv"
        df_red_write.to_csv(file_name_red_this, index=False)
        print("Wrote",file_name_red_this)

        # plotting
        '''
        plt.clf()
        fig = plt.figure(figsize=(15,5))
        plt.plot(wavel_blue,flux_blue)
        plt.plot(wavel_blue,sigma_blue)
        plt.plot(wavel_red,flux_red)
        plt.plot(wavel_red,sigma_red)
        plt.plot(df["wavel"],df["flux"])
        plt.axvline(x=5970, linestyle="--")
        plt.axvline(x=6030, linestyle="--")
        plt.ylim([0,100])
        plt.xlabel("wavel (angstrom)")
        plt.ylabel("flux")
        plt.xlim([4000,4150])
        #plt.savefig("./junk_data/" + os.path.basename(file_list[i]) + ".png")
        plt.show()
        '''
