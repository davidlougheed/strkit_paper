#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --time=3-00
#SBATCH --account=rrg-bourqueg-ad

module load python/3.11 parasail
source ../envs/env_strkit/bin/activate

#  --realign \
/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.strkit.time" strkit call \
  --ref "${REF}" \
  --loci ./out/adotto_catalog_strkit.bed \
  --sex-chr "${KARYOTYPE}" \
  --hq \
  --incorporate-snvs "./data/00-common_all.vcf.gz" \
  --vcf "./out/calls/${TECH}/${SAMPLE}.strkit.vcf" \
  --no-tsv \
  --seed "${SEED}" \
  --sample-id "${SAMPLE}" \
  --processes 10 \
  "${BAM}"
