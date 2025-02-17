#!/bin/bash
#SBATCH --mem=5G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --account=rrg-bourqueg-ad

mkdir -p ./out/mi

module load StdEnv/2023
module load python/3.11 scipy-stack/2023b parasail/2.6.2
source ../envs/env_strkit/bin/activate

export PYTHONOPTIMIZE=1

strkit mi --caller strkit-vcf \
    "./out/calls/${CHILD}.strkit.vcf.gz" \
    "./out/calls/${FATHER}.strkit.vcf.gz" \
    "./out/calls/${MOTHER}.strkit.vcf.gz" \
    --hist \
    --mismatch-out-mi seq \
    --json "${OUT_JSON}"

deactivate
