#!/usr/bin/env python
# coding: utf-8

# This makes plots showing the effective temperature retrievals based on synthetic spectra
# produced by R.W.

# Created from parent 2022 Jan 31 by E.S.

import pandas as pd
#from astropy.io import fits
from astropy.io.fits import getdata
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#get_ipython().run_line_magic('matplotlib', 'qt')

# name of csv file with EWs as produced by pipeline
ew_good_data_poststack_file_name = "/Users/bandari/Documents/git.repos/rrlfe/ew_products/" +                                     "all_data_input_mcmc_20220130_run_1.csv"

# read in
df_poststack = pd.read_csv(ew_good_data_poststack_file_name)

# array of metallicities and logg
feh_values = np.sort(df_poststack["feh"].drop_duplicates().values)
logg_values = np.sort(df_poststack["logg"].drop_duplicates().values)

# retrieved Balmer values, points colored by Fe/H AND sized by logg
plt.clf()

# vector for introducing some scatter in x, to avoid overlapping of data points
scatter_x = np.subtract(60*np.random.rand(len(df_poststack["teff"])),30)

colormap="Reds"
norm = matplotlib.colors.Normalize(vmin=np.min(feh_values),vmax=np.max(feh_values))

f, (a0, a1) = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [1, 1]}, sharex=True)

a0.axvspan(6000, 7250, color='y', alpha=0.5, lw=0,zorder=0) # RRLs in instability strip (Catelan 2015)
a1.axvspan(6000, 7250, color='y', alpha=0.5, lw=0,zorder=0)
a0.plot(df_poststack["teff"],df_poststack["teff"],zorder=1,linestyle="--",color="k")
a1.plot([np.min(df_poststack["teff"]),np.max(df_poststack["teff"])],[0,0],zorder=1,linestyle="--",color="k")

a0.scatter(np.add(scatter_x,df_poststack["teff"]),
            df_poststack["teff_bestfit"],
            c=df_poststack["feh"],
            s=np.power(np.divide(df_poststack["logg"],0.7),3),
            cmap=colormap, norm=norm, edgecolor="k",zorder=2)

a1.scatter(np.add(scatter_x,df_poststack["teff"]),
            np.subtract(df_poststack["teff_bestfit"],df_poststack["teff"]),
            c=df_poststack["feh"],
           s=np.power(np.divide(df_poststack["logg"],0.7),3),
            cmap=colormap, norm=norm, edgecolor="k",zorder=2)

# kludge to add legend while mapping colors correctly
for i in range(0,len(feh_values)):
    # indices reversed to get the order descending in the legend
    a0.scatter([0], [0], cmap=colormap, norm=norm, c=feh_values[-i-1],
                edgecolor="k", label=str(feh_values[-i-1]))

# logg plot; another kludge
# note indices reversed (-i-1) to get the order descending in the legend
l1 = a0.scatter([0], [0], c="w", norm=norm,
               s=np.power(np.divide(logg_values[-0-1],0.7),3),
                edgecolor="k")
l2 = a0.scatter([0], [0], c="w", norm=norm,
               s=np.power(np.divide(logg_values[-1-1],0.7),3),
                edgecolor="k")
l3 = a0.scatter([0], [0], c="w", norm=norm,
               s=np.power(np.divide(logg_values[-2-1],0.7),3),
                edgecolor="k")
loggpts = []
loggpts.append([l1,l2,l3])

f.canvas.draw() # need before legend to render

leg1 = a0.legend(loc='upper left', title="[Fe/H]", fontsize=12, title_fontsize=14)
# Add second legend for the maxes and mins.
# leg1 will be removed from figure
leg2 = a0.legend(loggpts[0],['3.0','2.5','2.0'], loc='lower right', title="log(g)", fontsize=12, title_fontsize=14)
# Manually add the first legend back
a0.add_artist(leg1)

a0.set_ylabel("Retrieved T$_{eff}$", fontsize=20)
a1.set_xlabel("Simulated T$_{eff}$", fontsize=20)
a1.set_ylabel("Residuals", fontsize=20)

a0.set_xlim([5500,8000])
a0.set_ylim([5500,8500])

#plt.show()
plt.savefig("junk.pdf")
