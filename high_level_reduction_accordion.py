'''
This is the high-level script which runs all the pieces of the pipeline to
obtain updated Layden coefficients [a, b, c, d]
'''

import sys
import collections
from collections import OrderedDict
from conf import *
from modules import *
from modules import (compile_normalization,
                      create_spec_realizations,
                      run_robo,
                      scrape_ew_and_errew,
                      ca_correction,
                      consolidate_pre_mcmc,
                      run_emcee,
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
        #global objective
        #self.objective = "find_calib"


    def add_step(self, module):
        '''
        Adds module to the list of things to do
        '''

        #if isinstance(module_name):

        self._dict_steps.update({module.name:module})
        print(self._dict_steps)

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
        Loop over steps and run
        '''

        print("tada:",self._dict_steps)


        for exec_id in self._dict_steps.values():
            print("----")
            exec_id.run_step()
            print("----")
            #self._dict_steps(name)
