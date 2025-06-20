#!/usr/bin/env bash

module load python/3.11

mkdir -p ./out/calls/hifi/
mkdir -p ./out/calls/ont/
mkdir -p ./out/calls/ont-simplex/

# HiFi -----------------------------------------------------------------------------------------------------------------
python ./run_all.py ./longtr.bash hifi ""
python ./run_all.py ./straglr.bash hifi ""
python ./run_all.py ./strdust.bash hifi ""
python ./run_all.py ./strkit.bash hifi ""
python ./run_all.py ./strkit-no-snv.bash hifi ""
python ./run_all.py ./trgt.bash hifi ""

# ONT: TRGT not permitted ----------------------------------------------------------------------------------------------

#  - Simplex
python ./run_all.py ./longtr.bash ont-simplex ""
python ./run_all.py ./straglr.bash ont-simplex ""
python ./run_all.py ./strdust.bash ont-simplex ""
python ./run_all.py ./strkit.bash ont-simplex ""
python ./run_all.py ./strkit-no-snv.bash ont-simplex ""

#  - Duplex
python ./run_all.py ./longtr.bash ont ""
python ./run_all.py ./straglr.bash ont ""
python ./run_all.py ./strdust.bash ont ""
python ./run_all.py ./strkit.bash ont ""
python ./run_all.py ./strkit-no-snv.bash ont ""

# HiFi - phased (no SNVs for STRkit) -----------------------------------------------------------------------------------
python ./run_all.py ./longtr.bash hifi "1"
python ./run_all.py ./strdust.bash hifi "1"
python ./run_all.py ./strkit.bash hifi "1"
python ./run_all.py ./trgt.bash hifi "1"
