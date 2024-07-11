#!/usr/bin/env bash
#SBATCH --mem=12G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=10:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 rust/1.76.0 clang/17.0.6 scipy-stack/2023b parasail/2.6.2

source ../envs/env_strkit/bin/activate

hifi_base="../2_giab_calls/out/calls/hifi"

strkit mi --caller strkit-vcf \
  "${hifi_base}/HG002.strkit.vcf.gz" \
  "${hifi_base}/HG004.strkit.vcf.gz" \
  "${hifi_base}/HG003.strkit.vcf.gz" \
  --hist \
  --json out/hg002_benchmark/hifi/strkit/mi_report.json

# TODO: strkit mi for other tools

deactivate
