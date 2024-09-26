#!/usr/bin/env bash

techs=( hifi ont )
# Re-enable if not failed
#tools=( longtr straglr strdust strkit trgt )
tools=( longtr strkit trgt )

for tech in "${techs[@]}"; do
  for tool in "${tools[@]}"; do
    f="../2_giab_calls/out/calls/${tech}/HG002.${tool}.norm.vcf.gz"
    if [[ -f "${f}" ]]; then
      echo "Running truvari on ${f}"
      sbatch --export="VCF=${f},TECH=${tech},TOOL=${tool}" ./truvari_job.bash
    else
      echo "Skipping job; ${f} does not exist"
    fi
  done
done
