#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from astroquery.sdss import SDSS
from astropy import coordinates as coords
import astropy.units as u
from astropy.io import fits
import time

stem = '/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/'

df = pd.read_csv(stem + 'li_catalog_ra_dec.csv', names=['ra','dec'])
stem_write = './tbd_dir/'

for idx in range(0,len(df)):
        
    ra = np.round(df.loc[idx]['ra'],4)
    dec = np.round(df.loc[idx]['dec'],4)

    print('ra:',ra)
    print('dec:',dec)
    
    co = coords.SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')
    result = SDSS.query_region(co, radius=2*u.arcsec, spectro=True)
    
    if result:
        try: 
            spec = SDSS.get_spectra(matches=result)
            
            for epoch_num in range(0,len(spec)):
                
                file_name_write = 'obj_id_' + str(int(spec[epoch_num][0].header['spec_id'])) + '.fits'
                spec[epoch_num].writeto(stem_write + file_name_write, overwrite=True)
                print('Wrote',file_name_write)
            
        except:
            print('Match but no spec for ',co)

    print('---------')
        
    # keep the sdss server happy
    if idx%40 == 0:
        
        time.sleep(61)
