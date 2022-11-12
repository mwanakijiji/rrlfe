'''
This is the high-level script which runs all the pieces of the pipeline to
obtain updated Layden coefficients [a, b, c, d]
'''

import os
import sys
import collections
from collections import OrderedDict
from configparser import ConfigParser, ExtendedInterpolation
from conf import *
from modules import *
'''
from modules import (compile_normalization,
                      create_spec_realizations,
                      run_robo,
                      scrape_ew_and_errew,
                      ca_correction,
                      consolidate_pre_mcmc,
                      run_emcee,
                      teff_retrieval)
'''
from modules import (compile_normalization,
                      create_spec_realizations,
                      run_robo,
                      scrape_ew_and_errew,
                      teff_retrieval)


class GenerateCalib():
    '''
    This actually runs the reduction that generates a calibration
    '''
    def __init__(self,
        model_choice = None):

        # dictionary to contain pipeline steps
        self._dict_steps = collections.OrderedDict()

        # define the calibration model
        self.model_choice = model_choice

        # GenerateCalib() is for finding a calibration
        self.objective = "find_calib"

        # read in choice of configuration data file for reduction;
        # set contents as attributes for sections to follow
        config_choice = ConfigParser(interpolation=ExtendedInterpolation()) # for parsing values in .init file
        # config for reduction to find a, b, c, d
        config_choice.read(os.path.join(os.path.dirname(__file__), 'conf', 'config_red.ini')) ## ## THIS HAS TO BE MANUALLY SET BY USER HERE; NEED TO CHANGE THIS

        # set pathnames for important files that are used by different modules
        '''
        self.cc_bkgrnd_file_path_abs = str(config_choice["data_dirs"]["DIR_SRC"] + "/bkgrnd.cc")
        self.compiled_bkgrnd_file_path_abs = str(config_choice["data_dirs"]["DIR_BIN"] + "/bkgrnd")
        '''

        self._attribs = config_choice


    def add_step(self, module):
        '''
        Adds module to the list of things to do
        '''

        #if isinstance(module_name):

        self._dict_steps.update({module.name:module})

        #self._dict_steps[module.name] = module
        '''
        print(type(teff_retrieval.junkAccordionFcn_zap()))
        teff_retrieval.junkAccordionFcn_zap()
        print(str(self.model_choice))
        print(self._dict_steps)
        print("module_name: ", module_name)
        #self._dict_steps[module_name.name] = module_name
        self._dict_steps.update({module_name.name:module_name})
        print(self._dict_steps)
        '''


    def run(self):
        '''
        Loop over steps and run, letting each step inherit the attributes
        from the config file
        '''

        print("tada:",self._dict_steps)


        for exec_id in self._dict_steps.values():
            print("----")
            exec_id.run_step(attribs = self._attribs)
            print("----")
            #self._dict_steps(name)
