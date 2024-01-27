#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=5-00
#SBATCH --account=rrg-bourqueg-ad

module load samtools

for bf in ./data/hifi/*; do
  echo "Working on $bf"
  samtools depth -a "$bf"  |  awk '{sum+=$3} END { print "Average = ",sum/NR}'
done

for bf in ./data/ont/*; do
  echo "Working on $bf"
  samtools depth -a "$bf"  |  awk '{sum+=$3} END { print "Average = ",sum/NR}'
done
