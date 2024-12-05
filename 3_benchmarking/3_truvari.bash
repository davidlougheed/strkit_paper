#!/usr/bin/env bash

techs=( hifi ont )
# Re-enable if not failed
#tools=( longtr straglr strdust strkit trgt )
tools=( longtr strkit strkit-no-snv trgt )

truvari_job () {
  tech="${1}"
  tool="${2}"
  phased="${3}"

  f="../2_giab_calls/out/calls/${tech}/HG002.${tool}.${phased:+phased.}norm.vcf.gz"

  if [[ -f "${f}" ]]; then
    echo "Running truvari on ${f}"
    sbatch --export="VCF=${f},TECH=${tech},TOOL=${tool},PHASED=${phased}" ./truvari_job.bash
  else
    echo "Skipping job; ${f} does not exist"
  fi
}

for tech in "${techs[@]}"; do
  for tool in "${tools[@]}"; do
    truvari_job "${tech}" "${tool}" ''
    truvari_job "${tech}" "${tool}" '1'
  done
done
