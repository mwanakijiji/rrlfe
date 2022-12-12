#!/usr/bin/env python
# coding: utf-8

# This automates removal of cosmic rays from SDSS red and blue single-epoch spectra,
# as required by Young Sun

# Created 2022 Dec. 3 by E.S.

'''
Order of operations:

1.) Based on number of single-epoch spectra
    - If 1 spectrum only, save a plot
'''

import pandas as pd
import numpy as np
import glob
import sys
import os
import matplotlib.pyplot as plt
from astropy.stats import sigma_clip

# top-level directory for SDSS spectra cosmic ray removal
stem_raw_single_epoch = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/sdss_processing/"+\
                        "01_separated_and_interpolated/"
# write spectra following cosmic ray removal to this destination
stem_write = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/sdss_processing/"+\
                        "02a_only1spec/plots/"

# find individual file names
file_list = glob.glob(stem_raw_single_epoch + "*.csv")
# find all parent names (i.e., one name for each target, whether or not multiepoch observations were made)
parent_list = list(set([i.split("_g0")[0] for i in file_list]))

# find individual file names
file_list_red = glob.glob(stem_raw_single_epoch + "*color_red.csv")
# find all parent names (i.e., one name for each target, whether or not multiepoch observations were made)
parent_list_red = list(set([i.split("_g0")[0] for i in file_list_red]))

# loop over each parent FITS file
for t in range(0,len(parent_list)):

    print("Parent FITS file "+str(t)+" of "+str(len(parent_list)))

    matching_all = list(filter(lambda x: parent_list[t] in x, file_list))
    matching_red = list(filter(lambda x: "color_red" in x, matching_all))
    matching_blue = list(filter(lambda x: "color_blue" in x, matching_all))

    #print(matching_all)
    #print(matching_red)
    #print(matching_blue)

    # keep the red and blue parts separate
    for color_num in range(0,2):

        if color_num==0:
            matching = matching_red
        elif color_num==1:
            matching = matching_blue
        print(len(matching))
        print(matching)

        #print("-------------------------")

        if (len(matching) == 1):

            print("Only one match found for this color. Making a plot")
            df_dummy = pd.read_csv(matching[0], names=["wavel","flux","noise"], delim_whitespace=False, skiprows=1)

        elif (len(matching) >= 2):

            continue

        fig = plt.figure(figsize=(24,10))
        plt.plot(df_dummy["wavel"],
                 np.multiply(100,flagged_empirical["flux_flag_1"]),color="gray",alpha=0.5,label="flag")
        #.axvline(x=0, ymin=0, ymax=1

        plt.plot(df_dummy["wavel"],df_dummy["flux"],label="empirical", zorder=9)
        plt.title(str(os.path.basename(matching[p]))+ " match number" + str(p))
        plt.legend(loc="lower right")
        file_name_write = stem_write+"plots/plot_" + str(os.path.basename(matching[p])) + ".png"
        plt.savefig(file_name_write, facecolor="white", edgecolor='white')
        print("Wrote", file_name_write)
        plt.clf()
        plt.close()
        #plt.show()
