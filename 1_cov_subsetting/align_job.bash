#!/bin/bash
#SBATCH --mem=64G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=1-00
#SBATCH --account=rrg-bourqueg-ad

module load samtools
../bin/minimap2 -t 8 -ax "map-${TECH}" "${REF}" "${BAM}" | samtools sort -@ 8 - -o "${BAM%.*}.aligned.bam"
