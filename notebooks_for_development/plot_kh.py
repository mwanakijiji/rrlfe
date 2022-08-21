# This makes a KH plot with isometallicity contours

# Created from parent 2022 Jan. 30 by E.S.


# #### In the following, we plot fits in KH space and write out data including the BIC to select
# #### the best model among variations that consider up to third-degree terms involving H (Balmer
# #### EW) and F (Fe/H), viz.
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
import seaborn as sns
from astropy import stats
from scipy import optimize
import matplotlib
# matplotlib.use('Agg') # necessary in the cloud
import matplotlib.pyplot as plt

# set the coefficients of the model
coeff_array= np.array([26.458560990753856,-2.902133161010684,13.111956399236913,-1.2137255854235038,
                    0.09607072758758611,1.5487308225785184,0.032702627768572155,-0.08555553824310289,0,0])
#coeff_array = np.array([1.,1.,1.,1.,1.,1.,1.,1.,0,0])

# read in the data points to be overplotted
stem = "/Users/bandari/Documents/git.repos/rrlfe/"
data_points_read = stem + "rrlfe_io_20220811_job_594776/rrlfe_io/ew_products/all_data_input_mcmc.csv"
df_choice = pd.read_csv(data_points_read)

# read in full list of spectra reduced (so that we can pinpoint the ones that failed the fitting process)
data_start = stem + "src/synthetic_spectra_without_feh_m30.list"
df_start = pd.read_csv(data_start)

# read in ALL EW data (good and bad), to plot and/or troubleshoot the failed fits
'''
# not sure if useful
good_bad = stem + "rrlfe_io_20220811_job_594776/rrlfe_io/ew_products/all_ew_info.csv"
df_goodbad = pd.read_csv(good_bad)
'''

# merge but return the non-overlapping spectrum names (print manually)
indicator_merge = df_start.merge(df_choice, on='orig_spec_file_name', how='outer', indicator=True)
df_lost = indicator_merge[indicator_merge['_merge']=='left_only'] # 'lost' spectra

#
#df_lost["feh_x"]
#import ipdb; ipdb.set_trace()

# set the file name to write
file_name_write = "junk.pdf"

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


# make some isometallicity lines for the plot
isometal_balmer_abcissa = np.arange(2,15.0,0.2)
retrieved_K_isometal_neg3pt0 = expanded_layden_all_coeffs(coeff_array=coeff_array, H=isometal_balmer_abcissa, F=-3.0)
retrieved_K_isometal_neg2pt5 = expanded_layden_all_coeffs(coeff_array=coeff_array, H=isometal_balmer_abcissa, F=-2.5)
retrieved_K_isometal_neg2pt0 = expanded_layden_all_coeffs(coeff_array=coeff_array, H=isometal_balmer_abcissa, F=-2.)
retrieved_K_isometal_neg1pt5 = expanded_layden_all_coeffs(coeff_array=coeff_array, H=isometal_balmer_abcissa, F=-1.5)
retrieved_K_isometal_neg1pt0 = expanded_layden_all_coeffs(coeff_array=coeff_array, H=isometal_balmer_abcissa, F=-1.)
retrieved_K_isometal_neg0pt5 = expanded_layden_all_coeffs(coeff_array=coeff_array, H=isometal_balmer_abcissa, F=-0.5)
retrieved_K_isometal_pos0pt0 = expanded_layden_all_coeffs(coeff_array=coeff_array, H=isometal_balmer_abcissa, F=0.0)
retrieved_K_isometal_pos0pt2 = expanded_layden_all_coeffs(coeff_array=coeff_array, H=isometal_balmer_abcissa, F=0.2)


plt.clf()
# kludge to make legend come out right
df_choice["[Fe/H]"] = df_choice["feh"]
df_choice["log(g)"] = df_choice["logg"]

cmap = "Reds"
sns.set(font_scale=1.9)
sns.set_style(style='white')
sns.set_style('ticks')

g = sns.relplot(
    data=df_choice,
    x="EW_Balmer", y="EW_CaIIK",
    hue="[Fe/H]", size="log(g)", edgecolor="k", legend="full",
    palette=cmap, sizes=(30,160), alpha=0.8, zorder=2
)
#import ipdb; ipdb.set_trace()
# plot points to show median error bars
# define the line along which they will lie
balmer_dummy = np.arange(7,16,1)
contour_4_points = np.add(8.,expanded_layden_all_coeffs(coeff_array=coeff_array, H=balmer_dummy, F=0.2))
bool_p02 = (df_choice["feh"] == 0.2)
#import ipdb; ipdb.set_trace()
plt.errorbar(balmer_dummy[0],[20],
                xerr=np.median(df_choice["err_EW_Balmer_from_Robo"][bool_p02]),
                yerr=np.median(df_choice["err_EW_CaIIK_from_robo"][bool_p02]), ecolor="k") # [Fe/H] = +0.2
plt.text(balmer_dummy[0]+0.1,20+0.5,"[Fe/H] = +0.2")
'''
bool_p00 = (df_choice["feh"] == 0.0)
plt.errorbar(balmer_dummy[1],contour_4_points[1],
                xerr=np.median(df_choice["err_EW_Balmer_from_Robo"][bool_p00]),
                yerr=np.median(df_choice["err_EW_CaIIK_from_robo"][bool_p00]), ecolor="k")  # [Fe/H] = +0.0

bool_m05 = (df_choice["feh"] == -0.5)
plt.errorbar(balmer_dummy[2],contour_4_points[2],
                xerr=np.median(df_choice["err_EW_Balmer_from_Robo"][bool_m05]),
                yerr=np.median(df_choice["err_EW_CaIIK_from_robo"][bool_m05]), ecolor="k") # [Fe/H] = -0.5
'''
bool_m10 = (df_choice["feh"] == -1.0)
plt.errorbar(balmer_dummy[3],[15],
                xerr=np.median(df_choice["err_EW_Balmer_from_Robo"][bool_m10]),
                yerr=np.median(df_choice["err_EW_CaIIK_from_robo"][bool_m10]), ecolor="k") # [Fe/H] = -1.0
plt.text(balmer_dummy[3]+0.1,15+0.5,"-1.0")
'''
bool_m15 = (df_choice["feh"] == -1.5)
plt.errorbar(balmer_dummy[4],contour_4_points[4],
                xerr=np.median(df_choice["err_EW_Balmer_from_Robo"][bool_m15]),
                yerr=np.median(df_choice["err_EW_CaIIK_from_robo"][bool_m15]), ecolor="k")  # [Fe/H] = -1.5

bool_m20 = (df_choice["feh"] == -2.0)
plt.errorbar(balmer_dummy[5],contour_4_points[5],
                xerr=np.median(df_choice["err_EW_Balmer_from_Robo"][bool_m20]),
                yerr=np.median(df_choice["err_EW_CaIIK_from_robo"][bool_m20]), ecolor="k")  # [Fe/H] = -2.0
'''
bool_m25 = (df_choice["feh"] == -2.5)
plt.errorbar(balmer_dummy[6],[10],
                xerr=np.median(df_choice["err_EW_Balmer_from_Robo"][bool_m25]),
                yerr=np.median(df_choice["err_EW_CaIIK_from_robo"][bool_m25]), ecolor="k")  # [Fe/H] = -2.5
plt.text(balmer_dummy[6]+0.1,10+0.5,"-2.5")

# plot isometallicity contours
success_rate_x = 14.5
lim_abcissa = 2 # for staggering the ends of the lines
y_offset = -0.2 # ibid
feh_nonred = np.array([-3.0,-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.2])
plt.text(isometal_balmer_abcissa[0]-0.65,retrieved_K_isometal_pos0pt2[0]+2,"[Fe/H]")
plt.text(success_rate_x+0.25,retrieved_K_isometal_pos0pt2[-1]+1.5,"S/F", fontsize=16)
p02 = sns.lineplot(x=isometal_balmer_abcissa[:-lim_abcissa], y=retrieved_K_isometal_pos0pt2[:-lim_abcissa], color="k", alpha=0.5, zorder=0)
plt.text(isometal_balmer_abcissa[0]-0.6,retrieved_K_isometal_pos0pt2[0],"+0.2")
plt.text(success_rate_x,retrieved_K_isometal_pos0pt2[-1]+y_offset,"19/8",fontsize=14) # successes/failures in fit
p00 = sns.lineplot(x=isometal_balmer_abcissa, y=retrieved_K_isometal_pos0pt0, color="k", alpha=0.5, zorder=0)
plt.text(isometal_balmer_abcissa[0]-0.6,retrieved_K_isometal_pos0pt0[0],"+0.0")
plt.text(success_rate_x+0.5,retrieved_K_isometal_pos0pt0[-1]+y_offset,"23/4",fontsize=14) # successes/failures in fit
m05 = sns.lineplot(x=isometal_balmer_abcissa[:-lim_abcissa], y=retrieved_K_isometal_neg0pt5[:-lim_abcissa], color="k", alpha=0.5, zorder=0)
plt.text(isometal_balmer_abcissa[0]-0.6,retrieved_K_isometal_neg0pt5[0],"-0.5")
plt.text(success_rate_x,retrieved_K_isometal_neg0pt5[-1]+y_offset,"26/1",fontsize=14) # successes/failures in fit
m10 = sns.lineplot(x=isometal_balmer_abcissa, y=retrieved_K_isometal_neg1pt0, color="k", alpha=0.5, zorder=0)
plt.text(isometal_balmer_abcissa[0]-0.6,retrieved_K_isometal_neg1pt0[0],"-1.0")
plt.text(success_rate_x+0.5,retrieved_K_isometal_neg1pt0[-1]+y_offset,"27/0",fontsize=14) # successes/failures in fit
m15 = sns.lineplot(x=isometal_balmer_abcissa[:-lim_abcissa], y=retrieved_K_isometal_neg1pt5[:-lim_abcissa], color="k", alpha=0.5, zorder=0)
plt.text(isometal_balmer_abcissa[0]-0.6,retrieved_K_isometal_neg1pt5[0],"-1.5")
plt.text(success_rate_x,retrieved_K_isometal_neg1pt5[-1]+y_offset,"27/0",fontsize=14) # successes/failures in fit
m20 = sns.lineplot(x=isometal_balmer_abcissa, y=retrieved_K_isometal_neg2pt0, color="k", alpha=0.5, zorder=0)
plt.text(isometal_balmer_abcissa[0]-0.6,retrieved_K_isometal_neg2pt0[0],"-2.0")
plt.text(success_rate_x+0.5,retrieved_K_isometal_neg2pt0[-1]+y_offset,"27/0",fontsize=14) # successes/failures in fit
m25 = sns.lineplot(x=isometal_balmer_abcissa[:-lim_abcissa], y=retrieved_K_isometal_neg2pt5[:-lim_abcissa], color="k", alpha=0.5, zorder=0)
plt.text(isometal_balmer_abcissa[0]-0.6,retrieved_K_isometal_neg2pt5[0],"-2.5")
plt.text(success_rate_x,retrieved_K_isometal_neg2pt5[-1]+y_offset,"27/0",fontsize=14) # successes/failures in fit

plt.xlim([1,16])
plt.legend(loc="upper right", ncol=3)

g.fig.set_size_inches(28,8)

g.set_ylabels(r"$W_{K}$"+" ($\AA$)", fontsize=22)
g.set_xlabels(r"$W_{B}$"+" ($\AA$)", fontsize=22)
g.set(ylim=(0, 25))

g.savefig(file_name_write, bbox_inches='tight')
print("Wrote", file_name_write)
