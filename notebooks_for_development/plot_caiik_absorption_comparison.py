import matplotlib.pyplot as plt
import pandas as pd

stem = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/"
file_name = stem + "caii_ew_ism_contamination.csv"

df = pd.read_csv(file_name, skiprows=4)

x = df.loc[:, ['max_ism']]
df.sort_values('max_ism', inplace=True)
df.reset_index(inplace=True)

# Draw plot
plt.figure(figsize=(14,10), dpi= 80)
plt.scatter(df.max_ism, df.index, s=140, marker="<", color="red", label="ISM")
plt.scatter(df.min_caiik_ew, df.index, s=140, marker=">", color="k", label="Measured (min)")
plt.scatter(df.max_caiik_ew, df.index, s=140, marker="<", color="k", label="Measured (max)")
#[plt.plot(df.min_caiik_ew, df.max_caiik_ew) for star_name in df.index]
plt.hlines(y=df.index, xmin=df.min_caiik_ew, xmax=df.max_caiik_ew, color="k", lw=3)

# Decorations
# Lighten borders
plt.gca().spines["top"].set_alpha(.3)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(.3)
plt.gca().spines["left"].set_alpha(.3)

plt.xticks(fontsize=30)
plt.yticks(df.index, df.name, fontsize=30)
plt.xlabel("Ca II K EW ($\AA$)", fontsize=30)
plt.grid(linestyle='--', alpha=0.5)
plt.xlim(0, 13)
#plt.legend(loc="lower right", fontsize=30)
plt.tight_layout()
plt.savefig("junk.pdf")
