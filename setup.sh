# This script will hopefully set up everything you need to work
# on the lab VM. To use it call source <scriptname> from the command line.
#
curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
python virtualenv.py vevn
source ./venv/bin/activate
sudo yum install /usr/include/libpq-fe.h
sudo yum install postgresql
pip install -r requirements.txt
