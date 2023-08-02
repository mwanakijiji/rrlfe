#!/usr/bin/env python
# coding: utf-8

# Makes publication plot comparing our periods with those in GCVS5

# Created 2023 Aug 2 by E.S.

import matplotlib.pyplot as plt
import pandas as pd

stem = '/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/'

df = pd.read_csv(stem + 'period_comparison_gcvs5_us.txt', delimiter='|')

fig, ax = plt.subplots(figsize=(4, 4))

ax.scatter(df['P_gcvs5'],df['us'],color='red',edgecolor='k')
ax.plot([0.2,0.75],[0.2,0.75], linestyle='--', color='gray')

for int_ in df.index:
    
    if df['name'][int_] in ['BH Peg','TU UMa', 'RR Leo', 'AV Peg', 'V535 Mon']:
        
        ax.annotate('   '+df['name'][int_],
                    xy=(df['P_gcvs5'][int_]-0.005, df['us'][int_]-0.005), xycoords='data', xytext=(0,0), 
                    textcoords='offset pixels', rotation=-45, rotation_mode='anchor', ha='left')
        
    elif df['name'][int_] in ['RU Psc', 'RR Cet']:
        
        ax.annotate(df['name'][int_] + '   ',
                    xy=(df['P_gcvs5'][int_], df['us'][int_]), xycoords='data', xytext=(-7,-7), 
                    textcoords='offset pixels', rotation=-45, rotation_mode='anchor', ha='right')
        ax.annotate('',
                    xy=(df['P_gcvs5'][int_], df['us'][int_]), xycoords='data', xytext=(-10,0), 
                    textcoords='offset pixels', rotation=-45, rotation_mode='anchor', ha='right',
                    arrowprops =dict(arrowstyle='wedge,tail_width=2', mutation_scale=2, linewidth=0, color='k'))
    
    else:

        ax.annotate(df['name'][int_] + '   ',
                xy=(df['P_gcvs5'][int_]-0.005, df['us'][int_]-0.005), xycoords='data', xytext=(0,0), 
                    textcoords='offset pixels', rotation=-45, rotation_mode='anchor', ha='right')

ax.set_xlabel('Period, GCVS 5 (day)')
ax.set_ylabel('Period, this work (day)')

ax.set_aspect('equal')
plt.savefig('junk.pdf')
