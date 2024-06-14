#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-8
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 scipy-stack/2023b parasail/2.6.2

time python3 ./call_longtr.py

source ../envs/env_strkit/bin/activate
time python3 ./call_strkit.py
deactivate

time python3 ./call_trgt.py
