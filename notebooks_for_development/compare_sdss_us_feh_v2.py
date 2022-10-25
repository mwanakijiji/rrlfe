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
df_types["type_mode_0"] = df_types[["sesar_type","drake_type","drake2013b_chart_type","abbas2014_type","catalina_DR2_chart_type","drake_MLS_chart_type"]].mode(axis=1)[0]
df_types["type_mode_1"] = df_types[["sesar_type","drake_type","drake2013b_chart_type","abbas2014_type","catalina_DR2_chart_type","drake_MLS_chart_type"]].mode(axis=1)[1]
# a string will appear in element [1] if it is represented equally with that of element [0]

# keep only the data points which are more unambiguously typed (i.e., where element [1] is nan, meaning that element [0] represents a 'majority vote' among the literature sources)
df_types = df_types[df_types["type_mode_1"].isna()]

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

# less restrictive: just get rid of nans
idx_finite = np.isfinite(df_merged_1["feh_direct_nsspp"]) & np.isfinite(df_merged_1["feh_retrieved"])

# more restrictive: get rid of clearly unphysical values
idx_sane = (np.isfinite(df_merged_1["feh_direct_nsspp"]) & np.isfinite(df_merged_1["feh_retrieved"])) & \
                ((np.abs(df_merged_1["feh_retrieved"]) < 5.) & (np.abs(df_merged_1["feh_direct_nsspp"]) < 5.))
idx_sane_abs_only = (np.isfinite(df_merged_1["feh_direct_nsspp"]) & np.isfinite(df_merged_1["feh_retrieved"])) & \
                ((np.abs(df_merged_1["feh_retrieved"]) < 5.) & (np.abs(df_merged_1["feh_direct_nsspp"]) < 5.)) & (df_merged_1["type_mode_0"] == "ab")
idx_sane_cs_only = (np.isfinite(df_merged_1["feh_direct_nsspp"]) & np.isfinite(df_merged_1["feh_retrieved"])) & \
                ((np.abs(df_merged_1["feh_retrieved"]) < 5.) & (np.abs(df_merged_1["feh_direct_nsspp"]) < 5.)) & (df_merged_1["type_mode_0"] == "c")

# experiment: if we artifically split the stars by 7000K (ab/c boundary), are things better behaved?
idx_sane_cool_7000 = (np.isfinite(df_merged_1["feh_direct_nsspp"]) & np.isfinite(df_merged_1["feh_retrieved"])) & \
                ((np.abs(df_merged_1["feh_retrieved"]) < 5.) & (np.abs(df_merged_1["feh_direct_nsspp"]) < 5.)) & (df_merged_1["teff"] < 7000)
idx_sane_hot_7000 = (np.isfinite(df_merged_1["feh_direct_nsspp"]) & np.isfinite(df_merged_1["feh_retrieved"])) & \
                ((np.abs(df_merged_1["feh_retrieved"]) < 5.) & (np.abs(df_merged_1["feh_direct_nsspp"]) < 5.)) & (df_merged_1["teff"] > 7000)
import ipdb; ipdb.set_trace()

df_merged_merged_abs_only = df_merged_1[idx_sane_abs_only]
df_merged_merged_cs_only = df_merged_1[idx_sane_cs_only]

coeffs = np.polyfit(df_merged_1["feh_direct_nsspp"][idx_sane], df_merged_1["feh_retrieved"][idx_sane], deg=1)
coeffs_ab = np.polyfit(df_merged_1["feh_direct_nsspp"][idx_sane_abs_only], df_merged_1["feh_retrieved"][idx_sane_abs_only], deg=1)
coeffs_c = np.polyfit(df_merged_1["feh_direct_nsspp"][idx_sane_cs_only], df_merged_1["feh_retrieved"][idx_sane_cs_only], deg=1)
import ipdb; ipdb.set_trace()

# coefficients of line reflected around the 1-to-1 line
# if m1 and b1 are slope and y-int of line of best fit, the flipped line is
# y = m1^(-1)*x + b1*(1-m1^(-1))/(1-m1)
coeffs_flip = np.array([np.divide(1.,coeffs[0]), coeffs[1]*np.divide(1.-np.divide(1.,coeffs[0]),1.-coeffs[0])])

print("Coeffs of line of best fit:",coeffs)
print("Coeffs of line flipped around 1-to-1:",coeffs_flip)

# plot comparison of Fe/H values
plt.clf()
plt.figure(figsize=(10,5))
plt.plot([-4.0,0.0],[-4.0,0.0], linestyle="--", color="black", zorder=0) # one-to-one
plt.plot([-4.0,0.0],[coeffs[0]*(-4.0)+coeffs[1],coeffs[0]*(0.0)+coeffs[1]], linestyle="-", label="best-fit, RRabs and cs", zorder=0) # line of best fit, both types
#plt.plot([-3.0,0.0],[coeffs_flip[0]*(-3.0)+coeffs_flip[1],coeffs_flip[0]*(0.0)+coeffs_flip[1]], linestyle="-", zorder=0) # line flipped around 1-to-1
plt.scatter(df_low_s2n["feh_direct_nsspp"], df_low_s2n["feh_retrieved"],
            c="gray", s=50, alpha=0.5, label="S/N<15", zorder=0)
#plt.plot(df_merged_1["feh_direct_nsspp"], np.add(coeffs[1],np.multiply(coeffs[0],df_merged_1["feh_direct_nsspp"])), linestyle="-", color="gray")

# if we want to compare Feh
plt.scatter(df_merged_1["feh_direct_nsspp"][idx_finite], df_merged_1["feh_retrieved"][idx_finite],
            c=df_merged_1["s_to_n"][idx_finite], cmap="Greens", s=50, label="S/N>15", edgecolors="k")

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
plt.legend()
#plt.gca().set_aspect('equal', adjustable='box') # for equal x and y scale
file_name_write = "junk.pdf"
import ipdb; ipdb.set_trace()
#plt.show()
plt.savefig(file_name_write)
print("Wrote scatterplot", file_name_write)

# distinguish points by type
plt.clf()
plt.figure(figsize=(10,5))

# Fe/H retrievals
plt.plot([-4.0,0.0],[-4.0,0.0], linestyle="--", color="black", zorder=0) # one-to-one
plt.plot([-4.0,0.0],[coeffs[0]*(-4.0)+coeffs[1],coeffs[0]*(0.0)+coeffs[1]], linestyle="-", color="orange", label="best-fit, RRabs and cs", zorder=0) # line of best fit
plt.plot([-4.0,0.0],[coeffs_ab[0]*(-4.0)+coeffs_ab[1],coeffs_ab[0]*(0.0)+coeffs_ab[1]], linestyle="-", color="blue", label="best-fit, RRabs", zorder=0) # line of best fit, RRabs
plt.plot([-4.0,0.0],[coeffs_c[0]*(-4.0)+coeffs_c[1],coeffs_c[0]*(0.0)+coeffs_c[1]], linestyle="-", color="red", label="best-fit, RRcs", zorder=0) # line of best fit, RRcs
#plt.plot([-3.0,0.0],[coeffs_flip[0]*(-3.0)+coeffs_flip[1],coeffs_flip[0]*(0.0)+coeffs_flip[1]], linestyle="-", zorder=0) # line flipped around 1-to-1
plt.legend()
plt.xlabel("[Fe/H], nSSPP", fontsize=25)
plt.ylabel("[Fe/H], rrlfe", fontsize=25)
plt.scatter(df_merged_1["feh_direct_nsspp"][idx_sane_abs_only], df_merged_1["feh_retrieved"][idx_sane_abs_only],
            label="ab", s=50, color="blue", edgecolors="k")
plt.scatter(df_merged_1["feh_direct_nsspp"][idx_sane_cs_only], df_merged_1["feh_retrieved"][idx_sane_cs_only],
            label="c", s=50, color="red", edgecolors="k")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend()
plt.tight_layout()
#plt.gca().set_aspect('equal', adjustable='box') # for equal x and y scale
file_name_write = "junk_bytype.pdf"
import ipdb; ipdb.set_trace()
#plt.show()
plt.savefig(file_name_write)


# if we want to compare retrieved Teffs

#plt.scatter(df_merged_1["teff"], df_merged_1["teff_retrieved"],
#            c=df_merged_1["s_to_n"], cmap="Greens", s=50, edgecolors="k")
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
ax.plot([6000,8000],[6000,8000], linestyle="--", color="black", zorder=0, label="1-to-1") # one-to-one
ax.scatter(df_merged_1["teff"][idx_sane_abs_only], df_merged_1["teff_retrieved"][idx_sane_abs_only], s=50, edgecolors="k", label="RRabs")
ax.scatter(df_merged_1["teff"][idx_sane_cs_only], df_merged_1["teff_retrieved"][idx_sane_cs_only], s=50, edgecolors="k", label="RRcs")
ax.set_xlabel("Teff, nSSPP")
ax.set_ylabel("Teff, rrlfe")
fig.legend()
plt.savefig("junk_teff_retr.png")

# density plots

# all RRLs
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged_1["feh_direct_nsspp"][idx_sane] # idx_finite, idx_sane, idx_sane
y = df_merged_1["feh_retrieved"][idx_sane]
hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.plot([-3.5,0.5],[-3.5,0.5], linestyle="--", color="white", zorder=1, label="1-to-1")
ax.plot([-3.0,0.0],[coeffs[0]*(-3.0)+coeffs[1],coeffs[0]*(0.0)+coeffs[1]], linestyle="-", color="k", zorder=1, label="best fit, all")
ax.plot([-3.0,0.0],[coeffs_ab[0]*(-3.0)+coeffs_ab[1],coeffs_ab[0]*(0.0)+coeffs_ab[1]], linestyle="-", color="red", zorder=1, label="best fit, RRabs")
ax.plot([-3.0,0.0],[coeffs_c[0]*(-3.0)+coeffs_c[1],coeffs_c[0]*(0.0)+coeffs_c[1]], linestyle="-", color="blue", zorder=1, label="best fit, RRcs")
plt.title("Hexbin of RRabs and RRcs")
ax.set_xlabel("Fe/H, nSSPP")
ax.set_ylabel("Fe/H, rrlfe")
ax.set_xlim([-3.5,0.5])
ax.set_ylim([-3.5,0.5])
cb = fig.colorbar(hb, ax=ax)
cb.set_label('counts')
fig.legend()
plt.savefig("junk_all_hex.png")

# RRabs
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged_1["feh_direct_nsspp"][idx_sane_abs_only] # idx_finite, idx_sane_abs_only, idx_sane_abs_only
y = df_merged_1["feh_retrieved"][idx_sane_abs_only]
hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.plot([-3.5,0.5],[-3.5,0.5], linestyle="--", color="white", zorder=1, label="1-to-1")
ax.plot([-3.0,0.0],[coeffs[0]*(-3.0)+coeffs[1],coeffs[0]*(0.0)+coeffs[1]], linestyle="-", color="k", zorder=1, label="best fit, all")
ax.plot([-3.0,0.0],[coeffs_ab[0]*(-3.0)+coeffs_ab[1],coeffs_ab[0]*(0.0)+coeffs_ab[1]], linestyle="-", color="red", zorder=1, label="best fit, RRabs")
ax.plot([-3.0,0.0],[coeffs_c[0]*(-3.0)+coeffs_c[1],coeffs_c[0]*(0.0)+coeffs_c[1]], linestyle="-", color="blue", zorder=1, label="best fit, RRcs")
plt.title("Hexbin of RRabs only")
ax.set_xlabel("Fe/H, nSSPP")
ax.set_ylabel("Fe/H, rrlfe")
ax.set_xlim([-3.5,0.5])
ax.set_ylim([-3.5,0.5])
cb = fig.colorbar(hb, ax=ax)
cb.set_label('counts')
fig.legend()
plt.savefig("junk_abs_hex.png")

# RRcs
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged_1["feh_direct_nsspp"][idx_sane_cs_only] # idx_finite, idx_sane_abs_only, idx_sane_cs_only
y = df_merged_1["feh_retrieved"][idx_sane_cs_only]
hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.plot([-3.5,0.5],[-3.5,0.5], linestyle="--", color="white", zorder=1, label="1-to-1")
ax.plot([-3.0,0.0],[coeffs[0]*(-3.0)+coeffs[1],coeffs[0]*(0.0)+coeffs[1]], linestyle="-", color="k", zorder=1, label="best fit, all")
ax.plot([-3.0,0.0],[coeffs_ab[0]*(-3.0)+coeffs_ab[1],coeffs_ab[0]*(0.0)+coeffs_ab[1]], linestyle="-", color="red", zorder=1, label="best fit, RRabs")
ax.plot([-3.0,0.0],[coeffs_c[0]*(-3.0)+coeffs_c[1],coeffs_c[0]*(0.0)+coeffs_c[1]], linestyle="-", color="blue", zorder=1, label="best fit, RRcs")
plt.title("Hexbin of RRcs only")
ax.set_xlabel("Fe/H, nSSPP")
ax.set_ylabel("Fe/H, rrlfe")
ax.set_xlim([-3.5,0.5])
ax.set_ylim([-3.5,0.5])
cb = fig.colorbar(hb, ax=ax)
cb.set_label('counts')
fig.legend()
plt.savefig("junk_cs_hex.png")

## 1d residual plots

# all RRLs
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged_1["feh_direct_nsspp"][idx_sane] # idx_finite, idx_sane, idx_sane
y = np.subtract(df_merged_1["feh_retrieved"][idx_sane],df_merged_1["feh_direct_nsspp"][idx_sane])
#hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.scatter(x,y,s=2)
ax.plot([-3.5,0.5],[0.,0.], linestyle="-", color="k", zorder=1)
plt.title("[Fe/H] residuals for RRabs and RRcs")
ax.set_ylabel("(Fe/H, rrlfe) - (Fe/H, nSSPP)")
ax.set_xlabel("Fe/H, nSSPP")
ax.set_xlim([-3.5,0.5])
ax.set_ylim([-1.0,1.0])
plt.savefig("junk_resids_feh_all.png")

# RRabs
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged_1["feh_direct_nsspp"][idx_sane_abs_only] # idx_finite, idx_sane, idx_sane
y = np.subtract(df_merged_1["feh_retrieved"][idx_sane_abs_only],df_merged_1["feh_direct_nsspp"][idx_sane_abs_only])
#hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.scatter(x,y,s=2)
ax.plot([-3.5,0.5],[0.,0.], linestyle="-", color="k", zorder=1)
plt.title("[Fe/H] residuals for RRabs only")
ax.set_ylabel("(Fe/H, rrlfe) - (Fe/H, nSSPP)")
ax.set_xlabel("Fe/H, nSSPP")
ax.set_xlim([-3.5,0.5])
ax.set_ylim([-1.0,1.0])
plt.savefig("junk_resids_feh_abs.png")

# RRcs
plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
x = df_merged_1["feh_direct_nsspp"][idx_sane_cs_only] # idx_finite, idx_sane, idx_sane
y = np.subtract(df_merged_1["feh_retrieved"][idx_sane_cs_only],df_merged_1["feh_direct_nsspp"][idx_sane_cs_only])
#hb = ax.hexbin(x,y, extent=(-3.5,0.5,-3.5,0.5))
ax.scatter(x,y,s=2)
ax.plot([-3.5,0.5],[0.,0.], linestyle="-", color="k", zorder=1)
plt.title("[Fe/H] residuals for RRcs only")
ax.set_ylabel("(Fe/H, rrlfe) - (Fe/H, nSSPP)")
ax.set_xlabel("Fe/H, nSSPP")
ax.set_xlim([-3.5,0.5])
ax.set_ylim([-1.0,1.0])
plt.savefig("junk_resids_feh_cs.png")



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
