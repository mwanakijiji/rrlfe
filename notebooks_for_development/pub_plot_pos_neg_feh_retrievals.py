#!/usr/bin/env python
# coding: utf-8

# This tries a couple function-fitting routines to find the best-fit
# Layden coefficients if the input data is synthetic data with no errors

# Created 2020 Jan. 25 by E.S.
#
# #### $K = a + bH + cF + dHF + f(H^{2}) + g(F^{2}) + h(H^{2})F + kH(F^{2}) $
# #### $+ m(H^{3}) + n(F^{3}) $

import pandas as pd
import numpy as np
import astropy
import itertools
import multiprocessing
import random
import string
from astropy import stats
from scipy import optimize
import matplotlib.pyplot as plt

# read in data
stem = "/Users/bandari/Documents/git.repos/rrlfe/rrlfe_io_20220810/rrlfe_io/ew_products/"
df = pd.read_csv(stem + "all_data_input_mcmc.csv")

# remove the three really bad datapoints
'''
index_names1 = df[ df["original_spec_file_name"]=="600025p00.smo" ].index
df.drop(index_names1 , inplace=True)
index_names2 = df[ df["original_spec_file_name"]=="625025p02.smo" ].index
df.drop(index_names2 , inplace=True)
index_names3 = df[ df["original_spec_file_name"]=="600030p02.smo" ].index
df.drop(index_names3 , inplace=True)
index_names4 = df[ df["logg"]=="2.5" ].index # test of individual values of logg
df.drop(index_names4 , inplace=True)
df = df.reset_index(drop = True)
'''

df_choice = df

# set name of csv written-out data to which we will append BIC info
csv_file_name = "junk.csv"

# figure out all subsets of coefficients beyond [a,b,c,d]
'''
coeffs_strings = ["f","g","h","k","m","n"]
coeffs_strings_nan = ["NaN1"]
new_coeffs_6 = list(itertools.combinations(coeffs_strings, 6))
new_coeffs_5 = list(itertools.combinations(coeffs_strings, 5))
new_coeffs_4 = list(itertools.combinations(coeffs_strings, 4))
new_coeffs_3 = list(itertools.combinations(coeffs_strings, 3))
new_coeffs_2 = list(itertools.combinations(coeffs_strings, 2))
new_coeffs_1 = list(itertools.combinations(coeffs_strings, 1))
baseline = list(itertools.combinations(coeffs_strings_nan, 1)) # original Layden [a,b,c,d] coefficients only

# create the array of arrays, so we can map them across cores
new_coeffs_mother_array = [baseline,new_coeffs_1,new_coeffs_2,new_coeffs_3,new_coeffs_4,new_coeffs_5,new_coeffs_6]
'''

def expanded_layden_all_coeffs(coeff_array,H,F):

    # definition of coefficients as of 2020 Mar 9:
    # K = a + bH + cF + dHF + f(H^{2}) + g(F^{2}) + hF(H^{2}) + kH(F^{2}) + m(H^{3}) + n(F^{3})

    a_coeff = coeff_array[0]
    b_coeff = coeff_array[1]
    c_coeff = coeff_array[2]
    d_coeff = coeff_array[3]
    f_coeff = coeff_array[4]
    g_coeff = coeff_array[5]
    h_coeff = coeff_array[6]
    k_coeff = coeff_array[7]
    m_coeff = coeff_array[8]
    n_coeff = coeff_array[9]

    K_calc = a_coeff + b_coeff*H + c_coeff*F + d_coeff*H*F + \
        f_coeff*np.power(H,2.) + g_coeff*np.power(F,2.) + \
        h_coeff*F*np.power(H,2.) + k_coeff*H*np.power(F,2.) + \
        m_coeff*np.power(H,3.) + n_coeff*np.power(F,3.)

    return K_calc


def original_layden_abcd(coeff_array,H,F):

    # definition of coefficients as of 2020 Mar 9:
    # K = a + bH + cF + dHF + f(H^{2}) + g(F^{2}) + hF(H^{2}) + kH(F^{2}) + m(H^{3}) + n(F^{3})

    a_coeff = coeff_array[0]
    b_coeff = coeff_array[1]
    c_coeff = coeff_array[2]
    d_coeff = coeff_array[3]

    K_calc = a_coeff + b_coeff*H + c_coeff*F + d_coeff*H*F

    return K_calc


# Find some metallicities
H = df_choice["EW_Balmer"]
K = df_choice["EW_CaIIK"]

## calculate retrieved Fe/H using solution with [a,b,c,d,f,g,h,k], using logg3pt0_bic_output_20200322.csv
modified_soln_7_abcdfghk = [20.268216020772577,-2.103240677086597,9.682756160690241,-0.7990904214384392,0.07262757512570928,1.1242402933493127,0.020811006600471953,-0.05460696008885377]

coeff_a = modified_soln_7_abcdfghk[0]
coeff_b = modified_soln_7_abcdfghk[1]
coeff_c = modified_soln_7_abcdfghk[2]
coeff_d = modified_soln_7_abcdfghk[3]
coeff_f = modified_soln_7_abcdfghk[4]
coeff_g = modified_soln_7_abcdfghk[5]
coeff_h = modified_soln_7_abcdfghk[6]
coeff_k = modified_soln_7_abcdfghk[7]

A_cap = coeff_g + coeff_k*H
B_cap = coeff_c + coeff_d*H + coeff_h*np.power(H,2)
C_cap = coeff_a + coeff_b*H + coeff_f*np.power(H,2) - K

F_pos = np.divide(-B_cap + np.sqrt(np.power(B_cap,2.)-4*A_cap*C_cap),2*A_cap)
F_neg = np.divide(-B_cap - np.sqrt(np.power(B_cap,2.)-4*A_cap*C_cap),2*A_cap)


## and calculate retrieved Fe/H using just [a,b,c,d] (the Layden fit, but with our best-fit values)
original_layden_our_fit_soln_0_abcd = [12.51368502,-0.78716519,3.87785117,-0.24297523]
coeff_a_original = original_layden_our_fit_soln_0_abcd[0]
coeff_b_original = original_layden_our_fit_soln_0_abcd[1]
coeff_c_original = original_layden_our_fit_soln_0_abcd[2]
coeff_d_original = original_layden_our_fit_soln_0_abcd[3]
F_original_our_fit = np.divide(K-coeff_a_original-coeff_b_original*H,coeff_c_original+coeff_d_original*H)

plt.clf()
plt.clf()
#plt.figure(figsize=(7,14))
plt.scatter(df_choice["feh"],F_original_our_fit,facecolors="none",
            edgecolors="k",label="abcd", zorder=2)
plt.scatter(df_choice["feh"],F_pos,facecolors="orange",edgecolors="r",
            label="abcdfghk (+ solution)", zorder=3)
'''
for i in range(0,len(df)):
    plt.annotate(df["original_spec_file_name"].iloc[i],
                 xy=(df["final_feh_center"].iloc[i],F_pos.iloc[i]),
                 xytext=(df["final_feh_center"].iloc[i],F_pos.iloc[i]))
'''
#plt.scatter(df_choice["feh"],F_neg,label="abcdfghk: ($-$) solution")
plt.plot([-3,2], [-3,2], linestyle="--", zorder=0, color="gray")
plt.xlim([-3., 0.5])
plt.grid(zorder=1)
#plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel("[Fe/H], model spectrum", fontsize=20)
plt.ylabel("[Fe/H], retrieved", fontsize=20)
plt.xticks(np.arange(-3.,0.5,1.0), fontsize=14)
plt.yticks(np.arange(-3.,6.5,1.0), fontsize=14)
plt.legend(fontsize=14)
plt.tight_layout()

file_name_write = "junk.pdf"
plt.savefig(file_name_write)
print("Wrote", file_name_write)
