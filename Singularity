Bootstrap: docker
From: python:3.6.6

# copy files required for the app to run (this might be subsumed by pip command)

# get files from host (but we don't need any)

%environment
  # set environment variable to retrieve new image each time
  export SINGULARITY_DISABLE_CACHE=True

%post
  # install Robospect
  git clone https://github.com/czwa/robospect.py.git
  cd robospect.py
  git checkout tags/v0.76
  sudo apt-get install python3-setuptools
  sudo apt install python3-distutils
  python ./setup.py install
  cd ..
  # clone rrlfe
  git clone https://github.com/mwanakijiji/rrlfe.git
  cd rrlfe
  # install pip
  apt-get update
  apt-get install -y python3-pip
  pip install -U pip
  # install dependencies
  pip install -r requirements.txt

%runscript
  echo "Runscript; Python version is"
  python --version
