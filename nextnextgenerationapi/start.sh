#!/bin/bash
#
echo "Running api"
source env/bin/activate
source .env
python source/flaskapp.py
