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

  # install dependencies
  wget https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/requirements_bare_versions.txt
  pip install -r requirements_bare_versions.txt


%runscript
  echo "Runscript; Python version is"
  python --version

  # clone rrlfe
  git clone https://github.com/mwanakijiji/rrlfe.git

  # install Robospect
  git clone https://github.com/czwa/robospect.py.git
  cd robospect.py
  git -c advice.detachedHead=false checkout tags/v0.76
  sudo python ./setup.py install
  cd ..
