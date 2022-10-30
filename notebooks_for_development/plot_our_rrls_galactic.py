#!/usr/bin/env python
# coding: utf-8

# This plots our RR Lyrae stars in galactic coordinates, so as to see where they are relative
# to the SDSS Ca absorption footprint (Murga+ 2015 MNRAS 452, 511)

# created 2018 July 8 by E.S.

import numpy as np
import pandas as pd
import astropy.coordinates as coord
import astropy.units as u
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.interpolate import SmoothSphereBivariateSpline
from scipy.interpolate import RectSphereBivariateSpline
from astropy.coordinates import SkyCoord

stem = "/Users/bandari/Documents/git.repos/rrlfe/"

# read coord data on our RRLs
stars = pd.read_csv(stem + "notebooks_for_development/data/rrl_gal_coords.csv")

# read in measured Ca II K EWs from our RRLs; use this manually, with lines such as
# > idx = df_ews["orig_spec_file_name"].str.contains("RW_Ari", case=False)
# > np.nanmin(df_ews["EW_CaIIK"].loc[idx])
df_ews = pd.read_csv(stem + "rrlfe_io_20220803_01_mcd/bin/retrieved_vals_20220803.csv")
import ipdb; ipdb.set_trace()

# define read-in data as degrees
gal_lon_l_all = coord.Angle(stars['gal_lon_l']*u.degree)
gal_lat_b_all = coord.Angle(stars['gal_lat_b']*u.degree)
gal_lon_l_ab = coord.Angle(stars['gal_lon_l'].loc[stars['type']=='ab']*u.degree)
gal_lat_b_ab = coord.Angle(stars['gal_lat_b'].loc[stars['type']=='ab']*u.degree)
gal_lon_l_c = coord.Angle(stars['gal_lon_l'].loc[stars['type']=='c']*u.degree)
gal_lat_b_c = coord.Angle(stars['gal_lat_b'].loc[stars['type']=='c']*u.degree)

# make coordinates
stars_coords_all = coord.Galactic(l=gal_lon_l_all,b=gal_lat_b_all)
stars_coords_ab = coord.Galactic(l=gal_lon_l_ab,b=gal_lat_b_ab)
stars_coords_c = coord.Galactic(l=gal_lon_l_c,b=gal_lat_b_c)

# read in Ca data
image, header = fits.getdata('./data/maps_EW(CaNa)_20150318.fits',0,header=True)

# convert Ca absorption data into coordinates
cak_lon_l = coord.Angle(image['longitude']*u.degree)
cak_lat_b = coord.Angle(image['latitude']*u.degree)
cak_ew = image['Ca_K_EW ']
cak_coords = coord.Galactic(l=cak_lon_l,b=cak_lat_b)

# replace zeros with nans
cak_ew[cak_ew == 0] = 'nan'

# the full Muraveva map
'''
plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111, projection="mollweide")
#plt.scatter(image['longitude']*np.pi/180., image['latitude']*np.pi/180., c=cak_ew, cmap=cm.Reds)
plt.scatter(cak_coords.l.wrap_at(180*u.deg).rad, cak_coords.b.wrap_at(180*u.deg).rad,
            c=cak_ew, vmin=0, vmax=0.5, edgecolors='none')
plt.plot(stars_coords_ab.l.wrap_at(180*u.deg).rad, stars_coords_ab.b.wrap_at(180*u.deg).rad, 'o', color='k', markersize=10, markeredgewidth=4)
plt.plot(stars_coords_c.l.wrap_at(180*u.deg).rad, stars_coords_c.b.wrap_at(180*u.deg).rad, 'x', color='red', markersize=10, markeredgewidth=4)

for i, txt in enumerate(stars['name']):
    ax.annotate(stars['name'][i], (stars_coords_all.l.wrap_at(180*u.deg).rad[i],stars_coords_all.b.wrap_at(180*u.deg).rad[i]))

#plt.gca().invert_xaxis()
ax.grid(True)
plt.suptitle('CaK absorption coverage (Murga+ 2015, esp. Fig. 2); black dots = our RRabs; xs = our RRcs')
plt.xlabel('galactic l')
plt.ylabel('galactic b')
plt.colorbar()
plt.show()
'''

# coords sampled in Ca maps
catalog = SkyCoord(cak_coords.l.rad*u.rad, cak_coords.b.rad*u.rad, frame='galactic')

# for each program star, find the maximum of Ca absorption values that are within
# a given angle of it, and compare it to the EWs that we actually measure for that star
for rrl_num in range(0,len(stars)):

    # make cross-matching
    # (N.b. Resolution elements in Muraveva maps are ~3.7x3.7 deg^2)
    c_rrl = SkyCoord([stars["gal_lon_l"].loc[rrl_num]]*u.deg, [stars["gal_lat_b"].loc[rrl_num]]*u.deg, frame='galactic')
    idxc, idxcatalog, d2d, d3d = catalog.search_around_sky(c_rrl, seplimit = 7.4*u.deg)

    # find max Ca absorption within given angle
    print("---------------")
    print("Star: "+stars["name"].loc[rrl_num])
    print(np.nanmax(cak_ew[idxcatalog]))

    # plot for confirmation code is working right
    '''
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="mollweide")
    #plt.scatter(image['longitude']*np.pi/180., image['latitude']*np.pi/180., c=cak_ew, cmap=cm.Reds)
    plt.scatter(cak_coords.l.wrap_at(180*u.deg)[idxcatalog].rad, cak_coords.b.wrap_at(180*u.deg)[idxcatalog].rad,
                c=cak_ew[idxcatalog], vmin=0, vmax=0.5, edgecolors='none')
    plt.scatter(stars_coords_all.l[rrl_num].rad,stars_coords_all.b[rrl_num].rad, s=10, color="k")
    #plt.plot(stars_coords_ab.l.wrap_at(180*u.deg).rad, stars_coords_ab.b.wrap_at(180*u.deg).rad, 'o', color='k', markersize=10, markeredgewidth=4)
    #plt.plot(stars_coords_c.l.wrap_at(180*u.deg).rad, stars_coords_c.b.wrap_at(180*u.deg).rad, 'x', color='red', markersize=10, markeredgewidth=4)

    ax.annotate(stars['name'][rrl_num], (stars_coords_all.l.wrap_at(180*u.deg).rad[rrl_num],stars_coords_all.b.wrap_at(180*u.deg).rad[rrl_num]))

    #plt.gca().invert_xaxis()
    ax.grid(True)
    plt.suptitle('CaK absorption coverage (Murga+ 2015, esp. Fig. 2); black dots = our RRabs; xs = our RRcs')
    plt.xlabel('galactic l')
    plt.ylabel('galactic b')
    plt.colorbar()
    plt.show()
    '''
