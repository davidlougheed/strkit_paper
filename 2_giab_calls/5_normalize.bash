#!/bin/bash
#SBATCH --mem=4G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --account=rrg-bourqueg-ad

REF='../1_cov_subsetting/data/ref/hg38.analysisSet.fa'

truvari_norm () {
  # Normalizes a .vcf.gz with path $1 to have bi-allelic entries only (so multi-allelic VCF lines get split up),
  # which is a requirement for input into Truvari.

  base_path="${1%.*}"
  base_path="${base_path%.*}"

  echo "Working on ${1}; base_path=${base_path}"

  bcftools norm -f "${REF}" -c s -m - "${base_path}.vcf.gz" -O z -o "${base_path}.norm.vcf.gz"
  tabix "${base_path}.norm.vcf.gz"

  echo "Done ${1}"
}

module load bcftools

for f in ./out/calls/**/*.longtr.vcf.gz; do
  truvari_norm "${f}"
done

for f in ./out/calls/**/*.straglr.vcf.gz; do
  truvari_norm "${f}"
done

for f in ./out/calls/**/*.strkit.vcf.gz; do
  truvari_norm "${f}"
done

for f in ./out/calls/**/*.trgt.vcf.gz; do
  truvari_norm "${f}"
done
