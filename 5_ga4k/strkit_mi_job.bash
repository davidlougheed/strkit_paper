#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --account=rrg-bourqueg-ad

mkdir -p ./out/mi

module load StdEnv/2023
module load python/3.11 scipy-stack/2025a parasail/2.6.2
source ../envs/env_strkit/bin/activate

export PYTHONOPTIMIZE=1

strkit mi \
    --caller "${MI_CALLER}" \
    "./out/calls/${CHILD}.${CALLER}.vcf.gz" \
    "./out/calls/${FATHER}.${CALLER}.vcf.gz" \
    "./out/calls/${MOTHER}.${CALLER}.vcf.gz" \
    --hist \
    --motif-bed "./out/adotto_catalog_strkit.bed" \
    --json "${OUT_JSON}"

deactivate
