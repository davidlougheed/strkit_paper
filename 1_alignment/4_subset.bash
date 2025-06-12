#!/usr/bin/env bash

for bf in ./data/ont-simplex/HG00?.aligned.bam; do
  echo "Submitting subset job for ${bf}"
  frac="TODO"  #TODO: FRAC
  if "${bf}" == "./data/ont-simplex/HG004.aligned.bam"; then
    frac="TODO"  #TODO: FRAC
  fi
  sbatch --export="BAM=${bf},FRAC=${frac}" ./subset_job.bash
done
