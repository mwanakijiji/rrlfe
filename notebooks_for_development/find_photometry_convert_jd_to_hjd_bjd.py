#!/usr/bin/env python
# coding: utf-8

# This calculates MJDs and BJDs of light curve maxima, as observed at MacAdam, U Louisville, and Mt. Kent in Australia

# created 2018 Jan 02 by E.S.

import astropy
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
from astropy import time, coordinates as coord, units as u
from astropy.time import Time
from dateutil.parser import parse
import glob

# read in list of epochs-of-max in JD, and add columns of HJD and BJD

file_path = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/photometry_max_epochs_jd.csv"

photometry_jd = pd.read_csv(file_path)

########################################
## FIND HJDs, BJDs
########################################

# set observatory coordinates

loc_mcdonald = coord.EarthLocation.from_geodetic(lon=-104.022438,lat=30.671626,height=2076,ellipsoid='WGS84')
loc_macadam = coord.EarthLocation.from_geodetic(lon=-84.503758,lat=38.033949,height=298,ellipsoid='WGS84')
loc_mtKent = coord.EarthLocation.from_geodetic(lon=151.855484,lat=-27.797708,height=682,ellipsoid='WGS84')
loc_ulmo = coord.EarthLocation.from_geodetic(lon=-85.528756,lat=38.344543,height=142,ellipsoid='WGS84')

# make time objects

photometry_times = Time(photometry_jd['jd'], format='jd')

# fcn to convert MJD to BJD times

'''
DO NOT USE THIS! 0.5 DAY BUG HERE; USE JD_TO_BJD
def convert_mjd_to_bjd(mjdTimes,observatoryLoc,skyCoordObj):

    timesObj = time.Time(mjdTimes, format='mjd', scale='utc', location=observatoryLoc)
    ltt_bary = timesObj.light_travel_time(skyCoordObj)

    time_barycentre = timesObj.tdb + ltt_bary

    return time_barycentre
'''


# fcn to convert JD to BJD times


# THIS WAS BEING TESTED AND GAVE SAME ANSWERS AS convert_mjd_to_bjd()
def convert_jd_to_bjd(jdTimes,observatoryLoc,skyCoordObj):

    timesObj = time.Time(jdTimes, format='jd', scale='utc', location=observatoryLoc)
    ltt_bary = timesObj.light_travel_time(skyCoordObj)

    time_barycentre = timesObj.tdb + ltt_bary

    return time_barycentre


# fcn to convert MJD to HJD times

'''
DO NOT USE THIS! 0.5 DAY BUG HERE; USE JD_TO_BJD
def convert_mjd_to_hjd(mjdTimes,observatoryLoc,skyCoordObj):

    timesObj = time.Time(mjdTimes, format='mjd', scale='utc', location=observatoryLoc)
    ltt_helio = timesObj.light_travel_time(skyCoordObj, 'heliocentric')

    times_heliocentre = timesObj.utc + ltt_helio

    return times_heliocentre.mjd
'''

# read in star name, return file names and BJDs of epochs-of-max

def return_star_epochs_photometry(starNames,jdTimes,observatoryLocs):
    # returns cols of MJD, HJD, and BJD

    if len(starNames) != len(jdTimes): # something must be wrong!
        return

    # initialize a pandas dataframe
    df = pd.DataFrame()

    # convert jds to mjds
    mjdTimes = jdTimes.mjd

    thisStar = []
    observatoryThisStar = []
    jdThisStar = []
    #mjdThisStar = []
    #hjdThisStar = []
    bjdThisStar = []

    # go through each row in file
    for t in range(0,len(jdTimes)):

        # make a star coordinate object
        coord_thisStar = coord.SkyCoord.from_name(starNames[t])
        print("==========")
        print(starNames[t])
        print("coords star: ", coord_thisStar)

        # determine observatory location
        if (observatoryLocs[t] == 'MSO'): observ_thisStar = loc_macadam
        if (observatoryLocs[t] == 'MtKent'): observ_thisStar = loc_mtKent
        if (observatoryLocs[t] == 'ULMO'): observ_thisStar = loc_ulmo

        thisStar.append(starNames[t])
        observatoryThisStar.append(observatoryLocs[t])
        jdThisStar.append(jdTimes[t].jd)
        #mjdThisStar.append(mjdTimes[t])
        #hjdThisStar.append(convert_mjd_to_hjd(mjdTimes[t],observ_thisStar,coord_thisStar))
        #
        #bjdThisStar.append(convert_jd_to_bjd(mjdTimes[t],observ_thisStar,coord_thisStar))
        bjdThisStar.append(convert_jd_to_bjd(jdTimes.jd[t],observ_thisStar,coord_thisStar))
        print("BJD from JD:", convert_jd_to_bjd(jdTimes.jd[t],observ_thisStar,coord_thisStar))
        #print("BJD from MJD:", convert_mjd_to_bjd(jdTimes.mjd[t],observ_thisStar,coord_thisStar))

    df['star'] = thisStar
    df['observatory'] = observatoryThisStar
    df['jd'] = jdThisStar
    #df['mjd'] = mjdThisStar
    #df['hjd'] = hjdThisStar
    df['bjd'] = bjdThisStar

    return df

# find

photometryEpochs = return_star_epochs_photometry(photometry_jd['star'],photometry_times,photometry_jd['observatory'])

# write out csv

file_name_out = 'junk.csv'
photometryEpochs.to_csv(file_name_out)
print("Wrote ", file_name_out)
