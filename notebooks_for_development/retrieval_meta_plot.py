#!/usr/bin/env python
# coding: utf-8

# Makes a meta-plot of various Fe/H retrievals

# Created 2023 Feb 5

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# subplot arrangement

# [0,0]: rrlfe vs. SSPP (single-epoch)
# [0,1]: rrlfe vs. SSPP (coadded)
# [1,0]: rrlfe vs. Liu+
# [1,1]: rrlfe vs. Whitten+
# [2,0]: rrlfe vs. Li+

df_sspp_single = pd.read_csv("junk_single.csv")
df_sspp_coadded = pd.read_csv("junk_coadded.csv")
df_liu_2020 = pd.read_csv("junk_liu.csv")
df_whitten = pd.read_csv("junk_whitten.csv")
df_li_2022 = pd.read_csv("junk_single.csv")

fig, axes = plt.subplots(ncols=2, nrows=3, sharex=True, sharey=True, figsize=(10, 15))

# Fe/H limits
xlim = [-4,1]
ylim = [-4,1]

# [0,0]: rrlfe vs. SSPP (single-epoch)
# [0,1]: rrlfe vs. SSPP (coadded)
# [1,0]: rrlfe vs. Liu+
# [1,1]: rrlfe vs. Whitten+
# [2,0]: rrlfe vs. Li+

char_size = 20

#import ipdb; ipdb.set_trace()

# rrlfe vs. SSPP (single-epoch)
hb = axes[0,0].hexbin(df_sspp_single["feh_sspp_single"],df_sspp_single["feh_rrlfe"], extent=(-4.,1.,-4.,1.), linewidths=0.01)
axes[0,0].plot([-4, 1], [-4, 1], linestyle="--", color="white", zorder=1, label="1-to-1")
axes[0,0].set_xlim(xlim)
axes[0,0].set_ylim(ylim)
axes[0,0].set(adjustable='box', aspect='equal')
axes[0,0].set_xlabel("SSPP (single-epoch)", fontsize = char_size)
axes[0,0].set_ylabel("rrlfe", fontsize = char_size)
# best-fit coeffs
idx_sane_single_epoch = (np.isfinite(df_sspp_single["feh_sspp_single"]) & np.isfinite(df_sspp_single["feh_rrlfe"])) & \
        ((np.abs(df_sspp_single["feh_rrlfe"]) < 5.) & (np.abs(df_sspp_single["feh_sspp_single"]) < 5.))
coeffs_single_epoch = np.polyfit(df_sspp_single["feh_sspp_single"][idx_sane_single_epoch], df_sspp_single["feh_rrlfe"][idx_sane_single_epoch], deg=1)
axes[0,0].plot([-4.0,1.0],[coeffs_single_epoch[0]*(-4.0)+coeffs_single_epoch[1],coeffs_single_epoch[0]*(1.0)+coeffs_single_epoch[1]], linestyle="-", color="white", zorder=1)

# rrlfe vs. SSPP (coadded)
hb = axes[0,1].hexbin(df_sspp_coadded["feh_sspp_coadded"],df_sspp_coadded["feh_rrlfe"], extent=(-4.,1.,-4.,1.), linewidths=0.01)
axes[0,1].plot([-4, 1], [-4, 1], linestyle="--", color="white", zorder=1, label="1-to-1")
axes[0,1].set_xlim(xlim)
axes[0,1].set_ylim(ylim)
axes[0,1].set_xlabel("SSPP (coadded)", fontsize = char_size)
axes[0,1].set(adjustable='box', aspect='equal')
# best-fit coeffs
idx_sane_coadded = (np.isfinite(df_sspp_coadded["feh_sspp_coadded"]) & np.isfinite(df_sspp_coadded["feh_rrlfe"])) & \
        ((np.abs(df_sspp_coadded["feh_rrlfe"]) < 5.) & (np.abs(df_sspp_coadded["feh_sspp_coadded"]) < 5.))
coeffs_coadded = np.polyfit(df_sspp_coadded["feh_sspp_coadded"][idx_sane_coadded], df_sspp_coadded["feh_rrlfe"][idx_sane_coadded], deg=1)
axes[0,1].plot([-4.0,1.0],[coeffs_coadded[0]*(-4.0)+coeffs_coadded[1],coeffs_coadded[0]*(1.0)+coeffs_coadded[1]], linestyle="-", color="white", zorder=1)

# rrlfe vs. Liu+
hb = axes[1,0].hexbin(df_liu_2020["feh_liu"],df_liu_2020["feh_rrlfe"], extent=(-4.,1.,-4.,1.), linewidths=0.01)
axes[1,0].plot([-4, 1], [-4, 1], linestyle="--", color="white", zorder=1, label="1-to-1")
axes[1,0].set_xlim(xlim)
axes[1,0].set_ylim(ylim)
axes[1,0].set_xlabel("Liu+ 2020", fontsize = char_size)
axes[1,0].set(adjustable='box', aspect='equal')
# best-fit coeffs
idx_sane_liu = (np.isfinite(df_liu_2020["feh_liu"]) & np.isfinite(df_liu_2020["feh_rrlfe"])) & \
        ((np.abs(df_liu_2020["feh_rrlfe"]) < 5.) & (np.abs(df_liu_2020["feh_liu"]) < 5.))
coeffs_liu = np.polyfit(df_liu_2020["feh_liu"][idx_sane_liu], df_liu_2020["feh_rrlfe"][idx_sane_liu], deg=1)
axes[1,0].plot([-4.0,1.0],[coeffs_liu[0]*(-4.0)+coeffs_liu[1],coeffs_liu[0]*(1.0)+coeffs_liu[1]], linestyle="-", color="white", zorder=1)

axes[1,0].set_ylabel("rrlfe", fontsize = char_size)

# rrlfe vs. Whitten+
axes[1,1].scatter(df_whitten["feh_whitten"], df_whitten["feh_rrlfe"], s=10, color="k")
axes[1,1].plot([-4, 1], [-4, 1], linestyle="--", color="gray")
axes[1,1].set_xlim(xlim)
axes[1,1].set_ylim(ylim)
axes[1,1].set_xlabel("Whitten+ 2021", fontsize = char_size)
axes[1,1].set(adjustable='box', aspect='equal')
# best-fit coeffs
idx_sane_whitten = (np.isfinite(df_whitten["feh_whitten"]) & np.isfinite(df_whitten["feh_rrlfe"])) & \
        ((np.abs(df_whitten["feh_rrlfe"]) < 5.) & (np.abs(df_whitten["feh_whitten"]) < 5.))
coeffs_whitten = np.polyfit(df_whitten["feh_whitten"][idx_sane_whitten], df_whitten["feh_rrlfe"][idx_sane_whitten], deg=1)
axes[1,1].plot([-4.0,1.0],[coeffs_whitten[0]*(-4.0)+coeffs_whitten[1],coeffs_whitten[0]*(1.0)+coeffs_whitten[1]], linestyle="-", color="grey", zorder=1)

# rrlfe vs. Li+
# !uncomment below when ready!
#hb = axes[2,0].hexbin(df_li_2022["feh_li"],df_li_2022["feh_rrlfe"], extent=(-4.,1.,-4.,1.), linewidths=0.01)
axes[2,0].plot([-4, 1], [-4, 1], linestyle="--", color="k")
axes[2,0].set_xlim(xlim)
axes[2,0].set_ylim(ylim)
axes[2,0].set_xlabel("Li+ 2022", fontsize = char_size)
axes[2,0].set(adjustable='box', aspect='equal')
axes[2,0].set_ylabel("rrlfe", fontsize = char_size)

# all best-fit lines together
coeffs_rrlfe_synth = 1.1*coeffs_liu
print("!!!! SYNTHETIC BASIS SET VALUES ARE PLACEHOLDERS !!!!")
axes[2,1].plot([-4, 1], [-4, 1], linestyle="--", color="gray")
axes[2,1].set_xlim(xlim)
axes[2,1].set_ylim(ylim)
axes[2,1].set(adjustable='box', aspect='equal')
axes[2,1].plot([-4.0,1.0],[coeffs_rrlfe_synth[0]*(-4.0)+coeffs_rrlfe_synth[1],coeffs_rrlfe_synth[0]*(1.0)+coeffs_rrlfe_synth[1]], linestyle="-", zorder=0, label="rrlfe synthetic basis set (PLACEHOLDER)")
axes[2,1].plot([-4.0,1.0],[coeffs_single_epoch[0]*(-4.0)+coeffs_single_epoch[1],coeffs_single_epoch[0]*(1.0)+coeffs_single_epoch[1]], linestyle="-", zorder=0, label="SDSS, single-epoch")
axes[2,1].plot([-4.0,1.0],[coeffs_coadded[0]*(-4.0)+coeffs_coadded[1],coeffs_coadded[0]*(1.0)+coeffs_coadded[1]], linestyle="-", zorder=0, label="SDSS, coadded")
axes[2,1].plot([-4.0,1.0],[coeffs_liu[0]*(-4.0)+coeffs_liu[1],coeffs_liu[0]*(1.0)+coeffs_liu[1]], linestyle="-", zorder=0, label="Liu+ 2020")
axes[2,1].plot([-4.0,1.0],[coeffs_whitten[0]*(-4.0)+coeffs_whitten[1],coeffs_whitten[0]*(1.0)+coeffs_whitten[1]], linestyle="-", zorder=0, label="Whitten+ 2021")
axes[2,1].legend()

plt.subplots_adjust(wspace=0.0, hspace=0.2)

#plt.show()

plt.savefig("junk.png")