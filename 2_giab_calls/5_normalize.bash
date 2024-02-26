#!/bin/bash
#SBATCH --mem=4G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --account=rrg-bourqueg-ad

REF='../1_cov_subsetting/data/ref/hg38.analysisSet.fa'

truvari_norm () {
  # Normalizes a .vcf.gz with base path $1 to have bi-allelic entries only (so multi-allelic VCF lines get split up),
  # which is a requirement for input into Truvari.
  bcftools norm -f "${REF}" -c s -m - "${1}.vcf.gz" -O z -o "${1}.norm.vcf.gz"
}

module load bcftools

for f in ./out/calls/**/*.strkit.vcf.gz; do
  base_path="${f%.*}"
  base_path="${base_path%.*}"
  echo "Working on ${f}; base_path=${base_path}"
  truvari_norm "${base_path}"
  echo "Done ${f}"
done

for f in ./out/calls/**/*.trgt.vcf.gz; do
  base_path="${f%.*}"
  base_path="${base_path%.*}"
  echo "Working on ${f}; base_path=${base_path}"
  truvari_norm "${base_path}"
  echo "Done ${f}"
done
