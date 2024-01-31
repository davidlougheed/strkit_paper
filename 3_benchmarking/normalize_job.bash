#!/bin/bash
#SBATCH --mem=4G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-08
#SBATCH --account=rrg-bourqueg-ad

module load bcftools
bcftools norm -f "${REF}" -c s -m - "${VCF}" -o "${VCF%.*}.norm.vcf"
