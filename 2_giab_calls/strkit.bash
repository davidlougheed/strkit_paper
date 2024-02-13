#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=3-00
#SBATCH --account=rrg-bourqueg-ad

module load python/3.11 parasail
source ../envs/env_strkit/bin/activate

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

snv_vcf_tmpdir="${SLURM_TMPDIR}/snvs.vcf.gz"
cp "./data/00-common_all.vcf.gz" "${snv_vcf_tmpdir}"
cp "./data/00-common_all.vcf.gz.tbi" "${snv_vcf_tmpdir}.tbi"

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.strkit.time" strkit call \
  --ref "${REF}" \
  --loci ./out/adotto_catalog_strkit.bed \
  --sex-chr "${KARYOTYPE}" \
  --hq \
  --incorporate-snvs "${snv_vcf_tmpdir}" \
  --vcf "./out/calls/${TECH}/${SAMPLE}.strkit.vcf" \
  --no-tsv \
  --seed "${SEED}" \
  --sample-id "${SAMPLE}" \
  --processes 8 \
  --log-level debug \
  "${bam_tmpdir}"
