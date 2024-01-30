#!/usr/bin/env bash

#python3 ./call_longtr.py

source ../envs/env_strkit/bin/activate
python3 ./call_strkit.py
deactivate

python3 ./call_trgt.py
