#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=0-12
#SBATCH --account=rrg-bourqueg-ad

module load samtools

echo "BAM=${BAM}"
echo "FRAC=${FRAC}"

subsam_bam="${BAM%.*}.subsam.bam"

if [ "${FRAC}" == "1" ]; then
  ln -s "${BAM}" "${subsam_bam}"
else
  samtools view -@ 2 -s "${FRAC}" -b -o "${subsam_bam}" "${BAM}"
fi

samtools index "${subsam_bam}"
