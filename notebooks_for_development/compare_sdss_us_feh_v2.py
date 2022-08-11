#!/usr/bin/env python
# coding: utf-8

# This takes in output file of retrieved [Fe/H], finds matches with nSSPP output file,
# and plots comparison

# Created 2022 Aug. 9 by E.S.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read in our values
df_retrieved = pd.read_csv(stem + "rrlfe_io_20220809_01/bin/retrieved_vals_20220809.csv")

# read in nSSPP Fe/H values
df_nsspp = pd.read_csv(stem + "notebooks_for_development/data/nSSPP82.out", names=["sdss","spectrum", "teff", "logg",
                                                     "feh_direct_nsspp", "feh_beers"], delim_whitespace=True)
# read in S/N
df_s2n = pd.read_csv("./data/s2n_sdss_spec.csv")

# make a column on the basis of which we can merge the tables
df_retrieved["name_match"] = df_retrieved["realization_spec_file_name"].str.split(pat="_noise_ver", expand=True)[0]
df_s2n["name_match"] = df_s2n["file_name"].str.split(pat=".dat", expand=True)[0]
df_nsspp["name_match"] = df_nsspp["spectrum"]
df_nsspp["name_match"] = df_nsspp["name_match"].str.replace(pat="h", repl="g") # change 'h' to 'g'

# merge everything
df_merged_0 = df_retrieved.merge(df_nsspp, on="name_match", how="inner")
df_merged_1 = df_merged_0.merge(df_s2n, on="name_match", how="inner")

# comparison of Fe/H values
plt.clf()
plt.figure(figsize=(10,5))
plt.plot([-2.5,0.0],[-2.5,0.0], linestyle="--", color="black", zorder=0)
plt.scatter(df_merged_1["feh_direct_nsspp"], df_merged_1["feh_retrieved"],
            c=df_merged_1["s_to_n"], cmap="Greens", s=50, edgecolors="k")
plt.xlabel("[Fe/H], nSSPP", fontsize=25)
plt.ylabel("[Fe/H], rrlfe", fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
cbar = plt.colorbar()
cbar.set_label("S/N",fontsize=20)
cbar.ax.tick_params(labelsize=20)
plt.tight_layout()
file_name_write = "junk.pdf"
plt.savefig(file_name_write)
print("Wrote scatterplot", file_name_write)

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
plt.legend(bbox_to_anchor=(1.55, 1), loc=2, borderaxespad=0.)
#plt.tight_layout()
file_name_write4 = "junk4.pdf"
plt.savefig(file_name_write4)
print("Wrote plot", file_name_write4)
