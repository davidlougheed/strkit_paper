#!/usr/bin/env bash

for bf in ./data/ont-simplex/HG00?.aligned.bam; do
  echo "Submitting subset job for ${bf}"
  frac="0.6676492"  #TODO: FRAC
  if "${bf}" == "./data/ont-simplex/HG003.aligned.bam"; then
    frac="TODO"  #TODO: FRAC
  elif "${bf}" == "./data/ont-simplex/HG004.aligned.bam"; then
    frac="TODO"  #TODO: FRAC
  fi
  sbatch --export="BAM=${bf},FRAC=${frac}" ./subset_job.bash
done
