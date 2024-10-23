#!/usr/bin/env bash
#SBATCH --mem=4G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 rust/1.76.0 clang/17.0.6 scipy-stack/2023b parasail/2.6.2

source ../envs/env_strkit/bin/activate

hifi_base="../2_giab_calls/out/calls/hifi"
out_base="out/hg002_benchmark/hifi"

tools=( longtr strkit strkit-no-snv trgt )

longtr_out="${out_base}/longtr/mi_report.json"
strkit_out="${out_base}/strkit/mi_report.json"
trgt_out="${out_base}/trgt/mi_report.json"

for tool in "${tools[@]}"; do
  out="${out_base}/${tool}/mi_report.json"
  if [[ ! -f "${out}" ]]; then
    mi_caller="${tool}"
    if [[ "${mi_caller}" == "strkit" || "${mi_caller}" == "strkit-no-snv" ]]; then
      mi_caller="strkit-vcf"
    fi
    strkit mi --caller "${mi_caller}" \
      "${hifi_base}/HG002.${tool}.vcf.gz" \
      "${hifi_base}/HG004.${tool}.vcf.gz" \
      "${hifi_base}/HG003.${tool}.vcf.gz" \
      --hist \
      --trf-bed "../2_giab_calls/out/adotto_catalog_strkit.bed" \
      --json "${out}"
  fi
done

deactivate
