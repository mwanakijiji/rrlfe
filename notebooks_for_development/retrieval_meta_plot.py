#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Makes a meta-plot of various Fe/H retrievals

# Created 2023 Feb 5


# In[1]:


import matplotlib.pyplot as plt
import pandas as pd


# In[2]:


# subplot arrangement

# [0,0]: rrlfe vs. SSPP (single-epoch)
# [0,1]: rrlfe vs. SSPP (coadded)
# [1,0]: rrlfe vs. Liu+
# [1,1]: rrlfe vs. Whitten+
# [2,0]: rrlfe vs. Li+


# In[44]:


df_sspp_single = pd.read_csv("TBD")
df_sspp_coadded = pd.read_csv("TBD")
df_sspp_liu_2020 = pd.read_csv("TBD")
df_sspp_whitten = pd.read_csv("TBD")
df_sspp_li_2022 = pd.read_csv("TBD")


# In[45]:


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

# rrlfe vs. SSPP (single-epoch)
axes[0,0].plot([-4, 1], [-4, 1], linestyle="--")
axes[0,0].set_xlim(xlim)
axes[0,0].set_ylim(ylim)
axes[0,0].set(adjustable='box', aspect='equal')
axes[0,0].set_xlabel("SSPP (single-epoch)", fontsize = char_size)
axes[0,0].set_ylabel("rrlfe", fontsize = char_size)


# rrlfe vs. SSPP (coadded)
axes[0,1].plot([-4, 1], [-4, 1], linestyle="--")
axes[0,1].set_xlim(xlim)
axes[0,1].set_ylim(ylim)
axes[0,1].set_xlabel("SSPP (coadded)", fontsize = char_size)
axes[0,1].set(adjustable='box', aspect='equal')

# rrlfe vs. Liu+
axes[1,0].plot([-4, 1], [-4, 1], linestyle="--")
axes[1,0].set_xlim(xlim)
axes[1,0].set_ylim(ylim)
axes[1,0].set_xlabel("Liu+ 2020", fontsize = char_size)
axes[1,0].set(adjustable='box', aspect='equal')

axes[1,0].set_ylabel("rrlfe", fontsize = char_size)

# rrlfe vs. Whitten+
axes[1,1].plot([-4, 1], [-4, 1], linestyle="--")
axes[1,1].set_xlim(xlim)
axes[1,1].set_ylim(ylim)
axes[1,1].set_xlabel("Whitten+ 2021", fontsize = char_size)
axes[1,1].set(adjustable='box', aspect='equal')

# rrlfe vs. Li+
axes[2,0].plot([-4, 1], [-4, 1], linestyle="--")
axes[2,0].set_xlim(xlim)
axes[2,0].set_ylim(ylim)
axes[2,0].set_xlabel("Li+ 2022", fontsize = char_size)
axes[2,0].set(adjustable='box', aspect='equal')
axes[2,0].set_ylabel("rrlfe", fontsize = char_size)

# TBD: leave blank?
axes[2,1].plot([-4, 1], [-4, 1], linestyle="--")
axes[2,1].set_xlim(xlim)
axes[2,1].set_ylim(ylim)
axes[2,1].set(adjustable='box', aspect='equal')

plt.subplots_adjust(wspace=0.0, hspace=0.2)

#for ax in axes:
#$    ax.plot([1, 2, 3], [1, 2, 3])
#    ax.set(adjustable='box', aspect='equal')


# In[ ]:




