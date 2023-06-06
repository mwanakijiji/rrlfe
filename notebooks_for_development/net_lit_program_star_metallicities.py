#!/usr/bin/env python
# coding: utf-8

# This takes metallicities from Layden 94 and converts them into a "net" high-res 
# literature value, based on our mapping in the style of Chadid+ 2017
# (Note this is not the [Fe/H] retrieval with our calibration; it's just the next 
# high-res value)

# Created 2022 Aug 2 by E.S.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# set linear relation values, based on >200 data points, offsets, and best-fitting 
# using error in x and y in Matlab
# (note added later: _matlab is actually obsolete here; these vals are generated in make_high_res_feh_basis.py)
m_matlab = 1.0401625282974445
b_matlab = -0.060221399367776464
sigma_m_matlab = 0.02568848255048297
sigma_b_matlab = 0.03499115602745869

file_name = "/Users/bandari/Documents/git.repos/rrlfe/src/high_res_feh/layden_1994_abundances.dat"
df_layden = pd.read_csv(file_name)


def prop_err_feh(feh_lay, err_feh_lay, m, err_m, err_b):
    '''
    Finds error on mapped [Fe/H], given uncertainties in
    1. Layden 94 value
    2. slope of previously-established fit
    3. y-intercept of " "
    
    INPUTS:
    feh_lay: Layden 94 [Fe/H] value
    err_feh_lay: error in "
    m: slope
    err_m: error in "
    b: y-intercept
    err_b: error in "
    '''
    
    sig_feh = np.sqrt(
                    np.add(
                        np.add(
                            np.multiply(np.power(feh_lay,2.),np.power(err_m,2.)),
                            np.multiply(np.power(m,2.),np.power(err_feh_lay,2.))
                        ),
                        np.power(err_b,2.)
                    )
                )

    return sig_feh


df_layden["feh_mapped"] = np.add(np.multiply(m_matlab,df_layden["feh"]),b_matlab)

df_layden["err_feh_mapped"] = prop_err_feh(feh_lay=df_layden["feh"], 
                             err_feh_lay=df_layden["err_feh"], 
                             m=m_matlab, 
                             err_m=sigma_m_matlab, 
                             err_b=sigma_b_matlab)

'''
plt.errorbar(df_layden["feh"], df_layden["feh_mapped"], 
             yerr=df_layden["err_feh"], xerr=df_layden["err_feh_mapped"], 
             linestyle="")
plt.show()
'''

pd.set_option('display.max_rows', 1000)
print(df_layden)

file_write = "junk_mapped_program_fehs.csv"
df_layden.to_csv(file_write)
print("Wrote " + file_write)
