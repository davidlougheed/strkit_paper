#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=1-00
#SBATCH --account=rrg-bourqueg-ad

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.trgt.time" ../bin/trgt -v genotype \
  --reads "${bam_tmpdir}" \
  --genome "${REF}" \
  --repeats ./out/adotto_catalog_trgt.bed \
  --output-prefix "./out/calls/${TECH}/${SAMPLE}.trgt" \
  --sample-name "${SAMPLE}" \
  --karyotype "${KARYOTYPE}" \
  --threads 8
