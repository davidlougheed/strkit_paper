#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1-00
#SBATCH --account=rrg-bourqueg-ad

module load python/3.9 parasail
source ../envs/env_strkit/bin/activate

strkit call \
  --ref "${REF}" \
  --loci ./out/adotto_catalog_strkit.bed \
  --sex-chr "${KARYOTYPE}" \
  --hq \
  --realign \
  --json "./out/calls/${TECH}/${SAMPLE}.strkit.json" \
  --vcf "./out/calls/${TECH}/${SAMPLE}.strkit.vcf" \
  --seed "${SEED}" \
  "${BAM}"
