#!/usr/bin/env bash

module load python/3.10

mkdir -p ./out/calls/hifi/
mkdir -p ./out/calls/ont/

python ./run_all.py ./longtr.bash hifi
python ./run_all.py ./strkit.bash hifi
python ./run_all.py ./trgt.bash hifi
