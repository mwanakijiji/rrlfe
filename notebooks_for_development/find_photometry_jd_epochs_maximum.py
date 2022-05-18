#!/usr/bin/env python
# coding: utf-8

# This calculates light curve maxima, as observed at MacAdam, U Louisville, and Mt. Kent in Australia

# created 2020 May 18 by E.S.

import astropy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import glob

# read in original photometries, fit Nth order polynomial, interp to find max

dir_photometries = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/photometries/"

file_names = glob.glob(dir_photometries + "*csv")
file_names.sort()

for i in range(0,len(file_names)):

    data_df = pd.read_csv(file_names[i])
    data_df["JD_trunc"] = np.subtract(data_df["JD"],np.floor(data_df["JD"][0]))

    print("-----------")
    print(file_names[i])

    try:
        p = np.polyfit(data_df["JD_trunc"], data_df["del_mag"], deg=5)
    except:
        print("FAILED")
        continue

    abcissa_fine = np.linspace(np.min(data_df["JD_trunc"]),np.max(data_df["JD_trunc"]),int(1e8))
    ordinate_fine = np.multiply(p[0],np.power(abcissa_fine,5)) + \
                                np.multiply(p[1],np.power(abcissa_fine,4)) + \
                                np.multiply(p[2],np.power(abcissa_fine,3)) + \
                                np.multiply(p[3],np.power(abcissa_fine,2)) + \
                                np.multiply(p[4],abcissa_fine) + \
                                p[5]

    epoch_max = abcissa_fine[np.where(ordinate_fine == np.min(ordinate_fine))][0]

    plt.scatter(data_df["JD_trunc"], data_df["del_mag"], color="k", s=4)
    plt.plot(abcissa_fine, ordinate_fine, linewidth=5, color="red", alpha=0.5)

    plt.gca().invert_yaxis()

    plt.annotate("Max at " + str(epoch_max),(0.5,0.3),xycoords="figure fraction")

    plt.title(os.path.basename(file_names[i]))

    plt.ylabel("mag")
    plt.xlabel("JD - " + str(np.floor(data_df["JD"][0])))

    plt.savefig(os.path.basename(file_names[i]).split(".")[0] + ".pdf")
    plt.clf()

    print("Max: " + str(np.floor(data_df["JD"][0]) + epoch_max))
    print(os.path.basename(file_names[i]).split(".")[0] + ".pdf")
