#!/usr/bin/env bash

techs=( hifi ont )
tools=( longtr strkit trgt )

for tech in "${techs[@]}"; do
  for tool in "${tools[@]}"; do
    for f in ../2_giab_calls/out/calls/${tech}/HG002.${tool}.norm.vcf; do
      sbatch --export="VCF=${f},TECH=${tech},TOOL=${tool}" ./truvari_job.bash
    done
  done
done
