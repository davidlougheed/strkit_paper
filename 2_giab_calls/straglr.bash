#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=24:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 scipy-stack/2023b
source ../envs/env_straglr/bin/activate

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

export PATH="${PATH}:${PWD}/../bin"

# Straglr can use the same catalog format as STRkit

/usr/bin/time -o "./out/calls/${TECH}/${SAMPLE}.straglr.time" straglr.py \
  "${bam_tmpdir}" \
  "${REF}" \
  "./out/calls/${TECH}/${SAMPLE}.straglr" \
  --loci ./out/adotto_catalog_strkit.bed \
  --min_cluster_size 1 \
  --tmpdir "${SLURM_TMPDIR}" \
  --nprocs 8
