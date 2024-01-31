#!/bin/bash
#SBATCH --mem=64G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=1-00
#SBATCH --account=rrg-bourqueg-ad

module load bedtools samtools

echo "BAM=${BAM}"
echo "REF=${REF}"
echo "TECH=${TECH}"
fastq="${BAM%.*}.fq"
fastq_gz = "${fastq}.gz"
echo "fastq=${fastq}"

if [[ ! -f "${fastq_gz}" ]]; then
  bedtools bamtofastq -i "${BAM}" -fq "${fastq}"
  gzip "${fastq}"
fi

../bin/minimap2 -t 8 -ax "map-${TECH}" "${REF}" "${fastq_gz}" | samtools sort --write-index -@ 8 - -o "${BAM%.*}.aligned.bam"
