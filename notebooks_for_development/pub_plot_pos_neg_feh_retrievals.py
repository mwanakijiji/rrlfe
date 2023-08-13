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

# read in data which would be input into the MCMC
stem = '/Users/bandari/Documents/git.repos/rrlfe/'
df_abcd = pd.read_csv(stem + 'notebooks_for_development/data/retrieved_vals_corrected_synth_abcd_20230813.csv')
df_abcdfghk = pd.read_csv(stem + 'notebooks_for_development/data/retrieved_vals_synth_abcdfghk_raw_20230813.csv')

# add cols indicating true logg, teff, feh
df_abcd['teff_true'] = df_abcd['orig_spec_file_name'].str[0:4]
df_abcd['logg_true'] = df_abcd['orig_spec_file_name'].str[4:6]
df_abcd['feh_true'] = 0.1*df_abcd['orig_spec_file_name'].str[6:9].str.replace('m','-').str.replace('p','+').astype(float)

df_abcdfghk['teff_true'] = df_abcdfghk['orig_spec_file_name'].str[0:4]
df_abcdfghk['logg_true'] = df_abcdfghk['orig_spec_file_name'].str[4:6]
df_abcdfghk['feh_true'] = 0.1*df_abcdfghk['orig_spec_file_name'].str[6:9].str.replace('m','-').str.replace('p','+').astype(float)

import ipdb; ipdb.set_trace()

plt.clf()
#plt.figure(figsize=(7,14))
plt.scatter(df_abcd["feh_true"],df_abcd["feh_retrieved"],facecolors="none",
            edgecolors="k",label="abcd", zorder=2)
plt.scatter(df_abcdfghk["feh_true"],df_abcdfghk["feh_retrieved"],facecolors="orange",edgecolors="r",
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
plt.ylim([-3.,5.])
#plt.show()
plt.savefig(file_name_write)
print("Wrote", file_name_write)
