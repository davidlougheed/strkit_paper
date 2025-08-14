#!/bin/bash
#SBATCH --mem=90G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=36:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 scipy-stack/2025a
source ../envs/env_straglr/bin/activate

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

export PATH="${PATH}:${PWD}/../bin"

export PYTHONOPTIMIZE=1

# Straglr can use the same catalog format as STRkit

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.straglr.time" straglr.py \
  "${bam_tmpdir}" \
  "${REF}" \
  "${SLURM_TMPDIR}/${SAMPLE}.straglr" \
  --loci ./out/adotto_catalog_strkit.bed \
  --min_cluster_size 1 \
  --tmpdir "${SLURM_TMPDIR}" \
  --nprocs 8

chown dlough2:rrg-bourqueg-ad ${SLURM_TMPDIR}/${SAMPLE}.straglr.*
mv ${SLURM_TMPDIR}/${SAMPLE}.straglr.* ./out/calls/${TECH}/
