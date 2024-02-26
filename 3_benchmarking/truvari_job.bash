#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1-00
#SBATCH --account=rrg-bourqueg-ad

module load python/3.9
source ../envs/env_truvari/bin/activate

REFERENCE="../1_cov_subsetting/data/hg38.analysisSet.fa"

# External environment variables:
#  - VCF
#  - TECH (hifi, ont)
#  - TOOL (strkit, longtr, trgt)

tech_dir="out/hg002_benchmark/${TECH}"
bench_dir="${tech_dir}/${TOOL}/"

mkdir -p "${tech_dir}"
rm -rf "${bench_dir}"

truvari bench \
  -b ./data/HG002_GRCh38_TandemRepeats_v1.0.vcf.gz \
  -c "${VCF}" \
  --includebed ./data/HG002_GRCh38_TandemRepeats_v1.0.bed.gz \
  --sizemin 5 \
  --pick ac \
  -o "${bench_dir}"

module load mafft  # required for refine

truvari refine \
  --use-original-vcfs \
  --reference "${REFERENCE}" \
  --regions "../2_giab_calls/out/adotto_catalog_${TOOL}.bed" \
  "${bench_dir}"
