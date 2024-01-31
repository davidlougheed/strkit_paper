#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-18
#SBATCH --account=rrg-bourqueg-ad

module load samtools

for bf in ./data/hifi/*.aligned.bam; do
  echo "Working on $bf"
  samtools index "$bf"
  samtools depth -a "$bf" | awk '{sum+=$3} END { print "Average = ",sum/NR}'
done

for bf in ./data/ont/*.aligned.bam; do
  echo "Working on $bf"
  samtools index "$bf"
  samtools depth -a "$bf" | awk '{sum+=$3} END { print "Average = ",sum/NR}'
done
