#!/usr/bin/env python
# coding: utf-8

# Makes publication plot comparing our periods with those in GCVS5

# Created 2023 Aug 2 by E.S.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

stem = '/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/'

df = pd.read_csv(stem + 'period_comparison_gcvs5_us.txt', delimiter='|')

# for scaling the residuals such that the ordinate reads ~1
coeff_scaling_resid = np.power(10,4.)

fig, (a0, a1) = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [1, 0.5]}, sharex=True, figsize=(8,7))

a0.scatter(df['P_gcvs5'],df['us'],color='red',edgecolor='k')
a0.plot([0.2,0.75],[0.2,0.75], linestyle='--', color='gray')

for int_ in df.index:

    # FYI
    print('---')
    print(df['name'][int_])
    print(coeff_scaling_resid*(df['us'][int_]-df['P_gcvs5'][int_]))

    # underplot vertical lines
    a0.plot([df['P_gcvs5'][int_],df['us'][int_]],[df['P_gcvs5'][int_],-10], color='r', alpha = 0.5, zorder=0)
    a1.plot([df['P_gcvs5'][int_],df['us'][int_]],np.multiply(coeff_scaling_resid,[df['us'][int_]-df['P_gcvs5'][int_],10]), color='r', alpha = 0.5, zorder=0)
    
    if df['name'][int_] in ['BH Peg','TU UMa', 'RR Leo', 'AV Peg', 'V535 Mon']:
        
        a0.annotate('   '+df['name'][int_],
                    xy=(df['P_gcvs5'][int_]-0.005, df['us'][int_]-0.005), xycoords='data', xytext=(0,0), 
                    textcoords='offset pixels', rotation=-45, rotation_mode='anchor', ha='left', fontsize=13)
        
    elif df['name'][int_] in ['RU Psc', 'RR Cet']:
        
        a0.annotate(df['name'][int_] + '   ',
                    xy=(df['P_gcvs5'][int_], df['us'][int_]), xycoords='data', xytext=(-10,-7), 
                    textcoords='offset pixels', rotation=-45, rotation_mode='anchor', ha='right', fontsize=13)
        a0.annotate('',
                    xy=(df['P_gcvs5'][int_], df['us'][int_]), xycoords='data', xytext=(-10,0), 
                    textcoords='offset pixels', rotation=-45, rotation_mode='anchor', ha='right',
                    arrowprops =dict(arrowstyle='wedge,tail_width=2', mutation_scale=2, linewidth=0, color='k'))
    
    else:

        a0.annotate(df['name'][int_] + '   ',
                xy=(df['P_gcvs5'][int_]-0.005, df['us'][int_]-0.005), xycoords='data', xytext=(0,0), 
                    textcoords='offset pixels', rotation=-45, rotation_mode='anchor', ha='right', fontsize=13)

a1.set_xlabel('Period, GCVS 5 (day)', fontsize=20)
a0.set_ylabel('Period, this work (day)', fontsize=20)
#a1.set_ylabel('Residuals\n(day $\cdot 10^{-4}$ )', fontsize=20)
a1.set_ylabel('Residuals $\cdot 10^{-4}$', fontsize=20)

#a0.set_aspect('equal')

a1.plot([0.2,0.75],[0.,0.], linestyle='--', color='gray')
a1.scatter(df['P_gcvs5'],coeff_scaling_resid*(df['us']-df['P_gcvs5']),color='red',edgecolor='k')

a1.set_yticks(np.arange(-2.,2,0.5))
a0.set_ylim([0.17,0.78])
a1.set_ylim([-1.5,1.5])
a0.tick_params(axis='both', which='major', labelsize=15)
a1.tick_params(axis='both', which='both', labelsize=15)


plt.tight_layout()

file_name = 'junk.pdf'
plt.savefig(file_name)
print(file_name)
print('Note the residuals are scaled in y by 10^4')
