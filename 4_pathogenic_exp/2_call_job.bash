#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-8
#SBATCH --account=rrg-bourqueg-ad

module load python/3.9

#python3 ./call_longtr.py

source ../envs/env_strkit/bin/activate
python3 ./call_strkit.py
deactivate

python3 ./call_trgt.py
