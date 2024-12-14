#!/usr/bin/env bash

techs=( hifi ont )
tools=( longtr strdust strkit strkit-no-snv trgt )

laytr_job () {
  tech="${1}"
  tool="${2}"
  phased="${3}"

  d="./out/hg002_benchmark/${tech}/${tool}${phased:+_phased}"

  if [[ -d "${d}" ]]; then
    echo "Running laytr on ${d}"
    sbatch --export="BENCH_DIR=${d}" ./laytr_job.bash
  else
    echo "Skipping job; ${d} does not exist"
  fi
}

for tech in "${techs[@]}"; do
  for tool in "${tools[@]}"; do
    laytr_job "${tech}" "${tool}" ""
    laytr_job "${tech}" "${tool}" "1"
  done
done
