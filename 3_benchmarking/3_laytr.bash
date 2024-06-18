#!/usr/bin/env bash

techs=( hifi ont )
tools=( longtr strkit trgt )

for tech in "${techs[@]}"; do
  for tool in "${tools[@]}"; do
    d="./out/hg002_benchmark/${tech}/${tool}"
    if [[ -d "${d}" ]]; then
      echo "Running laytr on ${d}"
      sbatch --export="BENCH_DIR=${d}" ./laytr_job.bash
    else
      echo "Skipping job; ${d} does not exist"
    fi
  done
done
