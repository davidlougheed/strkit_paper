#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3-00
#SBATCH --account=rrg-bourqueg-ad

module load python/3.11 parasail
source ../envs/env_strkit/bin/activate

#  --realign \
strkit call \
  --ref "${REF}" \
  --loci ./out/adotto_catalog_strkit.bed \
  --sex-chr "${KARYOTYPE}" \
  --hq \
  --incorporate-snvs "./data/00-common_all.vcf.gz" \
  --json "./out/calls/${TECH}/${SAMPLE}.strkit.json" \
  --vcf "./out/calls/${TECH}/${SAMPLE}.strkit.vcf" \
  --seed "${SEED}" \
  --sample-id "${SAMPLE}" \
  --processes 1 \
  "${BAM}"
