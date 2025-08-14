#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --time=24:00:00
#SBATCH --account=rrg-bourqueg-ad

module load bcftools

REF='../1_alignment/data/ref/hg38.analysisSet.fa'
HIFI_BAM='../1_alignment/data/hifi/HG002.phased.aligned.bam'
ONT_SIMPLEX_BAM='../1_alignment/data/ont-simplex/HG002.aligned.subsam.bam'
ONT_DUPLEX_BAM='../1_alignment/data/ont/HG002.aligned.bam'

bcftools mpileup -Ou -f "${REF}" --threads 2 "${HIFI_BAM}" | \
  bcftools call --threads 2 --skip-variants indels -mv -Ob -o out/HG002_snv_calls.hifi.bcf &

bcftools mpileup -Ou -f "${REF}" --threads 2 "${ONT_SIMPLEX_BAM}" | \
  bcftools call --threads 2 --skip-variants indels -mv -Ob -o out/HG002_snv_calls.ont-simplex.bcf &

bcftools mpileup -Ou -f "${REF}" --threads 2 "${ONT_DUPLEX_BAM}" | \
  bcftools call --threads 2 --skip-variants indels -mv -Ob -o out/HG002_snv_calls.ont.bcf &

wait
