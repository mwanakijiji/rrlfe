#!/usr/bin/env python
# coding: utf-8

# This reads in data downloaded from ESO, identifies star, and writes files out
# as ascii with Gaia DR2 name in file name, so they can be read back in and stitched
# together.

# Created 2022 Aug. 6 by E.S.

from astropy.io import fits
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import glob
from astroquery.simbad import Simbad
import astropy.coordinates as coord
import astropy.units as u
import pandas as pd
import os

# directory containing Crestani FITS files
stem = "/Users/bandari/Documents/git.repos/rrlfe/src/crestani_spectra/"

# directory to receive asciis
dir_write_out = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/crestani_asciis_prestitch/"

file_name_list = glob.glob(stem + "*.fits")

gaiadr2_list = list()

for num_iteration in range(0,len(file_name_list)):
    print(num_iteration, "out of "+str(len(file_name_list)))

    file_name = file_name_list[num_iteration]

    hdul = fits.open(file_name)

    header = hdul[0].header
    spec_data = np.array(hdul[1].data[:2][0])

    # determine sigma of Gaussian kernel
    abcissa_data = spec_data[:][0]
    spacing = np.mean(np.subtract(abcissa_data,np.roll(abcissa_data,1))[1:-1])
    # del_lambda = lambda/R; lambda changes, obviously, and we'll just use central value
    sigma_lambda_units = np.divide(4430.5,2000.) # in units um
    sigma_element_units = np.divide(sigma_lambda_units,spacing) # in units of array elements

    # range we want to have: 3911 to 4950 angstr
    idx = np.logical_and(abcissa_data>=3911,abcissa_data<=4950)

    # if there is actually data in that range
    '''
    if sum(idx) < 30000:
        print("Not enough data in " + file_name)
        continue
    '''

    # degrade spectrum
    '''
    flux_smoothed = gaussian_filter1d(input=spec_data[:][1], sigma=sigma_element_units)
    '''

    try:

        # identify star
        print("IDing star")
        coord_string = str(header["RA"]) + " " + str(header["DEC"])
        result_table_obj = Simbad.query_region(coord.SkyCoord(coord_string, unit=(u.deg, u.deg), frame='icrs'), radius='0d0m20s') # identify object
        result_table_synon = Simbad.query_objectids(result_table_obj["MAIN_ID"][0]) # retrieve synonyms

        decoded_array = [elem.decode() for elem in np.array(result_table_synon["ID"])] # convert to array with elements of strings
        df = pd.DataFrame(decoded_array, columns=["IDS"])
        idx_gaiadr2 = df["IDS"].str.contains("Gaia DR2") # get Gaia DR2 name

        gaiadr2_string = df["IDS"].loc[idx_gaiadr2].values[0].split("Gaia DR2 ")[-1] # extract Gaia DR2 ID string

        gaiadr2_list.append(gaiadr2_string)

        # write out ascii
        # cols:
        # [0]: wavelength [angstr]
        # [1]: flux [unnormzed]
        # [2]: error [sqrt(flux)]
        df_2_write = pd.DataFrame(spec_data[:][0], columns=["wavelength"])
        df_2_write["flux"] = spec_data[:][1]
        df_2_write["err_flux"] = np.sqrt(spec_data[:][1])

        file_ascii_write = dir_write_out + gaiadr2_string + "_" + os.path.basename(file_name).split(".fits")[0] + ".dat"
        df_2_write.to_csv(file_ascii_write, sep = " ", header=False, index=False)
        print("Wrote " + file_ascii_write)

        '''
        file_name_write = "/Users/bandari/Downloads/junk_plots/" + str(num_iteration) + ".png"
        print("Writing " + file_name_write)
        plt.clf()
        plt.scatter(spec_data[:][0],spec_data[:][1],s=1)
        #plt.scatter(spec_data[:][0],flux_smoothed, s=1)
        plt.title(os.path.basename(file_name) + "\n" + gaiadr2_string)
        plt.axvline([3911])
        plt.axvline([4950])
        #plt.show()
        plt.savefig(file_name_write)
        '''


    except:
        print("Skipping " + file_name)
        continue
