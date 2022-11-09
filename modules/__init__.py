'''
Initialization
'''

import os
import git
import sys
import multiprocessing
import logging
from setuptools import Distribution
from setuptools.command.install import install
from datetime import datetime

# get pipeline hash
# warning: may throw error on cluster
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

# set up logging, to print to screen and save to file simultaneously
time_start = datetime.now()
timestring_human = str(time_start)
timestring_start = time_start.strftime("%Y%m%d_%H%M%S")
log_filename = timestring_start + ".log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d [%(levelname)s] %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)


# number of cores to use
#ncpu = multiprocessing.cpu_count()
ncpu = 4

# prompt user if files will be overwritten? (turn to false if running on HPC)
prompt_user = True

# set some constants

# vestigial constant in MCMC (this is NOT an astrophysical Teff)
Teff = 0.0586758
# coefficients from first line of Table 8 in Layden+ 1994
# (reddening not included), to serve as MCMC starting point
a_layden = 13.542
b_layden = -1.072
c_layden = 3.971
d_layden = -0.271


# The class OnlyGetScriptPath() and function get_setuptools_script_dir()
# are from the setup.py script in the Apogee repository by jobovy
# https://github.com/jobovy/apogee/blob/master/setup.py

class OnlyGetScriptPath(install):
    def run(self):
        self.distribution.install_scripts = self.install_scripts

def get_setuptools_script_dir():
    '''
    Get the directory setuptools installs scripts to for current python
    '''
    dist = Distribution({'cmdclass': {'install': OnlyGetScriptPath}})
    dist.dry_run = True  # not sure if necessary
    dist.parse_config_files()
    command = dist.get_command_obj('install')
    command.ensure_finalized()
    command.run()
    return dist.install_scripts


class makeDirs():
    '''
    Make directories for housing files/info if they don't already exist
    '''

    def __init__(self, module_name, objective=None):

        self.name = module_name
        self.objective = "apply_calib"

    def run_step(self, attribs = None):

        logging.info("## Making directories ##")

        # make directories for
        # 1. reduction of spectra to find a, b, c, d (objective = "find_calib"), or
        # 2. to apply the solution (objective = "apply_calib"; default)


        # loop over all directory paths we will need
        for vals in attribs["data_dirs"]:
            abs_path_name = str(attribs["data_dirs"][vals])
            logging.info("Directory exists: " + abs_path_name)

            # if directory does not exist, create it
            if not os.path.exists(abs_path_name):
                original_umask = os.umask(0) # original system permission
                os.makedirs(abs_path_name, 0o777)
                #os.mkdir(abs_path_name)
                logging.info("Made directory " + abs_path_name)
                os.umask(original_umask) # revert to previous permission status

            # if it does exist, check if it is not already empty;
            # if it is non-empty, prompt user (as long as prompt_user
            # flag has been set further above)
            # (this needs to be refined, since some directories are not supposed to be empty)
            if prompt_user and os.path.exists(abs_path_name):
                with os.scandir(abs_path_name) as list_of_entries1:
                    counter1 = 0
                    for entry1 in list_of_entries1:
                        if entry1.is_file():
                            counter1 += 1
                if (counter1 != 0):
                    logging.info("------------------------------")
                    logging.info(abs_path_name)
                    print("The above is a non-empty directory. Do you want to proceed? [Yes]")
                    print("(N.b. You will be prompted again when the directory is written to.)")
                    input()
                    logging.info("------------------------------")

'''
def get_hash():
    # Retrieve git hash

    # warning: may throw error on cluster
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    return sha
'''

class configInit():
    '''
    Print parameters from the config file to log
    '''

    def __init__(self, module_name):

        self.name = module_name
        #self.objective = "apply_calib"

    def run_step(self, attribs = None):

        logging.info("## Begin pipeline configuration parameters ##")

        logging.info("rrlfe git hash: " + sha)
        print(attribs.sections)

        logging.info("Pipeline purpose: find or apply a solution? ")# + objective)

        for each_section in attribs.sections():
            logging.info("----")
            logging.info("- " + each_section + " -")
            for (each_key, each_val) in attribs.items(each_section):
                logging.info(each_key + ": " + each_val)

        logging.info("----")
        logging.info("## End pipeline configuration parameters ##")


def phase_regions():
    '''
    Read in the boundary between good and bad phase regions
    '''

    # obtain values as floats
    value1 = config_red.getfloat("phase", "MIN_GOOD")
    value2 = config_red.getfloat("phase", "MAX_GOOD")

    return value1, value2
