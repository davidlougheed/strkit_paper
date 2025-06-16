#!/usr/bin/env bash

# we have high-depth ONT simplex data from the ont-open-data resource;
# we want to subset for (rough) comparability with HiFi.

for bf in ./data/ont-simplex/HG00?.aligned.bam; do
  echo "Submitting subset job for ${bf}"
  # aligned ont-simplex HG002 is at ~48x, we need ~32x for comparability
  frac="0.6676492"
  if [ "${bf}" == "./data/ont-simplex/HG003.aligned.bam" ]; then
    # aligned ont-simplex HG003 @ ~38.7x --> ~31.6x
    frac="0.8181350"
  elif [ "${bf}" == "./data/ont-simplex/HG004.aligned.bam" ]; then
    # HG004 ont-simplex is already at 30.2452x
    frac="1"  # this will skip subsetting in the job and just link the file instead
  fi
  sbatch --export="BAM=${bf},FRAC=${frac}" ./subset_job.bash
done
