#!/usr/bin/env bash

REF="./data/ref/hg38.analysisSet.fa"

for bf in ./data/hifi/HG00?.bam; do
  echo "Submitting alignment job for ${bf}"
  sbatch --export="BAM=${bf},REF=${REF},TECH=hifi" ./align_job.bash
done

for bf in ./data/ont/HG00?.bam; do
  echo "Submitting alignment job for ${bf}"
  sbatch --export="BAM=${bf},REF=${REF},TECH=ont" ./align_job.bash
done
