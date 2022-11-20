#!/usr/bin/env python
# coding: utf-8

# This overplots X Ari spectra, to see line filling

# Created 2022 Aug 25 by E.S.

import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
import os

stem = "/Users/bandari/Documents/git.repos/rrlfe/rrlfe_io_20220803_01_mcd/realizations_output/norm/final/"

df_spec_1 = pd.read_csv(stem + "/X_Ari__01_noise_ver_000.dat", names=["wavel","flux"], delim_whitespace=True) # 0.2956578031370327
df_spec_3 = pd.read_csv(stem + "/X_Ari__03_noise_ver_000.dat", names=["wavel","flux"], delim_whitespace=True) # 0.4002971942307454
df_spec_5 = pd.read_csv(stem + "/X_Ari__05_noise_ver_000.dat", names=["wavel","flux"], delim_whitespace=True) # 0.5023736237323533
df_spec_10 = pd.read_csv(stem + "/X_Ari__10_noise_ver_000.dat", names=["wavel","flux"], delim_whitespace=True) # 0.6415883880645765
df_spec_7 = pd.read_csv(stem + "/X_Ari__07_noise_ver_000.dat", names=["wavel","flux"], delim_whitespace=True) # 0.9828637931079244

# define spectrum to underplot in grey
template_spec = df_spec_3

# set some constants for plotting
margin_hbeta = 45
center_hbeta = 4861.290
y_offset = 0.5

plt.clf()

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 5), gridspec_kw={'width_ratios': [2, 1]})

# df_spec_1
ax1.plot(template_spec["wavel"], template_spec["flux"], color="k", alpha = 0.3)
ax1.plot(df_spec_1["wavel"], df_spec_1["flux"], color="k")
ax2.plot(template_spec["wavel"], template_spec["flux"], color="k", alpha = 0.3)
ax2.plot(df_spec_1["wavel"], df_spec_1["flux"], color="k")

# df_spec_3
ax1.plot(template_spec["wavel"], np.add(template_spec["flux"],y_offset), color="k", alpha = 0.3)
ax1.plot(df_spec_3["wavel"], np.add(df_spec_3["flux"],y_offset), color="k")
ax2.plot(template_spec["wavel"], np.add(template_spec["flux"],y_offset), color="k", alpha = 0.3)
ax2.plot(df_spec_3["wavel"], np.add(df_spec_3["flux"],y_offset), color="k")
ax2.set_xlim([center_hbeta-margin_hbeta,center_hbeta+margin_hbeta])

# df_spec_5
ax1.plot(template_spec["wavel"], np.add(template_spec["flux"],2.*y_offset), color="k", alpha = 0.3)
ax1.plot(df_spec_5["wavel"], np.add(df_spec_5["flux"],2.*y_offset), color="k")
ax2.plot(template_spec["wavel"], np.add(template_spec["flux"],2.*y_offset), color="k", alpha = 0.3)
ax2.plot(df_spec_5["wavel"], np.add(df_spec_5["flux"],2.*y_offset), color="k")

# df_spec_10
ax1.plot(template_spec["wavel"], np.add(template_spec["flux"],3.*y_offset), color="k", alpha = 0.3)
ax1.plot(df_spec_10["wavel"], np.add(df_spec_10["flux"],3.*y_offset), color="k")
ax2.plot(template_spec["wavel"], np.add(template_spec["flux"],3.*y_offset), color="k", alpha = 0.3)
ax2.plot(df_spec_10["wavel"], np.add(df_spec_10["flux"],3.*y_offset), color="k")

# df_spec_7
ax1.plot(template_spec["wavel"], np.add(template_spec["flux"],4.*y_offset), color="k", alpha = 0.3)
ax1.plot(df_spec_7["wavel"], np.add(df_spec_7["flux"],4.*y_offset), color="k")
ax2.plot(template_spec["wavel"], np.add(template_spec["flux"],4.*y_offset), color="k", alpha = 0.3)
ax2.plot(df_spec_7["wavel"], np.add(df_spec_7["flux"],4.*y_offset), color="k")

# denote lines
ax2.annotate("H" + r"$\beta$", xy=(4862,3.0), xytext=(4861-40,3.1), fontsize=15, rotation=0)
ax1.annotate("H" + r"$\gamma$", xy=(4340,3.0), xytext=(4340-13,3.1), fontsize=15, rotation=0)
ax1.annotate("H" + r"$\delta$", xy=(4102,3.0), xytext=(4102-13,3.1), fontsize=15, rotation=0)
ax1.annotate("H" + r"$\epsilon$", xy=(3970,3.0), xytext=(3970+70,3.1), fontsize=15, arrowprops=dict(facecolor='black', arrowstyle="-"), rotation=0)
ax1.annotate("Ca II H", xy=(3968.469,3.0), xytext=(3970-5,3.2), fontsize=15, arrowprops=dict(facecolor='black', arrowstyle="-"), rotation=0)
ax1.annotate("Ca II K", xy=(3933.7,3.0), xytext=(3933.7-30,3.1), fontsize=15, rotation=0)

ax1.annotate("0.98", xy=(4180,1.0), xytext=(4180+15,0.2+5.*y_offset), textcoords="data", fontsize=20)
ax1.annotate("0.64", xy=(4180,1.0), xytext=(4180+15,0.2+4.*y_offset), textcoords="data", fontsize=20)
ax1.annotate("0.50", xy=(4180,1.0), xytext=(4180+15,0.2+3.*y_offset), textcoords="data", fontsize=20)
ax1.annotate("0.40", xy=(4180,1.0), xytext=(4180+15,0.2+2.*y_offset), textcoords="data", fontsize=20)
ax1.annotate("$\phi$=0.30", xy=(4180,1.0), xytext=(4180,0.2+y_offset), textcoords="data", fontsize=20)

ax1.set_xlim([3900.,4382.])
ax1.set_ylim([0.2,3.45])
ax2.set_xlim([center_hbeta-margin_hbeta,center_hbeta+margin_hbeta])
ax2.axvline(x=center_hbeta, linestyle="--", color="gray", zorder=0)

#ax1.set_xlabel("Wavelength ($\AA$)", fontsize=25)
ax1.set_ylabel("Normalized flux", fontsize=20)
plt.yticks([])
ax1.tick_params(axis='both', which='major', labelsize=15)
ax2.tick_params(axis='both', which='major', labelsize=15)

f.text(0.5, -0.04, 'Wavelength ($\AA$)', ha='center', fontsize=20, color="k")

plt.tight_layout(pad=0.4, rect=[0, 0.03, 1, 0.95])

file_name_write = "junk.pdf"
plt.savefig(file_name_write, bbox_inches='tight')

print("Wrote",file_name_write)
