#!/usr/bin/env python
# coding: utf-8

# This reads in Balmer line widths and plots the scaling with respect to H-delta

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from cycler import cycler

file_name = "/Users/bandari/Documents/git.repos/rrlfe/ew_products/all_data_input_mcmc_20220130_run_1.csv"
#file_name = "/Users/bandari/Documents/git.repos/rrlfe/ew_products/all_data_input_mcmc_calib_run_long_100_spectra_from_synthetic_started_20220131_smo_files.csv"

n = 4
#color = plt.cm.tab10(np.linspace(0, 1,n))
#colormap = plt.get_cmap('Dark2')
color=iter(cm.viridis(np.linspace(0,1,n)))
matplotlib.rcParams['axes.prop_cycle'] = cycler('color', color)
#matplotlib.rcParams['axes.prop_cycle'] = cycler(color="Dark2")
#matplotlib.rcParams['axes.prop_cycle'] = cycler('color', plt.cm.tab20c.colors)
df = pd.read_csv(file_name)

plt.clf()
plt.figure(figsize=(10,7))
plt.scatter(df["EW_Hdelta"], np.add(df["EW_Heps"],10), s=12, label="W"+r"$\epsilon$+10")
plt.scatter(df["EW_Hdelta"], np.add(df["EW_Hbeta"],5), s=12, label="W"+r"$\beta$+5")
plt.scatter(df["EW_Hdelta"], df["EW_Hgamma"], s=12, label="W"+r"$\gamma$")
# note by plotting error bar points, color scheme conveniently repeats colors in order
plt.errorbar([5], [2], markersize=7, fmt="", mfc='white', capsize=3,
            xerr=np.median(df["err_EW_Hdelta_from_robo"]),
            yerr=np.median(df["err_EW_Heps_from_robo"]))
plt.errorbar([7], [3], markersize=7, fmt="", mfc='white', capsize=3,
            xerr=np.median(df["err_EW_Hdelta_from_robo"]),
            yerr=np.median(df["err_EW_Hbeta_from_robo"]))
plt.errorbar([9], [4], markersize=7, fmt="", mfc='white', capsize=3,
            xerr=np.median(df["err_EW_Hdelta_from_robo"]),
            yerr=np.median(df["err_EW_Hgamma_from_robo"]))
plt.xlim([1.2,15.0])
plt.xlabel(r"$W_{\delta}$"+" "+"($\AA$)", fontsize=35)
plt.ylabel("$W$"+" "+"($\AA$)", fontsize=35)
plt.legend(fontsize=25)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.ylim([0,26])
plt.tight_layout()

file_write_name = "junk.pdf"
plt.savefig(file_write_name)
print("Wrote out", file_write_name)
