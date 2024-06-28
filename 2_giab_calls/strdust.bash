#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=3:00:00
#SBATCH --account=rrg-bourqueg-ad

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

# STRdust just expects regions in the BED file and ignores other columns

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.strdust.time" ../bin/STRdust \
  -R ./out/adotto_catalog_strkit.bed \
  -s 1 \
  -t 8 \
  --unphased \
  --haploid "${HAPLOID_CHRS}" > "./out/calls/${TECH}/${SAMPLE}.strdust.vcf"
