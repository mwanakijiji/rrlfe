import matplotlib
matplotlib.use('Agg')

import sys, os
from configparser import ConfigParser, ExtendedInterpolation
import pandas as pd
import astropy

current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, target_dir)

# import more things with changed system path
from modules import *
from modules import scrape_ew_and_errew
from conf import *
import numpy as np
import glob

# configuration data for reduction
config_gen = ConfigParser(interpolation=ExtendedInterpolation()) # for parsing values in .init file
# config for reduction to find a, b, c, d
config_gen.read(os.path.join(os.path.dirname(__file__), '../conf', 'config_gen.ini'))

'''
def test_junk_fcn():

    junk = scrape_ew_and_errew.junk_Fcn()

    assert junk
'''

def test_junk_class():

    junk = scrape_ew_and_errew.junk_Class(module_name="junk", var1="test2")

    assert junk