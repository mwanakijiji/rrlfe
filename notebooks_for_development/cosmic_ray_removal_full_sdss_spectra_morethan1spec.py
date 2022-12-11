#!/usr/bin/env python
# coding: utf-8

# This automates removal of cosmic rays from SDSS red and blue single-epoch spectra,
# as required by Young Sun

# Created 2022 Dec. 3 by E.S.

'''
Order of operations:

1.) Based on number of single-epoch spectra
    - If 1 spectrum only, ignore for now
    - If 2 spectra only, do a sigma-clipping and identify anomalies *upward* (with a window)
    - If >=3 spectra, find median spectrum and identify outliers (with a window)
2.) TBD
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
                        "02b_morethan1spec_post_cosmic_ray_removal/"

# find individual file names
file_list = glob.glob(stem_raw_single_epoch + "*.csv")
# find all parent names (i.e., one name for each target, whether or not multiepoch observations were made)
parent_list = list(set([i.split("_g0")[0] for i in file_list]))

# find individual file names
file_list_red = glob.glob(stem_raw_single_epoch + "*color_red.csv")
# find all parent names (i.e., one name for each target, whether or not multiepoch observations were made)
parent_list_red = list(set([i.split("_g0")[0] for i in file_list_red]))


def flag_regions(df_empir_pass,df_avg_pass,df_median_pass,sigma_choice=1):
    '''
    Flag points based on their deviation from the average spectrum

    INPUTS:
    df_empir_pass: dataframe of empirical spectrum
    df_avg_pass: dataframe of average spectrum
    df_median_pass: dataframe of median spectrum
    sigma_choice: threshold for clipping
    '''

    # initialize DataFrame to return
    masked_spec = df_empir_pass.copy(deep=True)
    #masked_spec["flux_masked_1"] = masked_spec["flux"]

    # take difference between empirical spectrum and the AVERAGE of the AVERAGE AND MEDIAN spectrum
    # (note this preserves sign information, and (if only 2 spectra are being compared) protects against
    # misidentification of a cosmic ray in 1 spectrum when the ray is actually in the other)
    #initialize DataFrame for taking an average of some kind
    standin_df = df_avg_pass.copy(deep=True)
    standin_df["median_flux"] = df_median_pass["median_flux"]
    # remove column of wavelengths
    print(standin_df.keys())
    standin_df = standin_df.drop(labels=["wavel"],axis=1)
    # find the mean of a mean and a median
    standin_df["mean_of_stuff"] = standin_df.mean(axis=1) # average of the columns (superfluous?)

    #avg_flux = np.expand_dims(df_avg_pass["avg_flux"].values,axis=1)
    #median_flux = np.expand_dims(df_median_pass["median_flux"].values,axis=1)
    #print(np.expand_dims(avg_flux,axis=0).shape)
    #print(median_flux.shape)
    #mean_median_combo = np.mean(avg_flux,median_flux)

    # difference between empirical and median
    # masked_spec["diff"] = np.subtract(df_empir_pass["flux"],standin_df["mean_of_stuff"])
    masked_spec["diff"] = np.subtract(df_empir_pass["flux"],standin_df["median_flux"])

    #plt.plot(masked_spec["diff"])
    #plt.show()

    # mask deviant points
    # logic: is positive difference between empirical and median beyond error bounds?
    error_bound_1 = sigma_choice*np.nanstd(masked_spec["diff"])
    logic_1 = np.greater(masked_spec["diff"],error_bound_1)
    masked_spec["flux_flag_1"] = logic_1 # flag these points as suspect

    # make a second pass (if not, some cosmic rays in the first pass may raise the
    # bar for flagging cosmic rays up so that smaller rays are missed)
    error_bound_2 = sigma_choice*np.nanstd(masked_spec["diff"].where(masked_spec["flux_flag_1"]==0))
    logic_2 = np.greater(masked_spec["diff"],error_bound_2)
    masked_spec["flux_flag_1"] = logic_2 # flag these points as suspect

    return masked_spec, error_bound_1, error_bound_2


def discard_if_in_line(this_spectrum):
    '''
    If flagged areas of an input spectrum are inside absorption line regions,
    throw a flag to indicate that line needs to be discarded. Recall
    3933.66-30 # CaII-K
    3970.075 # H-eps
    4101.71 # H-del
    4340.472 # H-gam
    4861.29 # H-beta
    6562.79 # H-alpha

    INPUTS:

    this_spectrum: DataFrame with cols
        - wavel: wavelength abcissa
        - flux_flag_1: boolean flag at each wavelength (0: good; 1: bad)

    RETURNS:

    0 [int]: fine; no flagged points inside lines
    1 [int]: bad; there are points inside lines
    '''
    margin_choice = 20. # angstroms
    caii_K_line = np.logical_and(this_spectrum["wavel"] >= 3933.66-margin_choice,this_spectrum["wavel"] <= 3933.66+margin_choice)
    h_eps_line = np.logical_and(this_spectrum["wavel"] >= 3970.075-margin_choice,this_spectrum["wavel"] <= 3970.075+margin_choice)
    h_del_line = np.logical_and(this_spectrum["wavel"] >= 4101.71-margin_choice,this_spectrum["wavel"] <= 4101.71+margin_choice)
    h_gam_line = np.logical_and(this_spectrum["wavel"] >= 4340.472-margin_choice,this_spectrum["wavel"] <= 4340.472+margin_choice)
    h_beta_line = np.logical_and(this_spectrum["wavel"] >= 4861.29-margin_choice,this_spectrum["wavel"] <= 4861.29+margin_choice)
    h_alpha_line = np.logical_and(this_spectrum["wavel"] >= 6562.79-margin_choice,this_spectrum["wavel"] <= 6562.79+margin_choice)

    # sum across the arrays
    sum_array = np.sum([np.array(caii_K_line),
                        np.array(h_eps_line),
                        np.array(h_del_line),
                        np.array(h_gam_line),
                        np.array(h_beta_line),
                        np.array(h_alpha_line)],axis=0)
    # convert to boolean (True = 'there is an absorption line here')
    line_bool_array = np.array(sum_array, dtype=bool)
    # inversion so 1 signifies regions OUTSIDE lines
    #outside_line_bool_array = ~line_bool_array

    # indices of cosmic ray artifacts inside absorption lines...
    idx_2_drop = this_spectrum.index[np.logical_and(this_spectrum["flux_flag_1"],line_bool_array)].tolist()

    # if the list of indices is non-zero in length, throw the flag
    if len(idx_2_drop) > 0:
        return_flag = 1
    elif len(idx_2_drop) == 0:
        return_flag =0

    print("idx_2_drop",idx_2_drop)
    print("return_flag",return_flag)

    return return_flag



# loop over each parent FITS file
for t in range(0,len(parent_list)):

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
        #print(matching)

        #print("-------------------------")

        if (len(matching) == 1):

            print("Only one match found for this color. Skipping")
            print(matching)

        elif (len(matching) >= 2):


            # dictionary to hold dataframes
            d = {}

            # intialize aggregate array to contain all fluxes
            df_dummy = pd.read_csv(matching[0], names=["wavel","flux","noise"], delim_whitespace=False, skiprows=1)
            aggregate_flux_array = np.nan*np.ones((len(df_dummy),len(matching)))

            # collect spectra in single dictionary
            for p in range(0,len(matching)):

                # read in one of the matches
                df_single_p = pd.read_csv(matching[p], names=["wavel","flux","noise"], delim_whitespace=False, skiprows=1)

                #plt.plot(df_single_p["wavel"],df_single_p["flux"])

                # sanity check that wavelength abcissa are the same among all the matches
                if p==0:
                    # for checking wavel abcissa is same
                    wavel_initial = df_single_p["wavel"].values
                else:
                    #print(df_single_p["wavel"])
                    #print(wavel_initial)
                    #print(len(np.setdiff1d(df_single_p["wavel"].values,wavel_initial)))
                    if len(np.setdiff1d(df_single_p["wavel"].values,wavel_initial) >= 1):
                        print("Hey, the wavelength abcissas are not the same!")
                        sys.exit()

                # put fluxes into aggregate array
                aggregate_flux_array[:,p] = df_single_p["flux"].values


            # take mean flux of all the spectra
            mean_flux_array = np.mean(aggregate_flux_array,axis=1)

            # cast mean spectrum data to a DataFrame
            df_mean = pd.DataFrame(mean_flux_array,columns=["avg_flux"])
            df_mean["wavel"] = df_single_p["wavel"] # uses last spectrum read in

            # include median flux too (important for identifying cosmic rays when only 2 spectra are compared)
            median_flux_array = np.median(aggregate_flux_array,axis=1)
            df_median = pd.DataFrame(median_flux_array,columns=["median_flux"])
            df_median["wavel"] = df_single_p["wavel"] # uses last spectrum read in
            #mean_flux_array["median_flux"] = pd.Series(median_flux_array.tolist())

            for p in range(0,len(matching)):

                #print("len(matching)", len(matching))
                #print(matching)

                # test each empirical spectrum against the mean, and flag points
                df_single_p = pd.read_csv(matching[p], names=["wavel","flux","noise"], delim_whitespace=False, skiprows=1)
                flagged_empirical, limit1, limit2 = flag_regions(
                                                        df_empir_pass = df_single_p,
                                                        df_avg_pass = df_mean,
                                                        df_median_pass = df_median,
                                                        sigma_choice=5
                                                        )


                # if cosmic ray appears to be in an absorption line, discard the spectrum entirely
                test_line_contam = discard_if_in_line(flagged_empirical)
                if test_line_contam:
                    print("Line contamination; skipping ",str(matching[p]))
                    continue
                elif not test_line_contam:
                    # if not contaminated, write out a csv of the masked spectrum
                    spec_cleaned = flagged_empirical.where(flagged_empirical["flux_flag_1"] == False)
                    file_name_cleaned_write = stem_write + os.path.basename(matching[p])
                    spec_cleaned.to_csv(file_name_cleaned_write, columns=["wavel","flux","noise"], index=False)
                    print("Wrote",file_name_cleaned_write)


                #plt.plot(wavel_initial,mean_flux_array,linestyle="--",color="k")
                #plt.show()
                #plt.clf()

                ## ## CONTINUE HERE; MAKE SURE FLAGS ARE GOOD FOR EACH CHILD SPECTRUM
                #plt.clf()
                fig = plt.figure(figsize=(24,10))
                plt.plot(flagged_empirical["wavel"],
                         np.multiply(100,flagged_empirical["flux_flag_1"]),color="gray",alpha=0.5,label="flag")
                #.axvline(x=0, ymin=0, ymax=1

                # plot mean flux
                plt.plot(df_mean["wavel"],np.add(df_mean["avg_flux"],0.2),label="mean")
                # plot median flux
                plt.plot(df_mean["wavel"],np.add(df_median["median_flux"],0.2),label="median")
                # plot empirical flux
                plt.plot(flagged_empirical["wavel"],flagged_empirical["flux"],label="empirical", zorder=9)
                plt.plot(spec_cleaned["wavel"],spec_cleaned["flux"],label="cleaned", zorder=10)
                # plot flux minus mean flux
                plt.plot(flagged_empirical["wavel"],flagged_empirical["diff"],label="diff")
                #plt.plot(df_single_p["wavel"].where(test["flux_flag_1"] == True),
                #             df_single_p["flux"].where(test["flux_flag_1"] == True),
                #         label="flagged",color="k",linewidth=4)
                plt.plot([3900,9000],[limit1,limit1],linestyle="--")
                plt.plot([3900,9000],[limit2,limit2],linestyle="--")
                plt.title(str(os.path.basename(matching[p]))+ " match number" + str(p))
                plt.legend(loc="lower right")
                file_name_write = stem_write+"plots/plot_" + str(os.path.basename(matching[p])) + ".png"
                plt.savefig(file_name_write, facecolor="white", edgecolor='white')
                print("Wrote", file_name_write)
                plt.clf()
                #plt.show()
