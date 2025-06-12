#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --time=0-12
#SBATCH --account=rrg-bourqueg-ad

module load samtools

echo "BAM=${BAM}"
echo "FRAC=${FRAC}"

samtools view -s "${FRAC}" -b -o "${BAM%.*}.subsam.bam" "${BAM}"
