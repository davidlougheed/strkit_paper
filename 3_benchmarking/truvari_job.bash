#!/bin/bash
#SBATCH --mem=32G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=4:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11
source ../envs/env_truvari/bin/activate

pip freeze

REFERENCE="../1_alignment/data/ref/hg38.analysisSet.fa"

# External environment variables:
#  - VCF
#  - TECH (hifi, ont)
#  - TOOL (strkit, longtr, trgt)

ls_bench_dir="${SLURM_TMPDIR}/bench/"

# set TMPDIR - try to address cursed Truvari 4.3.1 errors...
export TMPDIR="${SLURM_TMPDIR}/tmp"
mkdir -p "${TMPDIR}"

truvari bench \
  -b ./data/HG002_GRCh38_TandemRepeats_v1.0.1.no_homopolymers.vcf.gz \
  -c "${VCF}" \
  --includebed ./data/HG002_GRCh38_TandemRepeats_v1.0.bed.gz \
  --sizemin 5 \
  --pick ac \
  -o "${ls_bench_dir}" || exit

module load mafft  # required for refine

bed_tool="${TOOL}"
if [[ "${bed_tool}" == "strkit-no-snv" ]] || [[ "${bed_tool}" == "strdust" ]]; then
  bed_tool="strkit"
fi

truvari refine \
  --use-original-vcfs \
  --coords O \
  --reference "${REFERENCE}" \
  --regions "../2_giab_calls/out/adotto_catalog_${bed_tool}.bed" \
  --subset \
  --threads 8 \
  "${ls_bench_dir}" || exit

tech_dir="out/hg002_benchmark/${TECH}"
bench_dir="${tech_dir}/${TOOL}${PHASED:+_phased}"
mkdir -p "${tech_dir}"
rm -rf "${bench_dir}"  # remove bench_dir if it exists and overwrite it with the new contents
chown -R dlough2:rrg-bourqueg-ad "${ls_bench_dir}"
mv "${ls_bench_dir}" "${bench_dir}"
