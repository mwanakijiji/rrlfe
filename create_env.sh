#!/bin/bash
conda create -n rrlfe_env python=3.8 --yes
source $(conda info --base)/etc/profile.d/conda.sh
conda install -n rrlfe_env pip