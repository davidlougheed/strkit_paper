#!/bin/bash
#SBATCH --mem=70G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --time=1-04
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

tmp_bam="${SLURM_TMPDIR}/out.bam"

../bin/minimap2 -t 12 -ax "map-${TECH}" "${REF}" "${fastq_gz}" | samtools sort --write-index -@ 12 - -o "${tmp_bam}"
mv "${tmp_bam}" "${BAM%.*}.aligned.bam"
