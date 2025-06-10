#!/usr/bin/env bash

REF="./data/ref/hg38.analysisSet.fa"

for bf in ./data/hifi/HG00?.bam; do
  if [[ ! -f "${bf%.*}.aligned.bam" ]]; then
    echo "Submitting alignment job for ${bf}"
    sbatch --export="BAM=${bf},REF=${REF},TECH=hifi" ./align_job.bash
  fi
done

for bf in ./data/ont/HG00?.bam; do
  if [[ ! -f "${bf%.*}.aligned.bam" ]]; then
    echo "Submitting alignment job for ${bf}"
    sbatch --export="BAM=${bf},REF=${REF},TECH=ont" ./align_job.bash
  fi
done

for bf in ./data/ont-simplex/HG00?.bam; do
  if [[ ! -f "${bf%.*}.aligned.bam" ]]; then
    echo "Submitting alignment job for ${bf}"
    sbatch --export="BAM=${bf},REF=${REF},TECH=ont" ./align_job.bash
  fi
done
