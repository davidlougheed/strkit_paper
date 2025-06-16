#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=15:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 scipy-stack/2025a parasail/2.6.2

# LongTR
time python3 ./call_longtr.py

# Straglr
export PATH="${PATH}:${PWD}/../bin"  # for TRF
source ../envs/env_straglr/bin/activate
time python3 ./call_straglr.py
deactivate

# STRdust
time python3 ./call_strdust.py

# STRkit
source ../envs/env_strkit/bin/activate
time python3 ./call_strkit.py
deactivate

# TRGT
time python3 ./call_trgt.py
