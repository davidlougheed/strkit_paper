#!/bin/bash
#SBATCH --mem=36G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=72:00:00
#SBATCH --account=rrg-bourqueg-ad

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

# STRdust just expects regions in the BED file and ignores other columns

if [[ "${PHASED}" == "1" ]]; then
  pf=""
else
  pf="--unphased"
fi

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.strdust.${PHASED:+phased.}time" ../bin/STRdust \
  -R ./out/adotto_catalog_strkit.bed \
  -s 1 \
  -t 8 \
  ${pf} \
  --haploid "${HAPLOID_CHRS}" \
  "${REF}" \
  "${bam_tmpdir}" > "./out/calls/${TECH}/${SAMPLE}.strdust.${PHASED:+phased.}vcf"
