#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --time=3-00
#SBATCH --account=rrg-bourqueg-ad

../bin/trgt \
  -v \
  --reads "${BAM}" \
  --genome "${REF}" \
  --repeats ./out/adotto_catalog_trgt.bed \
  --output-prefix "./out/calls/${TECH}/${SAMPLE}.trgt" \
  --sample-name "${SAMPLE}" \
  --karyotype "${KARYOTYPE}" \
  --threads 10
