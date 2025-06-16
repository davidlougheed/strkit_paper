#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=0-12
#SBATCH --account=rrg-bourqueg-ad

module load samtools

echo "BAM=${BAM}"
echo "FRAC=${FRAC}"

if "${FRAC}" == "1"; then
  ln -s "${BAM}" "${BAM%.*}.subsam.bam"
else
  samtools view -@ 2 -s "${FRAC}" -b -o "${BAM%.*}.subsam.bam" "${BAM}"
fi
