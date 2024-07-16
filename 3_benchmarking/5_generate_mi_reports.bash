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
out_base="out/hg002_benchmark/hifi"

strkit_out="${out_base}/strkit/mi_report.json"
trgt_out="${out_base}/strkit/mi_report.json"

if [[ ! -f "${strkit_out}" ]]; then
  strkit mi --caller strkit-vcf \
    "${hifi_base}/HG002.strkit.vcf.gz" \
    "${hifi_base}/HG004.strkit.vcf.gz" \
    "${hifi_base}/HG003.strkit.vcf.gz" \
    --hist \
    --json "${strkit_out}"
fi

if [[ ! -f "${trgt_out}" ]]; then
  strkit mi --caller trgt \
    "${hifi_base}/HG002.trgt.vcf.gz" \
    "${hifi_base}/HG004.trgt.vcf.gz" \
    "${hifi_base}/HG003.trgt.vcf.gz" \
    --hist \
    --json "${trgt_out}"
fi

# TODO: strkit mi for other tools

deactivate
