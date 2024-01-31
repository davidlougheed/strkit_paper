#!/usr/bin/env bash

REF="./data/ref/hg38.analysisSet.fa"

for bf in ./data/hifi/*; do
  sbatch --export="BAM=${bf},REF=${REF},TECH=hifi" ./align_job.bash
done

for bf in ./data/ont/*; do
  sbatch --export="BAM=${bf},REF=${REF},TECH=ont" ./align_job.bash
done
