#!/usr/bin/env python
# coding: utf-8

# Makes a meta-plot of various Fe/H retrievals

# Created 2023 Feb 5

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
from scipy.stats import binned_statistic_2d

# subplot arrangement

# plot 1:
# [0]: rrlfe vs. SSPP (single-epoch)
# [1]: rrlfe vs. SSPP (coadded)

# plot 2:
# [1,0]: rrlfe vs. Liu+
# [1,0]: rrlfe vs. Whitten+
# [2,0]: rrlfe vs. Li+

stem = '/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/'

'''
df_sspp_single = pd.read_csv("comparison_sspp_single_20230604.csv") # source: examine_sspp_output.py
df_sspp_coadded = pd.read_csv("comparison_sspp_coadded_20230604.csv") # source: examine_sspp_output.py
df_liu_2020 = pd.read_csv("comparison_liu_2020_20230604.csv") # source: lamost_comparison.py 
df_whitten = pd.read_csv("comparison_whitten_20230604.csv") # source: inspect_whitten_catalog.py
df_li_2023 = pd.read_csv("comparison_lietal2023_20230608.csv") # source: cross_ref_sdss_lietal2023_retrievals.py
'''
df_sspp_single = pd.read_csv("comparison_sspp_single_20230604.csv") # source: examine_sspp_output.py
df_sspp_coadded = pd.read_csv("comparison_sspp_coadded_20230604.csv") # source: examine_sspp_output.py
df_liu_2020 = pd.read_csv(stem + "data/comparison_liu_2020_w_s2n_20230604.csv") # source: lamost_comparison.py 
df_whitten = pd.read_csv(stem + "data/comparison_whitten_w_s2n_20230604.csv") # source: inspect_whitten_catalog.py
df_li_2023 = pd.read_csv(stem + "data/comparison_lietal_2023_w_s2n_20230608.csv") # source: cross_ref_sdss_lietal2023_retrievals.py

fig, axes = plt.subplots(ncols=2, nrows=1, sharex='row', sharey='row', figsize=(10, 5))
#matplotlib.rc('xtick', labelsize=40) 
#matplotlib.rc('ytick', labelsize=20) 

# Fe/H limits
xlim = [-3,0]
ylim = [-3,0]

# [0,0]: rrlfe vs. SSPP (single-epoch)
# [0,1]: rrlfe vs. SSPP (coadded)
# [1,0]: rrlfe vs. Liu+
# [1,1]: rrlfe vs. Whitten+
# [2,0]: rrlfe vs. Li+

char_size = 20
loc = ticker.MultipleLocator(base=1.0) # for ticks

# coloration cut-offs to indicate S/N
v_min = 10
v_max = 50

# rrlfe vs. SSPP (single-epoch)
hb = axes[0].hexbin(df_sspp_single["feh_sspp_single"],df_sspp_single["feh_rrlfe"], extent=(-4.,1.,-4.,1.), linewidths=0.01)
axes[0].plot([-3, 0], [-3, 0], linestyle="--", color="white", zorder=1, label="1-to-1")
axes[0].set_xlim(xlim)
axes[0].set_ylim(ylim)
axes[0].set(adjustable='box', aspect='equal')
#axes[0].set_xlabel("SSPP (single-epoch)", fontsize = char_size)
axes[0].set_ylabel("[Fe/H], rrlfe", fontsize = char_size-2)
# best-fit coeffs
idx_sane_single_epoch = (np.isfinite(df_sspp_single["feh_sspp_single"]) & np.isfinite(df_sspp_single["feh_rrlfe"])) & \
        ((np.abs(df_sspp_single["feh_rrlfe"]) < 5.) & (np.abs(df_sspp_single["feh_sspp_single"]) < 5.))
coeffs_single_epoch = np.polyfit(df_sspp_single["feh_sspp_single"][idx_sane_single_epoch], df_sspp_single["feh_rrlfe"][idx_sane_single_epoch], deg=1)
axes[0].plot([-3, 0], [coeffs_single_epoch[0]*(-3.0)+coeffs_single_epoch[1],coeffs_single_epoch[0]*(0.0)+coeffs_single_epoch[1]], 
               linestyle="-", color="white", zorder=1)
axes[0].annotate("              \n(single-epoch)", xy=(-1.55, -2.8), xycoords='data', fontsize = char_size, color='white')
axes[0].tick_params(axis='both', which='major', labelsize=char_size-2)
axes[0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[0].xaxis.set_major_locator(loc)
axes[0].yaxis.set_major_locator(loc)
#axes[0].xaxis.set_tick_params(labelbottom=False)
axes[0].tick_params(width=2, length=8)
axes[0].set_xlabel("[Fe/H], SSPP", fontsize = char_size)

# rrlfe vs. SSPP (coadded)
hb = axes[1].hexbin(df_sspp_coadded["feh_sspp_coadded"],df_sspp_coadded["feh_rrlfe"], extent=(-4.,1.,-4.,1.), linewidths=0.01)
axes[1].plot([-3, 0], [-3, 0], linestyle="--", color="white", zorder=1, label="1-to-1")
axes[1].set_xlim(xlim)
axes[1].set_ylim(ylim)
#axes[1].set_xlabel("SSPP (coadded)", fontsize = char_size)
axes[1].set(adjustable='box', aspect='equal')
# best-fit coeffs
idx_sane_coadded = (np.isfinite(df_sspp_coadded["feh_sspp_coadded"]) & np.isfinite(df_sspp_coadded["feh_rrlfe"])) & \
        ((np.abs(df_sspp_coadded["feh_rrlfe"]) < 5.) & (np.abs(df_sspp_coadded["feh_sspp_coadded"]) < 5.))
coeffs_coadded = np.polyfit(df_sspp_coadded["feh_sspp_coadded"][idx_sane_coadded], df_sspp_coadded["feh_rrlfe"][idx_sane_coadded], deg=1)
axes[1].plot([-3, 0], [coeffs_coadded[0]*(-3.0)+coeffs_coadded[1],coeffs_coadded[0]*(0.0)+coeffs_coadded[1]], linestyle="-", color="white", zorder=1)
axes[1].annotate("        \n(coadded)", xy=(-1.15, -2.8), xycoords='data', fontsize = char_size, color='white')
axes[1].tick_params(axis='both', which='major', labelsize=char_size-2)
axes[1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[1].xaxis.set_major_locator(loc)
axes[1].yaxis.set_major_locator(loc)
#axes[1].xaxis.set_tick_params(labelbottom=False)
axes[1].tick_params(width=2, length=8)
axes[1].set_xlabel("[Fe/H], SSPP", fontsize = char_size)

#plt.subplots_adjust(wspace=0.0, hspace=0.2)
plt.tight_layout()

#plt.show()
plot_file_name = "junk1.png"
plt.savefig(plot_file_name)
print("Wrote",plot_file_name)

fig, axes = plt.subplots(ncols=2, nrows=3, sharex='row', sharey='row', figsize=(10, 15))

# rrlfe vs. Liu+
hb = axes[0,0].hexbin(df_liu_2020["feh_liu"],df_liu_2020["feh_rrlfe"], extent=(-4.,1.,-4.,1.), linewidths=0.01)
axes[0,0].plot([-3, 0], [-3, 0], linestyle="--", color="white", zorder=1, label="1-to-1")
axes[0,0].set_xlim(xlim)
axes[0,0].set_ylim(ylim)
#axes[0,0].set_xlabel("Liu+ 2020", fontsize = char_size)
axes[0,0].set(adjustable='box', aspect='equal')
# best-fit coeffs
idx_sane_liu = (np.isfinite(df_liu_2020["feh_liu"]) & np.isfinite(df_liu_2020["feh_rrlfe"])) & \
        ((np.abs(df_liu_2020["feh_rrlfe"]) < 5.) & (np.abs(df_liu_2020["feh_liu"]) < 5.))
coeffs_liu = np.polyfit(df_liu_2020["feh_liu"][idx_sane_liu], df_liu_2020["feh_rrlfe"][idx_sane_liu], deg=1)
axes[0,0].plot([-3, 0],[coeffs_liu[0]*(-3.0)+coeffs_liu[1],coeffs_liu[0]*(0.0)+coeffs_liu[1]], linestyle="-", color="white", zorder=1)
axes[0,0].set_ylabel("[Fe/H], rrlfe", fontsize = char_size)
axes[0,0].annotate("Liu+ 2020", xy=(-1.15, -2.8), xycoords='data', fontsize = char_size, color='white')
axes[0,0].tick_params(axis='both', which='major', labelsize=char_size-2)
axes[0,0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[0,0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[0,0].xaxis.set_major_locator(loc)
axes[0,0].yaxis.set_major_locator(loc)
axes[0,0].tick_params(width=2, length=8)

# S/N, Liu+
x_bins = np.linspace(-3, 0, 50)
y_bins = np.linspace(-3, 0, 50)
ret = binned_statistic_2d(df_liu_2020['feh_liu'], df_liu_2020['feh_rrlfe'], df_liu_2020['s_to_n'], statistic=np.mean, bins=[x_bins, y_bins])
axes[0,1].imshow(ret.statistic.T, origin='lower', extent=(-3, 0, -3, 0), vmin=v_min, vmax=v_max, cmap='winter')
axes[0,1].plot([-3, 0],[coeffs_liu[0]*(-3.0)+coeffs_liu[1],coeffs_liu[0]*(0.0)+coeffs_liu[1]], linestyle="-", color="gray", zorder=1)
axes[0,1].plot([-3, 1], [-3, 1], linestyle="--", color="gray")
axes[0,1].annotate("S/N, Liu+ 2020", xy=(-1.6, -2.8), xycoords='data', fontsize = char_size, color='k')
axes[0,1].tick_params(axis='both', which='major', labelsize=char_size-2)
axes[0,1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[0,1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[0,1].xaxis.set_major_locator(loc)
axes[0,1].yaxis.set_major_locator(loc)
axes[0,1].tick_params(width=2, length=8)
#axes[0,1].colorbar()


# rrlfe vs. Li+
hb = axes[1,0].hexbin(df_li_2023["feh_lietal2023"],df_li_2023["feh_rrlfe"], extent=(-4.,1.,-4.,1.), linewidths=0.01)
axes[1,0].plot([-3, 0], [-3, 0], linestyle="--", color="white", zorder=1, label="1-to-1")
axes[1,0].set_xlim(xlim)
axes[1,0].set_ylim(ylim)
#axes[1,0].set_xlabel("Liu+ 2020", fontsize = char_size)
axes[1,0].set(adjustable='box', aspect='equal')
# best-fit coeffs
idx_sane_lietal2023 = (np.isfinite(df_li_2023["feh_lietal2023"]) & np.isfinite(df_li_2023["feh_rrlfe"])) & \
        ((np.abs(df_li_2023["feh_rrlfe"]) < 5.) & (np.abs(df_li_2023["feh_lietal2023"]) < 5.))
coeffs_lietal2023 = np.polyfit(df_li_2023["feh_lietal2023"][idx_sane_lietal2023], df_li_2023["feh_rrlfe"][idx_sane_lietal2023], deg=1)
axes[1,0].plot([-3, 0],[coeffs_lietal2023[0]*(-3.0)+coeffs_lietal2023[1],coeffs_lietal2023[0]*(0.0)+coeffs_lietal2023[1]], linestyle="-", color="white", zorder=1)
axes[1,0].set_ylabel("[Fe/H], rrlfe", fontsize = char_size)
axes[1,0].annotate("Li+ 2023", xy=(-1.05, -2.8), xycoords='data', fontsize = char_size, color='white')
axes[1,0].tick_params(axis='both', which='major', labelsize=char_size-2)
axes[1,0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[1,0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[1,0].xaxis.set_major_locator(loc)
axes[1,0].yaxis.set_major_locator(loc)
axes[1,0].tick_params(width=2, length=8)

# S/N, Li+
x_bins = np.linspace(-3, 0, 50)
y_bins = np.linspace(-3, 0, 50)
ret = binned_statistic_2d(df_li_2023['feh_lietal2023'], df_li_2023['feh_rrlfe'], df_li_2023['s_to_n'], statistic=np.mean, bins=[x_bins, y_bins])
colorbarobj = axes[1,1].imshow(ret.statistic.T, origin='lower', extent=(-3, 0, -3, 0), vmin=v_min, vmax=v_max, cmap='winter') # plots + makes an object for the colorbar
axes[1,1].plot([-3, 0],[coeffs_lietal2023[0]*(-3.0)+coeffs_lietal2023[1],coeffs_lietal2023[0]*(0.0)+coeffs_lietal2023[1]], linestyle="-", color="gray", zorder=1)
axes[1,1].plot([-3.0, 0.], [-3.0, 0.], linestyle="--", color="gray")
axes[1,1].set_xlim([-3.0,0.])
axes[1,1].set_ylim([-3.0,0.])
axes[1,1].annotate("S/N, Li+ 2023", xy=(-1.5, -2.8), xycoords='data', fontsize = char_size, color='k')
axes[1,1].tick_params(axis='both', which='major', labelsize=char_size-2)
axes[1,1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[1,1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[1,1].xaxis.set_major_locator(loc)
axes[1,1].yaxis.set_major_locator(loc)
axes[1,1].tick_params(width=2, length=8)

# rrlfe vs. Whitten+ (& S/N)
#axes[2,1].scatter(df_whitten["feh_whitten"], df_whitten["feh_rrlfe"], s=10, color="k")
axes[2,1].scatter(df_whitten["feh_whitten"], df_whitten["feh_rrlfe"], c = df_whitten["s_to_n"], cmap="winter", vmin=v_min, vmax=v_max)
axes[2,1].plot([-3.0, 0.], [-3.0, 0.], linestyle="--", color="gray")
axes[2,1].set_xlim([-3.0,0.0])
axes[2,1].set_ylim([-3.0,0.0])
axes[2,1].set_xlabel("[Fe/H]", fontsize = char_size)
axes[2,1].set(adjustable='box', aspect='equal')
# best-fit coeffs (note metallicities covered are only within range [-3,0.])
idx_sane_whitten = (np.isfinite(df_whitten["feh_whitten"]) & np.isfinite(df_whitten["feh_rrlfe"])) & \
        ((np.abs(df_whitten["feh_rrlfe"]) < 3.) & (np.abs(df_whitten["feh_whitten"]) < 3.)) & \
        ((np.abs(df_whitten["feh_rrlfe"]) > 0.0) & (np.abs(df_whitten["feh_whitten"]) > 0.0))
coeffs_whitten = np.polyfit(df_whitten["feh_whitten"][idx_sane_whitten], df_whitten["feh_rrlfe"][idx_sane_whitten], deg=1)
axes[2,1].plot([-3.0,0.],[coeffs_whitten[0]*(-3.0)+coeffs_whitten[1],coeffs_whitten[0]*(0.)+coeffs_whitten[1]], linestyle="-", color="grey", zorder=1)
axes[2,1].tick_params(axis='both', which='major', labelsize=char_size-2)
axes[2,1].annotate("S/N, Whitten+ 2021", xy=(-2.1, -2.8), xycoords='data', fontsize = char_size, color='k')
axes[2,1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[2,1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[2,1].xaxis.set_major_locator(loc)
axes[2,1].yaxis.set_major_locator(loc)
axes[2,1].tick_params(width=2, length=8)
#axes[2,1].set_facecolor('lightgrey')

# all best-fit lines together
axes[2,0].plot([-3, 1], [-3, 1], linestyle="--", color="gray")
axes[2,0].set_xlim([-3.0,0.0])
axes[2,0].set_ylim([-3.0,0.0])
axes[2,0].set_xlabel("[Fe/H]", fontsize = char_size)
axes[2,0].set_ylabel("[Fe/H], rrlfe", fontsize = char_size)
axes[2,0].set(adjustable='box', aspect='equal')
#axes[2,0].plot([-3, 1], [-3, 1],[coeffs_rrlfe_synth[0]*(-3.0)+coeffs_rrlfe_synth[1],coeffs_rrlfe_synth[0]*(1.0)+coeffs_rrlfe_synth[1]], linestyle="-", zorder=0, label="rrlfe synthetic basis set (PLACEHOLDER)")
axes[2,0].plot([-3, 1], [coeffs_single_epoch[0]*(-3.0)+coeffs_single_epoch[1],coeffs_single_epoch[0]*(1.0)+coeffs_single_epoch[1]], linestyle="-", zorder=0, label="SSPP, single-epoch")
axes[2,0].plot([-3, 1], [coeffs_coadded[0]*(-3.0)+coeffs_coadded[1],coeffs_coadded[0]*(1.0)+coeffs_coadded[1]], linestyle="-", zorder=0, label="SSPP, coadded")
axes[2,0].plot([-3, 1], [coeffs_liu[0]*(-3.0)+coeffs_liu[1],coeffs_liu[0]*(1.0)+coeffs_liu[1]], linestyle="-", zorder=0, label="Liu+ 2020")
axes[2,0].plot([-3, 1], [coeffs_lietal2023[0]*(-3.0)+coeffs_lietal2023[1],coeffs_lietal2023[0]*(1.0)+coeffs_lietal2023[1]], linestyle="-", zorder=0, label="Li+ 2023")
axes[2,0].plot([-3, 1], [coeffs_whitten[0]*(-3.0)+coeffs_whitten[1],coeffs_whitten[0]*(1.0)+coeffs_whitten[1]], linestyle="-", zorder=0, label="Whitten+ 2021")
axes[2,0].legend(fontsize=13)
axes[2,0].tick_params(axis='both', which='major', labelsize=char_size-2)
axes[2,0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[2,0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.f'))
axes[2,0].xaxis.set_major_locator(loc)
axes[2,0].yaxis.set_major_locator(loc)
axes[2,0].tick_params(width=2, length=8)



plt.subplots_adjust(wspace=0.0, hspace=0.2)
plt.tight_layout()

#fig.colorbar(colorbarobj, ax=axes[0, :], shrink=0.6, location='top')

box = axes[0,0].get_position()
axColor = plt.axes([box.x0*6.5 + box.width * 1.05, box.y0, 0.01, box.height])
cbar = fig.colorbar(colorbarobj, cax = axColor, orientation="vertical")
cbar.ax.tick_params(labelsize=20)

box = axes[1,0].get_position()
axColor = plt.axes([box.x0*6.5 + box.width * 1.05, box.y0, 0.01, box.height])
cbar = fig.colorbar(colorbarobj, cax = axColor, orientation="vertical")
cbar.ax.tick_params(labelsize=20)

box = axes[2,0].get_position()
axColor = plt.axes([box.x0*6.5 + box.width * 1.05, box.y0, 0.01, box.height])
cbar = fig.colorbar(colorbarobj, cax = axColor, orientation="vertical")
cbar.ax.tick_params(labelsize=20)

#plt.show()
plot_file_name = "junk.png"
plt.savefig(plot_file_name, bbox_inches='tight')
print("Wrote",plot_file_name)