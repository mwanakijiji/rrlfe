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

df_spec_0 = pd.read_csv(stem + "/X_Ari__03_noise_ver_000.dat", names=["wavel","flux"], delim_whitespace=True)
df_spec_1 = pd.read_csv(stem + "/X_Ari__10_noise_ver_000.dat", names=["wavel","flux"], delim_whitespace=True)
df_spec_2 = pd.read_csv(stem + "/X_Ari__07_noise_ver_000.dat", names=["wavel","flux"], delim_whitespace=True)

plt.clf()
plt.plot(df_spec_0["wavel"], df_spec_0["flux"], color="k")
plt.annotate("$\phi$=0.40", xy=(4600,0.6+0.0), xytext=(4500,0.7+0.0), fontsize=22)

plt.plot(df_spec_1["wavel"], df_spec_1["flux"]+0.5, color="k")
plt.annotate(str(0.64), xy=(4600,0.6+0.5), xytext=(4600,0.7+0.5), fontsize=22)

plt.plot(df_spec_2["wavel"], df_spec_2["flux"]+1., color="k")
plt.annotate(str(0.98), xy=(4600,0.6+1.0), xytext=(4600,0.7+1.0), fontsize=22)

# denote lines
plt.annotate("H" + r"$\beta$", xy=(4862,2.2), xytext=(4861-30,2.2), fontsize=15, rotation=0)
plt.annotate("H" + r"$\gamma$", xy=(4340,2.2), xytext=(4340-30,2.2), fontsize=15, rotation=0)
plt.annotate("H" + r"$\delta$", xy=(4102,2.0), xytext=(4102+70,2.2), fontsize=15, arrowprops=dict(facecolor='black', arrowstyle="-"), rotation=0)
plt.annotate("H" + r"$\epsilon$", xy=(3970,2.0), xytext=(3970+80,2.15), fontsize=15, arrowprops=dict(facecolor='black', arrowstyle="-"), rotation=0)
plt.annotate("CaIIH", xy=(3968.469,2.0), xytext=(3970+50,2.35), fontsize=15, arrowprops=dict(facecolor='black', arrowstyle="-"), rotation=0)
plt.annotate("CaIIK", xy=(3933.7,2.0), xytext=(3933.7-40,2.2), fontsize=15, arrowprops=dict(facecolor='black', arrowstyle="-"), rotation=0)

file_name_write = "junk.pdf"
plt.xlabel("Wavelength ($\AA$)", fontsize=25)
plt.ylabel("Normalized flux", fontsize=25)
plt.yticks([])
plt.xticks(fontsize=20)
plt.ylim(0.2,2.5)
plt.tight_layout()
plt.savefig(file_name_write)

print("Wrote",file_name_write)
