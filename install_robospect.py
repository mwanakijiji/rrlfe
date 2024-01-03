import subprocess
import os

current_dir = os.getcwd()

# The URL of the Git repository to clone
repo_url = "https://github.com/czwa/robospect.py.git"

# The directory where the repo will be cloned (parent dir to rrlfe)
clone_dir = current_dir+"/../"

# Clone the repo
print("Cloning robospect.py...")
subprocess.run(["git", "clone", repo_url, clone_dir+"robospect.py"])

# Python commands
print("Installing robospect.py...")
subprocess.run(["python3", clone_dir+"robospect.py/setup.py", "install"])
subprocess.run(["mkdir", clone_dir+"robospect.py/tmp"])
print("Adding absorption line list...")
subprocess.run(["cp", "ll", "../robospect.py/tmp"])