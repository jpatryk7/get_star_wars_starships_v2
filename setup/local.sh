#!/bin/bash

ACTIVATE_PATH=$(find . -type f -name 'activate')

if ![ $ACTIVATE_PATH ]; then
  python -m venv my_venv
  ACTIVATE_PATH=$(./my_venv/Scripts/activate)
fi

source $ACTIVATE_PATH
pip install -r requirements.txt
python -m get_ships_v2