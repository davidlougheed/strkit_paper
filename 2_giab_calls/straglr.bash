#!/bin/bash
#SBATCH --mem=12G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=12:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 scipy-stack/2023b
source ../envs/env_straglr/bin/activate

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.straglr.time" straglr.py "${bam_tmpdir}" "${REF}" TODO --nprocs 8
