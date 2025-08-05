#!/bin/bash
#SBATCH --mem=16G
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

export PYTHONOPTIMIZE=1

# for comparison to TRGT, which has no minimum, we set --min-reads and --min-allele-reads low
/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.strkit-no-snv.time" strkit call \
  --ref "${REF}" \
  --loci ./out/adotto_catalog_strkit.bed \
  --sex-chr "${KARYOTYPE}" \
  --hq \
  --min-reads 2 \
  --min-allele-reads 1 \
  --min-read-align-score 0.2 \
  --vcf "./out/calls/${TECH}/${SAMPLE}.strkit-no-snv.vcf" \
  --no-tsv \
  --seed "${SEED}" \
  --sample-id "${SAMPLE}" \
  --processes 8 \
  "${bam_tmpdir}"
