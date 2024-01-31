#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1-00
#SBATCH --account=rrg-bourqueg-ad

../bin/trgt \
  --reads "${BAM}" \
  --genome "${REF}" \
  --repeats ./out/adotto_catalog_trgt.bed \
  --output-prefix "./out/calls/${TECH}/${SAMPLE}.trgt" \
  --karyotype "${KARYOTYPE}"
