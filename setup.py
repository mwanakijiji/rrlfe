# We will need:
# C++ (for Carrell's script)
# Python (for the wrapper in the first place)
# GSL ver1 as the libgsl0-dev package (for Robospect)

from setuptools import setup, Extension
from setuptools.command.install import install
import sys
import shlex
import subprocess
from subprocess import Popen,PIPE
from setuptools import setup, find_packages

long_description = "For determining metallicities of RR Lyraes from low-res spectroscopy see `here <https://rrlfe.readthedocs.io>`__ for more info"

setup(name="rrlfe",
      version="0.1",
      description="For finding FeH from low-res survey spectra of RR Lyrae stars",
      long_description=long_description,
      author="Eckhart Spalding, Ron Wilhelm, Nathan De Lee, Kenneth Carrell",
      author_email="eckhart.spalding@sydney.edu.au",
      url="https://github.com/mwanakijiji/rrlfe",
      download_url="https://github.com/mwanakijiji/rrlfe/archive/refs/tags/v_0.0.12.tar.gz",
      packages=find_packages(),
      include_package_data=True
      )