#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1-00
#SBATCH --account=rrg-bourqueg-ad

module load samtools python/3.11
python3 ./7_ga4k_coverages.py > ga4k_coverages.txt
