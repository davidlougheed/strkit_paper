#!/usr/bin/env bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 rust/1.85.0 clang/17.0.6 scipy-stack/2025a parasail/2.6.2

source ../envs/env_strkit/bin/activate

# we have trio data for hifi and ont-simplex technologies
techs=( hifi ont-simplex )

calls_base="../2_giab_calls/out/calls"
out_base="out/hg002_benchmark"

tools=( longtr strdust strkit strkit-no-snv straglr trgt )

run_mi () {
  tech="${1}"
  tool="${2}"
  phased="${3}"

  # ------------------------------------------------------------------------------------------

  tool_dir="${out_base}/${tech}/${tool}${phased:+_phased}"

  mkdir -p "${tool_dir}"
  out="${tool_dir}/mi_report.json"

  if [[ ! -f "${out}" ]]; then
    mi_caller="${tool}"
    if [[ "${mi_caller}" == "strkit" || "${mi_caller}" == "strkit-no-snv" ]]; then
      mi_caller="strkit-vcf"
    fi

    ext="vcf.gz"
    if [[ "${mi_caller}" == "straglr" ]]; then
      ext="bed"
    fi

    echo "Working on ${out}"

    tool_opt_phased="${tool}${phased:+.phased}"

    strkit mi --caller "${mi_caller}" \
      "${calls_base}/${tech}/HG002.${tool_opt_phased}.${ext}" \
      "${calls_base}/${tech}/HG004.${tool_opt_phased}.${ext}" \
      "${calls_base}/${tech}/HG003.${tool_opt_phased}.${ext}" \
      --hist \
      --motif-bed "../2_giab_calls/out/adotto_catalog_strkit.bed" \
      --json "${out}"
  fi
}

for tech in "${techs[@]}"; do
  for tool in "${tools[@]}"; do
    run_mi "${tech}" "${tool}" ''

    if [[ "${tech}" == "hifi" ]]; then
      if [[ "${tool}" == "longtr" ]] || [[ "${tool}" == "strkit" ]] || [[ "${tool}" == "trgt" ]]; then
        run_mi "${tech}" "${tool}" '1'
      fi
    fi
  done
done

deactivate
