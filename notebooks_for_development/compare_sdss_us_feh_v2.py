#!/usr/bin/env python
# coding: utf-8

# This takes in output file of retrieved [Fe/H], finds matches with nSSPP output file,
# and plots comparison

# Created 2022 Aug. 9 by E.S.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read in our values
#df_retrieved = pd.read_csv(stem + "rrlfe_io_20220904_s82_all_relaxed/bin/retrieved_vals_20220904.csv")
df_retrieved = pd.read_csv(stem + "rrlfe_io_20220914_catalina/bin/retrieved_vals_20220914_catalina.csv")

# get text file with RRL types
df_types = pd.read_csv(stem + "notebooks_for_development/data/phaseampgroupstype_modified.dat", names=["file_name", "hjd", "sesar_phase",
                        "sesar_cycles", "sesar_period", "g_ephemeris", "g_amplitude", "sesar_type", "drake_phase", "drake_cycles", "drake_period",
                        "drake_V_ephemeris", "drake_V_amp", "drake_type", "drake2013b_chart_period", "drake2013b_chart_amp", "drake2013b_chart_type",
                        "abbas2014_period", "abbas2014_amp", "abbas2014_type", "catalina_DR2_chart_period", "catalina_DR2_chart_amp", "catalina_DR2_chart_type",
                        "drake_MLS_chart_period", "drake_MLS_chart_amp", "drake_MLS_chart_type"], delim_whitespace=True)

# set a single type by taking the mode of all the types from the sources; use col [0]
# from the output (col [1] gives a second value in the rare case that the mode has
# to be found from a 50-50 distribution of types)
df_types["type_mode"] = df_types[["sesar_type","drake_type","drake2013b_chart_type","abbas2014_type","catalina_DR2_chart_type","drake_MLS_chart_type"]].mode(axis=1)[0]

# read in nSSPP Fe/H values
df_nsspp = pd.read_csv(stem + "notebooks_for_development/data/RRL2.out", names=["spectrum", "teff", "logg",
                                                     "feh_direct_nsspp", "feh_beers"], delim_whitespace=True)
# read in S/N
df_s2n = pd.read_csv("./data/s2n_sdss_spec.csv")

# make a column on the basis of which we can merge the tables
df_retrieved["name_match"] = df_retrieved["realization_spec_file_name"].str.split(pat="_noise_ver", expand=True)[0]
df_s2n["name_match"] = df_s2n["file_name"].str.split(pat=".dat", expand=True)[0]
df_types["name_match"] = df_types["file_name"].str.split(pat=".dat", expand=True)[0]
df_nsspp["name_match"] = df_nsspp["spectrum"]
df_nsspp["name_match"] = df_nsspp["name_match"].str.replace(pat="h", repl="g") # change 'h' to 'g'

# merge everything
df_merged_0 = df_retrieved.merge(df_nsspp, on="name_match", how="inner")
df_merged_1_post_type = df_merged_0.merge(df_types, on="name_match", how="inner")
df_merged_1_pre_s2n = df_merged_1_post_type.merge(df_s2n, on="name_match", how="inner")

# impose S/N cutoff; spectra with vals below this are dropped
idx_s2n = df_merged_1_pre_s2n["s_to_n"] > 15.
df_merged_1 = df_merged_1_pre_s2n[idx_s2n]
df_low_s2n = df_merged_1_pre_s2n[~idx_s2n]

# fit a line to the ones of high S/N
idx_finite = np.isfinite(df_merged_1["feh_direct_nsspp"]) & np.isfinite(df_merged_1["feh_retrieved"]) # to get rid of nans
coeffs = np.polyfit(df_merged_1["feh_direct_nsspp"][idx_finite], df_merged_1["feh_retrieved"][idx_finite], deg=1)

# indices of different types
idx_ab = df_merged_1["type_mode"] == "ab" # indices of RRabs
idx_c = df_merged_1["type_mode"] == "c" # indices of RRcs
df_merged_merged_abs_only = df_merged_1[idx_ab]
df_merged_merged_cs_only = df_merged_1[idx_c]

import ipdb; ipdb.set_trace()
idx_finite_abs_only = np.isfinite(df_merged_merged_abs_only["feh_direct_nsspp"]) & np.isfinite(df_merged_merged_abs_only["feh_retrieved"]) # to get rid of nans
idx_finite_cs_only = np.isfinite(df_merged_merged_cs_only["feh_direct_nsspp"]) & np.isfinite(df_merged_merged_cs_only["feh_retrieved"]) # to get rid of nans
coeffs_ab = np.polyfit(df_merged_merged_abs_only["feh_direct_nsspp"][idx_finite_abs_only], df_merged_merged_abs_only["feh_retrieved"][idx_finite_abs_only], deg=1)
coeffs_c = np.polyfit(df_merged_merged_cs_only["feh_direct_nsspp"][idx_finite_cs_only], df_merged_merged_cs_only["feh_retrieved"][idx_finite_cs_only], deg=1)
import ipdb; ipdb.set_trace()

# coefficients of line reflected around the 1-to-1 line
# if m1 and b1 are slope and y-int of line of best fit, the flipped line is
# y = m1^(-1)*x + b1*(1-m1^(-1))/(1-m1)
coeffs_flip = np.array([np.divide(1.,coeffs[0]), coeffs[1]*np.divide(1.-np.divide(1.,coeffs[0]),1.-coeffs[0])])

print("Coeffs of line of best fit:",coeffs)
print("Coeffs of line flipped around 1-to-1:",coeffs_flip)
# comparison of Fe/H values
plt.clf()
plt.figure(figsize=(10,5))
plt.plot([-3.0,0.0],[-3.0,0.0], linestyle="--", color="black", zorder=0) # one-to-one
plt.plot([-3.0,0.0],[coeffs[0]*(-3.0)+coeffs[1],coeffs[0]*(0.0)+coeffs[1]], linestyle="-", zorder=0) # line of best fit, both types
#plt.plot([-3.0,0.0],[coeffs_flip[0]*(-3.0)+coeffs_flip[1],coeffs_flip[0]*(0.0)+coeffs_flip[1]], linestyle="-", zorder=0) # line flipped around 1-to-1
plt.scatter(df_low_s2n["feh_direct_nsspp"], df_low_s2n["feh_retrieved"],
            c="gray", s=50, alpha=0.5, zorder=0)
#plt.plot(df_merged_1["feh_direct_nsspp"], np.add(coeffs[1],np.multiply(coeffs[0],df_merged_1["feh_direct_nsspp"])), linestyle="-", color="gray")

# if we want to compare Feh
plt.scatter(df_merged_1["feh_direct_nsspp"], df_merged_1["feh_retrieved"],
            c=df_merged_1["s_to_n"], cmap="Greens", s=50, edgecolors="k")

'''
# if we want to compare retrieved Teffs
plt.scatter(df_merged_1["teff"], df_merged_1["teff_retrieved"],
            c=df_merged_1["s_to_n"], cmap="Greens", s=50, edgecolors="k")
'''
plt.xlabel("[Fe/H], nSSPP", fontsize=25)
plt.ylabel("[Fe/H], rrlfe", fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
cbar = plt.colorbar()
cbar.set_label("S/N",fontsize=20)
cbar.ax.tick_params(labelsize=20)
plt.tight_layout()
#plt.gca().set_aspect('equal', adjustable='box') # for equal x and y scale
file_name_write = "junk.pdf"
import ipdb; ipdb.set_trace()
#plt.show()
plt.savefig(file_name_write)
print("Wrote scatterplot", file_name_write)

# distinguish points by type
plt.clf()
plt.figure(figsize=(10,5))
plt.plot([-3.0,0.0],[-3.0,0.0], linestyle="--", color="black", zorder=0) # one-to-one
plt.plot([-3.0,0.0],[coeffs[0]*(-3.0)+coeffs[1],coeffs[0]*(0.0)+coeffs[1]], linestyle="-", color="k", zorder=0) # line of best fit
plt.plot([-3.0,0.0],[coeffs_ab[0]*(-3.0)+coeffs_ab[1],coeffs_ab[0]*(0.0)+coeffs_ab[1]], linestyle="-", color="red", zorder=0) # line of best fit, RRabs
plt.plot([-3.0,0.0],[coeffs_c[0]*(-3.0)+coeffs_c[1],coeffs_c[0]*(0.0)+coeffs_c[1]], linestyle="-", color="blue", zorder=0) # line of best fit, RRcs
#plt.plot([-3.0,0.0],[coeffs_flip[0]*(-3.0)+coeffs_flip[1],coeffs_flip[0]*(0.0)+coeffs_flip[1]], linestyle="-", zorder=0) # line flipped around 1-to-1
plt.scatter(df_merged_1["feh_direct_nsspp"].where(idx_ab), df_merged_1["feh_retrieved"].where(idx_ab),
            label="ab", s=50, edgecolors="k")
plt.scatter(df_merged_1["feh_direct_nsspp"].where(idx_c), df_merged_1["feh_retrieved"].where(idx_c),
            label="c", s=50, edgecolors="k")
plt.legend()
'''
# if we want to compare retrieved Teffs
plt.scatter(df_merged_1["teff"], df_merged_1["teff_retrieved"],
            c=df_merged_1["s_to_n"], cmap="Greens", s=50, edgecolors="k")
'''
plt.title("best-fits in black: all; red: RRabs; blue: RRcs")
plt.xlabel("[Fe/H], nSSPP", fontsize=25)
plt.ylabel("[Fe/H], rrlfe", fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
#plt.gca().set_aspect('equal', adjustable='box') # for equal x and y scale
file_name_write = "junk_bytype.pdf"
import ipdb; ipdb.set_trace()
plt.show()
#plt.savefig(file_name_write)

# histograms of types
binedges = np.linspace(-3.5,0.5,num=401,endpoint=True)
plt.hist(df_merged_1["feh_direct_nsspp"].where(idx_ab), bins=binedges, label="ab")
plt.hist(df_merged_1["feh_direct_nsspp"].where(idx_c), bins=binedges, label="c")
plt.xlabel("nSSPP [Fe/H]")
plt.legend()
file_name_write = "junk_bytype_hist.pdf"
plt.savefig(file_name_write)

# histogram of Stripe 82 Fe/H
plt.clf()
plt.figure(figsize=(10,5))
plt.hist(df_retrieved["feh_retrieved"],bins=300)
plt.xlabel("[Fe/H] of Stripe 82 stars from rrlfe", fontsize=25)
plt.xlim([-3.,1.1])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
file_name_write2 = "junk2.pdf"
plt.savefig(file_name_write2)
print("Wrote histogram", file_name_write2)


# plot Teff (nSSPP) vs. Balmer line width to show linearity
plt.clf()
# just for clarity
df_merged_1["nsspp_logg"] = df_merged_1["logg"]
df_merged_1["nsspp_teff"] = df_merged_1["teff"]
df_merged_1["Teff (nSSPP)"] = df_merged_1["nsspp_teff"]
df_merged_1["[Fe/H] (nSSPP)"] = df_merged_1["feh_direct_nsspp"]
df_merged_1["log(g) (nSSPP)"] = df_merged_1["nsspp_logg"]

#sns.set_style('darkgrid', {'legend.frameon':True})
sns.set(rc={'axes.facecolor':'cornflowerblue', 'figure.facecolor':'cornflowerblue'})
sns.set(font_scale = 2.5)
cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
'''
g = sns.relplot(
    data=df_merged_1,
    x="EW_Balmer", y="Teff (nSSPP)",
    hue="[Fe/H] (nSSPP)", hue_norm=(-3.0,-0.5), size="log(g) (nSSPP)",
    palette=cmap, sizes=(10, 200),
    height=8.27, aspect=1.1, legend=False
)
#plt.plot([3,16], [6000,8000], linestyle = "--", color="k",zorder=0)
g.fig.set_size_inches(12,10)
g.ax.xaxis.grid(True, "minor", linewidth=.25)
g.ax.yaxis.grid(True, "minor", linewidth=.25)
g.ax.set_ylabel("Teff, nSSPP", fontsize=30)
g.ax.set_xlabel("Balmer EW, rrlfe ($\AA$)", fontsize=30)
g.despine(left=True, bottom=True)
#g.ax.set_title("(dashed line: 1-to-1)")
#handles, labels = g.get_legend_handles_labels()
#l = plt.legend(handles[0:2], labels[0:2], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#plt.legend(bbox_to_anchor=(1.55, 1), loc=2, borderaxespad=0.)
plt.tight_layout()
file_name_write3 = "junk3.pdf"
plt.savefig(file_name_write3)
print("Wrote plot", file_name_write3)
'''
g = sns.relplot(
    data=df_merged_1,
    x="EW_Balmer", y="Teff (nSSPP)",
    hue="[Fe/H] (nSSPP)", hue_norm=(-3.0,-0.5), size="log(g) (nSSPP)",
    palette=cmap, sizes=(10, 200),
    height=8.27, aspect=1.1, legend=True
)
g.fig.set_size_inches(14,10)
g.ax.xaxis.grid(True, "minor", linewidth=.25)
g.ax.yaxis.grid(True, "minor", linewidth=.25)
g.ax.set_ylabel("Teff, nSSPP", fontsize=30)
g.ax.set_xlabel("Balmer EW, rrlfe ($\AA$)", fontsize=30)
g.despine(left=True, bottom=True)
plt.xlim([-3.,0.])
plt.ylim([-3.,0.])
plt.legend(bbox_to_anchor=(1.55, 1), loc=2, borderaxespad=0.)
#plt.tight_layout()
file_name_write4 = "junk4.pdf"
plt.savefig(file_name_write4)
print("Wrote plot", file_name_write4)
