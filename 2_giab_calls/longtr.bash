#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3-00
#SBATCH --account=rrg-bourqueg-ad

module load python/3.9

../bin/LongTR \
  --bams "${BAM}" \
  --bam-samps "${SAMPLE}" \
  --bam-libs "${SAMPLE}" \
  --fasta "${REF}" \
  --regions ./out/adotto_catalog_longtr.bed \
  --skip-assembly \
  --tr-vcf "./out/calls/${TECH}/${SAMPLE}.longtr.vcf.gz" \
  --haploid-chrs "${HAPLOID_CHRS}"
