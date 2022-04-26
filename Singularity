Bootstrap: docker
From: python:3.8

# copy files required for the app to run (this might be subsumed by pip command)

# get files from host (but we don't need any)

%environment
  # set environment variable to retrieve new image each time
  export SINGULARITY_DISABLE_CACHE=True

%post

  # install pip
  apt-get update
  apt-get install -y python3-pip
  pip install --upgrade pip

  # install dependencies into default python interpreter
  wget https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/requirements_bare_versions.txt


%runscript

  echo "Runscript; Python version is"
  python --version

  # clone rrlfe
  git clone https://github.com/mwanakijiji/rrlfe.git

  # install Robospect, suppress comments about being in detached HEAD state
  git clone https://github.com/czwa/robospect.py.git
  cd robospect.py
  git -c advice.detachedHead=false checkout tags/v0.76
  mkdir tmp/
  python ./setup.py install --user
  cd ../rrlfe
  python -m pip install -r requirements_bare_versions.txt

  # do a pip freeze
  pip freeze > freeze_bad.txt

  # copy line list file
  cp ll ../robospect.py/tmp/

  # exec --bind $HOME/sandbox/rrlfe:/Users/bandari/Documents/git.repos/rrlfe,$HOME/sandbox/robospect.py:/Users/bandari/Documents/git.repos/robospect.py test.sif python rrlfe/high_level_reduction_script.py
