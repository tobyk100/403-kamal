#!/bin/bash

# This script will hopefully set up everything you need to work
# on a linux system. 

pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
