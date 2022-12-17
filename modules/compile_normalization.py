from subprocess import Popen, PIPE#, check_call, CalledProcessError
import shutil
from . import * # read in config file, basic functions (logging)

class CompileBkgrnd():
    """
    Compile background routine for spectrum normalization

    Returns:
        bool: 'True' if compile was successful
    """

    def __init__(self, module_name):

        self.name = module_name

    def run_step(self, attribs = None):

        cc_bkgrnd_file_path_abs = str(attribs["data_dirs"]["DIR_SRC"] + "/bkgrnd.cc")
        compiled_bkgrnd_file_path_abs = str(attribs["data_dirs"]["DIR_BIN"] + "/bkgrnd")

        logging.info("## Making directories ##")

        _COMPILE_BKGRND = True
        if _COMPILE_BKGRND:
            if True:

                logging.info("--------------------------")
                logging.info("Compiling background normalization script...")
                bkgrnd_compile = Popen(["g++", "-o",
                                        compiled_bkgrnd_file_path_abs,
                                        cc_bkgrnd_file_path_abs],
                                        stdout=PIPE, stderr=PIPE)

                output, error = bkgrnd_compile.communicate()
                if bkgrnd_compile.returncode != 0:
                    print("Compile error %d %s %s" % (bkgrnd_compile.returncode, output, error))
                    success_val = bool(False)
                else:
                    logging.info("Binary for spectrum normalization saved to")
                    logging.info(compiled_bkgrnd_file_path_abs)
                    logging.info("--------------------------")
                    success_val = bool(True)

        return success_val
