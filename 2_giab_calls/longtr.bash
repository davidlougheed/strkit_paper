#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --account=rrg-bourqueg-ad

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.longtr.time" ../bin/LongTR \
  --bams "${bam_tmpdir}" \
  --bam-samps "${SAMPLE}" \
  --bam-libs "${SAMPLE}" \
  --fasta "${REF}" \
  --regions ./out/adotto_catalog_longtr.bed \
  --skip-assembly \
  --max-reads 250 \
  --min-reads 2 \
  --tr-vcf "./out/calls/${TECH}/${SAMPLE}.longtr.vcf.gz" \
  --haploid-chrs "${HAPLOID_CHRS}"
