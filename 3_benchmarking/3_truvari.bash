#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3-00
#SBATCH --account=rrg-bourqueg-ad

module load python/3.9
source env_truvari/bin/activate

REFERENCE="/lustre03/project/rrg-bourqueg-ad/dlough2/workdir2022/ref/hg38.analysisSet.fa"

# External environment variables:
#  - VCF
#  - TOOL  (strkit, longtr, trgt)

dir="out/hg002_benchmark/${TOOL}/"

mkdir -p "${dir}"

truvari bench \
  -b HG002_GRCh38_TandemRepeats_v1.0.vcf.gz \
  -c "${VCF}" \
  --includebed HG002_GRCh38_TandemRepeats_v1.0.chr4.bed.gz \
  --sizemin 5 \
  --pick ac \
  -o "${dir}"

module load mafft  # required for refine

truvari refine \
  --use-original-vcfs \
  --reference "${REFERENCE}" \
  --regions "out/adotto_catalog_${TOOL}.bed" \
  "${dir}"
