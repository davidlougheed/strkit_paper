#!/usr/bin/env bash

module load python/3.10

mkdir -p ./out/calls/hifi/
mkdir -p ./out/calls/ont/

# HiFi
python ./run_all.py ./longtr.bash hifi
python ./run_all.py ./straglr.bash hifi
python ./run_all.py ./strdust.bash hifi
python ./run_all.py ./strkit.bash hifi
python ./run_all.py ./strkit-no-snv.bash hifi
python ./run_all.py ./trgt.bash hifi

# ONT: TRGT not permitted
python ./run_all.py ./longtr.bash ont
python ./run_all.py ./straglr.bash ont
python ./run_all.py ./strdust.bash ont
python ./run_all.py ./strkit.bash ont
python ./run_all.py ./strkit-no-snv.bash ont
