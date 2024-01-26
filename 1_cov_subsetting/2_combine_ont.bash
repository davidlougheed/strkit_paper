#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-6
#SBATCH --account=rrg-bourqueg-ad

module load samtools
cd data/ont || exit
samtools merge -o "${SLURM_TMPDIR}/HG002.bam" HG002-1.bam HG002-2.bam HG002-3.bam
mv "${SLURM_TMPDIR}/HG002.bam" ./
