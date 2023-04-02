#!/usr/bin/env python
# coding: utf-8

# This takes Fe/H values of our McDonald stars and compares the values from
# 1.) rrlfe
# 2.) the high-res basis

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

stem = "/Users/bandari/Documents/git.repos/rrlfe/"
file_name_rrlfe_retrieved = "rrlfe_io_20220803_01_mcd/bin/retrieved_vals_20220803.csv"
file_name_highres = "notebooks_for_development/mapped_program_fehs_20230402.csv"
file_name_phases = "./src/mcd_final_phases_ascii_files_all.list"

df_rrlfe = pd.read_csv(stem + file_name_rrlfe_retrieved)
df_highres = pd.read_csv(stem + file_name_highres)
df_phases = pd.read_csv(stem + file_name_phases)

# match Fe/Hs between two sources of Fe/H
df_rrlfe["name_match"] = ""
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("X_Ari")] = "X_Ari"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("RR_Cet")] = "RR_Cet"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("SV_Eri")] = "SV_Eri"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("RR_Leo")] = "RR_Leo"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("TW_Lyn")] = "TW_Lyn"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("RR_Lyr")] = "RR_Lyr"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("445")] = "V445_Oph"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("AV_Peg")] = "AV_Peg"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("BH_Peg")] = "BH_Peg"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("AR_Per")] = "AR_Per"
df_rrlfe["name_match"][df_rrlfe["realization_spec_file_name"].str.contains("TU_U")] = "TU_UMa"

df_highres['name_match'] = df_highres['name_match'].str.lower() # lower case, to make case insensitive
df_rrlfe['name_match'] = df_rrlfe['name_match'].str.lower() # lower case, to make case insensitive
df_retrievals_all = df_rrlfe.merge(df_highres, on="name_match")
df_retrievals_all = df_retrievals_all.merge(df_phases, on="orig_spec_file_name") # add phases

# find mean, for plotting
df_mean = df_retrievals_all.groupby("name_match", as_index=False).mean()

# distance (ito phase) from maximum (more informative)
df_retrievals_all["phase_from_zero"] = np.abs(np.subtract(np.abs(np.subtract(df_retrievals_all["phase"],0.5)),0.5))

'''
plt.scatter(df_retrievals_all["feh_high_res_mapped"], df_retrievals_all["feh_retrieved"], c=df_retrievals_all["phase"], zorder=3)
plt.plot([-2.5,0.0],[-2.5,0.0], linestyle="--", color="gray", zorder=2)
plt.colorbar()
plt.title("McDonald RRabs (color: phase)")
plt.xlabel("[Fe/H], High-res literature basis (based on Layden 94)")
plt.ylabel("[Fe/H], rrlfe retrieved")
plt.show()

plt.scatter(df_retrievals_all["feh_high_res_mapped"], df_retrievals_all["feh_retrieved"], c=df_retrievals_all["phase_from_zero"], zorder=3)
plt.plot([-2.5,0.0],[-2.5,0.0], linestyle="--", color="gray", zorder=2)
plt.colorbar()
plt.title("McDonald RRabs (color: phase from zero)")
plt.xlabel("[Fe/H], High-res literature basis (based on Layden 94)")
plt.ylabel("[Fe/H], rrlfe retrieved")
plt.show()
'''

cols = ["orig_spec_file_name","phase","phase_from_zero"]
df_retrievals_all.keys()

# line of best fit
coeffs_poly = np.polyfit(df_retrievals_all["feh_high_res_mapped"], df_retrievals_all["feh_retrieved"], deg=1)

print("Coeffs of line of best fit",coeffs_poly)

plt.clf()

cmap = "Blues"
sns.set(font_scale=1.9)
sns.set_style(style='white')

df_retrievals_all["$|\Delta \phi|$"] = df_retrievals_all["phase_from_zero"]
df_retrievals_all["$T_{eff}$"] = df_retrievals_all["teff_retrieved"]

g = sns.relplot(
    data=df_retrievals_all,
    x="feh_high_res_mapped", y="feh_retrieved",
    hue="$|\Delta \phi|$", size="$T_{eff}$", sizes=(40, 200), edgecolor="k",
    palette=cmap, zorder=4, hue_order= [0,0.5], alpha=0.8
)

#sns.scatterplot(data=df_mean, x = "feh_high_res_mapped", y = "feh_retrieved", palette="reds")
plt.errorbar(df_mean["feh_high_res_mapped"], df_mean["feh_retrieved"], xerr=df_mean["err_feh_high_res_mapped"], linestyle="",linewidth=4,color="lightcoral", marker="s", alpha=1., markersize=20)

lobf = np.add(np.multiply(coeffs_poly[0],[-2.8,0.0]),coeffs_poly[1])
h1 = sns.lineplot(x=[-2.8,0.0], y=[-2.8,0.0], linestyle="--", color="gray", legend=False)
h2 = sns.lineplot(x=[-2.8,0.0], y=lobf, legend=False)

plt.setp(h1, zorder=2)
plt.setp(h2, zorder=3)

g.set_xlabels("[Fe/H], mapped high-res", fontsize=30)
g.set_ylabels("[Fe/H], retrieved", fontsize=30)

#g.set_yticklabels(g.get_yticks(), size = 25)

g.fig.set_size_inches(16,9)
plt.grid()

plt.tight_layout()

# legend
leg = g._legend
leg.set_bbox_to_anchor([0.5, -0.5])  # coordinates of lower left of bounding box
leg._loc = 2  # if required you can set the loc
#leg._ncol=3

lgnd = plt.legend(ncol=1)

file_name_write = "junk.pdf"
g.savefig(file_name_write, bbox_inches='tight')
print("Wrote " + file_name_write)
