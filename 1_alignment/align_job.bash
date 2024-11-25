#!/bin/bash
#SBATCH --mem=70G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --time=0-12
#SBATCH --account=rrg-bourqueg-ad

module load samtools

echo "BAM=${BAM}"
echo "REF=${REF}"
echo "TECH=${TECH}"
fastq_gz="${BAM%.*}.fastq.gz"
echo "fastq_gz=${fastq_gz}"

if [[ ! -f "${fastq_gz}" ]]; then
  tmp="${SLURM_TMPDIR}/fastq.gz"
  samtools fastq -@ 10 "${BAM}" | pigz -p 10 -3 > "${tmp}"
  mv "${tmp}" "${fastq_gz}"
fi

tmp_bam="${SLURM_TMPDIR}/out.bam"
aligned_bam="${BAM%.*}.aligned.bam"

preset="map-hifi"
if [[ "${tech}" == "ont" ]]; then
  preset="lr:hq"  # new preset for more-accurate latest gen ONT data
fi

../bin/minimap2 -t 10 -ax "${preset}" "${REF}" "${fastq_gz}" | samtools sort --write-index -@ 10 - -o "${tmp_bam}"
mv "${tmp_bam}" "${aligned_bam}"
chgrp rrg-bourqueg-ad "${aligned_bam}"
