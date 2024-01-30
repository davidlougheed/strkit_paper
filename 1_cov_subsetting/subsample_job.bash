#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-4
#SBATCH --account=rrg-bourqueg-ad

module load python/3.9
source ./env_subsam/bin/activate

# TODO
