#!/usr/bin/env python
# coding: utf-8

# Takes blue and red ends of single-epoch spectra from SDSS, fuses them
# together by averaging the overlap region, and writes out the result

# Created 2022 Dec 12 by E.S.

import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

stem_read = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/"+ \
               "sdss_processing/02b_morethan1spec_post_cosmic_ray_removal/"
stem_write = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/"+ \
             "sdss_processing/03_red_blue_fused/"

file_list = glob.glob(stem_read + "*csv")

# make list of all blue and red spectra that survived the cosmic ray removal process
# (note that some have red and blue counterparts, and others have only red or blue,
# if the other color did not make it through the cosmic ray removal)
parent_single_epoch_stems_duplicates = [i.split("_color_", 1)[0] for i in file_list]

# remove duplicate names
parent_single_epoch_stems = [*set(parent_single_epoch_stems_duplicates)]

# loop over each stem, check that red and blue are both there
for i in range(0,len(parent_single_epoch_stems)):

    files_available = glob.glob(parent_single_epoch_stems[i] + "*csv")

    # if just red or blue is available, skip it
    if (len(files_available) == 1):

        continue

    # if both red and blue are available, fuse them
    elif (len(files_available) == 2):

        blue_name = glob.glob(parent_single_epoch_stems[i] + "*blue*csv")[0]
        df_blue = pd.read_csv(blue_name)

        red_name = glob.glob(parent_single_epoch_stems[i] + "*red*csv")[0]
        df_red = pd.read_csv(red_name)

        # get rid of regions of overlap where S/N is low
        df_red["flux"].loc[df_red["wavel"] < 5970.] = np.nan
        df_red["noise"].loc[df_red["wavel"] < 5970.] = np.nan
        df_blue["flux"].loc[df_blue["wavel"] > 6030.] = np.nan
        df_blue["noise"].loc[df_blue["wavel"] > 6030.] = np.nan

        # remove one region where there is always a systematic spike
        # that looks like a cosmic ray
        idx_spike = np.logical_and(df_blue["wavel"] > 5574.,df_blue["wavel"] < 5584.)
        df_blue["flux"].loc[idx_spike] = np.nan

        # fuse spectra
        df_fused = df_blue.merge(df_red, how="outer", on="wavel", suffixes=("_blue", "_red"))

        df_fused["flux_net"] = np.nanmean([df_fused["flux_blue"], df_fused["flux_red"]],
                                         axis=0)

        df_fused["noise_blue"] = df_fused["noise_blue"].fillna(0)
        df_fused["noise_red"] = df_fused["noise_red"].fillna(0)
        df_fused["noise_net"] = 0.5*np.sqrt(np.add(np.power(df_fused["noise_blue"].values,2.),
                                         np.power(df_fused["noise_red"].values,2.)))

        # write csv
        csv_write_name = stem_write + os.path.basename(parent_single_epoch_stems[i]) + "_net.csv"
        df_fused.to_csv(csv_write_name, columns=["wavel","flux_net","noise_net"], index=False)
        print("Wrote " + csv_write_name)

        plt.clf()
        plt.plot(df_fused["wavel"],df_fused["flux_net"], label="net")
        plt.plot(df_fused["wavel"],np.add(df_fused["flux_red"],30), label="red")
        plt.plot(df_fused["wavel"],np.add(df_fused["flux_blue"],30), label="blue")
        plt.plot(df_fused["wavel"],df_fused["noise_net"], label="noise")
        plt.legend()
        plt.title(os.path.basename(parent_single_epoch_stems[i]))
        plot_write_name = stem_write + "plots/" + os.path.basename(parent_single_epoch_stems[i]) + ".png"
        plt.savefig(plot_write_name)
        print("Wrote " + plot_write_name)

        print("---")
