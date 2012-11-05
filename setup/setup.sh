# This script will hopefully set up everything you need to work
# on the lab VM. To use it call source <scriptname> from the command line.
#
curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
python virtualenv.py venv
source ./venv/bin/activate
pip install -r requirements.txt
