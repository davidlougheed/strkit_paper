#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=3:00:00
#SBATCH --account=rrg-bourqueg-ad

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

# don't need to check $PHASED - TRGT automatically picks up HP tags

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.trgt.${PHASED:+phased.}time" ../bin/trgt -v genotype \
  --reads "${bam_tmpdir}" \
  --genome "${REF}" \
  --repeats ./out/adotto_catalog_trgt.bed \
  --output-prefix "./out/calls/${TECH}/${SAMPLE}.trgt${PHASED:+.phased}" \
  --disable-bam-output \
  --sample-name "${SAMPLE}" \
  --karyotype "${KARYOTYPE}" \
  --threads 8
