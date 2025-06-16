#!/bin/bash
#SBATCH --mem=12G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=12:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 scipy-stack/2025a parasail/2.6.2
source ../envs/env_strkit/bin/activate

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

snv_vcf_tmpdir="${SLURM_TMPDIR}/snvs.vcf.gz"
cp "./data/00-common_all.vcf.gz" "${snv_vcf_tmpdir}"
cp "./data/00-common_all.vcf.gz.tbi" "${snv_vcf_tmpdir}.tbi"

export PYTHONOPTIMIZE=1

if [[ "${PHASED}" == "1" ]]; then
  pf="--use-hp"
else
  pf="--incorporate-snvs ${snv_vcf_tmpdir}"
fi

# for comparison to TRGT, which has no minimum, we set --min-reads and --min-allele-reads low
/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.strkit.${PHASED:+phased.}time" strkit call \
  --ref "${REF}" \
  --loci ./out/adotto_catalog_strkit.bed \
  --sex-chr "${KARYOTYPE}" \
  --hq \
  ${pf} \
  --min-reads 2 \
  --min-allele-reads 1 \
  --min-read-align-score 0.0 \
  --max-rcn-iters 100 \
  --vcf "./out/calls/${TECH}/${SAMPLE}.strkit.${PHASED:+phased.}vcf" \
  --no-tsv \
  --seed "${SEED}" \
  --sample-id "${SAMPLE}" \
  --processes 8 \
  "${bam_tmpdir}"
