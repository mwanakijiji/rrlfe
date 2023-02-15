import glob
import pandas as pd
import os
import numpy as np
import sys
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits
from . import *

def feh_layden_vector(coeff_a,coeff_b,coeff_c,coeff_d,H,K):
    """
    Finds Fe/H given equivalent widths (in angstroms), from
    K = a + b*H + c*[Fe/H] + d*H*[Fe/H]  (Layden 1994 Eqn. 7)

    Parameters:
        coeff_a (float): coefficient a
        coeff_b (float): coefficient b
        coeff_c (float): coefficient c
        coeff_d (float): coefficient d

    Returns:
        [Fe/H] value
    """

    feh = np.divide(np.subtract(K,np.subtract(coeff_a,np.multiply(coeff_b,H))),
                    np.add(coeff_c,np.multiply(coeff_d,H)))

    return feh

def feh_abcdfghk_vector(coeff_a,coeff_b,coeff_c,coeff_d,coeff_f,coeff_g,coeff_h,coeff_k,H,K):
    """
    Finds Fe/H given equivalent widths (in angstroms), from
    K = a + b*H + c*[Fe/H] + d*H*[Fe/H] + f*(H^2) + g*([Fe/H]^2) + h*(H^2)*[Fe/H] + k*H*([Fe/H]^2)

    Parameters:
        coeff_a (float): coefficient a
        coeff_b (float): coefficient b
        coeff_c (float): coefficient c
        coeff_d (float): coefficient d
        coeff_f (float): coefficient f
        coeff_g (float): coefficient g
        coeff_h(float): coefficient h
        coeff_k (float): coefficient j
    Returns:
        [Fe/H] value
    """

    A_cap = np.add(coeff_g,np.multiply(coeff_k,H))
    B_cap = np.add(coeff_c,np.add(np.multiply(coeff_d,H),np.multiply(coeff_h,np.power(H,2))))
    C_cap = np.add(coeff_a,np.add(np.multiply(coeff_b,H),np.subtract(np.multiply(coeff_f,np.power(H,2)),K)))
    # since this involves a quadratic, there are two roots
    #import ipdb; ipdb.set_trace()
    F_pos = np.divide(-np.add(
                            B_cap,
                              np.sqrt(
                                            np.subtract(np.power(B_cap,2.),
                                                        4*np.multiply(A_cap,C_cap))
                                           )
                             ),
                      np.multiply(2,A_cap))
    #print(F_pos)
    #import ipdb; ipdb.set_trace()
    F_neg = np.divide(-np.subtract(
                                B_cap,
                                np.sqrt(
                                            np.subtract(np.power(B_cap,2.),
                                                             4*np.multiply(A_cap,C_cap))
                                            )),
                      np.multiply(2,A_cap))
    #print(F_neg)
    #import ipdb; ipdb.set_trace()

    return F_pos, F_neg


class FehRetrieval():
        """
        Find a Fe/H value for a combination of coefficients
        from the MCMC chain, and sample from the Balmer and
        CaIIK EWs, given their errors

        Parameters:
            write_out_filename (str): the file name of everything, incl. retrieved Teff and Fe/H

        Returns:
            final_table (DataFrame): dataframe equivalent of the written csv file, for unit testing
            [csv is also written to disk]
        """

        def __init__(self,
                    module_name,
                    file_good_ew_read,
                    file_calib_read,
                    dir_retrievals_write,
                    file_retrievals_write):

            self.name = module_name
            self.file_good_ew_read = file_good_ew_read
            self.file_calib_read = file_calib_read
            self.dir_retrievals_write = dir_retrievals_write
            self.file_retrievals_write = file_retrievals_write


        def run_step(self, attribs = None):

            #calib_read_file = attribs["data_dirs"]["DIR_SRC"] + attribs["file_names"]["CALIB_SOLN"]
            calib_read_file = self.file_calib_read
            calib_file = calib_read_file ## ## vestigial?
            mcmc_chain = Table.read(calib_file, hdu=1)
            #write_pickle_dir = attribs["data_dirs"]["DIR_PICKLE"]
            write_pickle_dir = self.dir_retrievals_write
            #good_ew_info_file = attribs["data_dirs"]["DIR_EW_PRODS"]+attribs["file_names"]["RESTACKED_EW_DATA_W_NET_BALMER_ERRORS"]
            good_ew_info_file = self.file_good_ew_read
            #write_out_filename = attribs["data_dirs"]["DIR_BIN"]+attribs["file_names"]["RETRIEVED_VALS"]
            write_out_filename = self.file_retrievals_write
            ew_file = good_ew_info_file
            ew_data = pd.read_csv(ew_file).copy(deep=True)
            hdul = fits.open(calib_file)
            soln_header = hdul[1].header

            # if write directories do not exist, create them
            make_dir(write_pickle_dir)
            make_dir(write_out_filename)

            ## ## find/input EWs for a single spectrum here; use stand-in EWs for the moment
            # number of samples to take within the Gaussian errors around Balmer, CaIIK EWs
            #N_EW_samples = 1 # vestigial

            # loop over samples in the MCMC chain
            N_MCMC_samples = len(mcmc_chain)

            # check if there is already something else in pickle directory
            preexisting_file_list = glob.glob(write_pickle_dir + "/*.{*}")
            if (len(preexisting_file_list) != 0):
                logging.info("------------------------------")
                logging.info("Directory to pickle Fe/H retrievals to is not empty!!")
                logging.info(write_pickle_dir)
                logging.info("------------------------------")
                if prompt_user:
                    input("Do what you want with those files, then hit [Enter]")

            # add columns to data table to include retrieved Fe/H values
            ew_data["feh_retrieved"] = np.nan
            ew_data["err_feh_retrieved"] = np.nan
            ew_data["teff_retrieved"] = np.nan

            # loop over the rows of the table of good EW data, with each row
            # corresponding to a spectrum; note that, depending on user setting
            # 'groupby,' this could either be a parent spectrum or individual noise-churned
            # spectra; the stuff that gets printed to screen here just uses the parent
            # spectrum name
            for row_num in range(0,len(ew_data)):

                print("-------------")
                print(row_num)
                #import ipdb; ipdb.set_trace()
                logging.info("Finding Fe/H for spectrum " + str(ew_data.iloc[row_num]["orig_spec_file_name"]))

                Balmer_EW = ew_data.iloc[row_num]["EW_Balmer"]
                CaIIK_EW = ew_data.iloc[row_num]["EW_CaIIK"]

                # set the offset (note mu=0; this is a relative offset)
                # (vestigial)
                offset_H = 0 # np.random.normal(loc = 0.0, scale = err_Balmer_EW)
                offset_K = 0 # np.random.normal(loc = 0.0, scale = err_CaIIK_EW)

                # initialize array
                feh_sample_array = np.nan*np.ones((N_MCMC_samples, 1))

                # find one value of Fe/H given those samples in Balmer and CaIIK EWs
                #import ipdb; ipdb.set_trace()
                if (len(mcmc_chain.columns)==4):

                    try:

                        feh_sample = feh_layden_vector(coeff_a = mcmc_chain["a"],
                                          coeff_b = mcmc_chain["b"],
                                          coeff_c = mcmc_chain["c"],
                                          coeff_d = mcmc_chain["d"],
                                          H = Balmer_EW,
                                          K = CaIIK_EW)

                    except:

                        print("Convergence failed")
                        continue

                elif (len(mcmc_chain.columns)==8):

                    feh_sample = feh_abcdfghk_vector(coeff_a = mcmc_chain["a"],
                                      coeff_b = mcmc_chain["b"],
                                      coeff_c = mcmc_chain["c"],
                                      coeff_d = mcmc_chain["d"],
                                      coeff_f = mcmc_chain["f"],
                                      coeff_g = mcmc_chain["g"],
                                      coeff_h = mcmc_chain["h"],
                                      coeff_k = mcmc_chain["k"],
                                      H = Balmer_EW,
                                      K = CaIIK_EW)

                    # just want one of the two roots
                    feh_sample = feh_sample[1]

                    # check for NaN answers
                    x=feh_sample
                    x = x[~np.isnan(x)]
                    frac_finite = len(x)/len(feh_sample)

                    # if less than 0.95 of the metallicities converged for this
                    # spectrum, consider it not to have converged
                    #import ipdb; ipdb.set_trace()
                    if (frac_finite < 0.95):

                        print("Convergence failed")
                        continue

                    print("-----")


                # write the results (note this pickle file just corresponds to one spectrum)
                #import ipdb; ipdb.set_trace()
                print("[Fe/H] = ", np.nanmedian(feh_sample))
                ew_data.at[row_num,"feh_retrieved"] = np.nanmedian(feh_sample)
                ew_data.at[row_num,"err_feh_retrieved"] = np.std(feh_sample)
                ew_data.at[row_num,"teff_retrieved"] = np.add(
                                                                    np.multiply(ew_data.iloc[row_num]["EW_Balmer"],soln_header["SLOPE_M"]),
                                                                    soln_header["YINT_B"]
                                                                    )

            final_table = ew_data.copy()

            final_table.to_csv(write_out_filename, index=False)
            logging.info("Wrote out retrieved [Fe/H] and Teff to " + write_out_filename)

            return final_table
