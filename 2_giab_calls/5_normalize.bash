#!/bin/bash
#SBATCH --mem=4G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=30:00
#SBATCH --account=rrg-bourqueg-ad

REF='../1_alignment/data/ref/hg38.analysisSet.fa'

truvari_norm () {
  # Normalizes a .vcf.gz with path $1 to have bi-allelic entries only (so multi-allelic VCF lines get split up),
  # which is a requirement for input into Truvari.

  base_path="${1%.*}"
  base_path="${base_path%.*}"

  echo "Working on ${1}; base_path=${base_path}"

  bcftools norm --force -f "${REF}" -c s -m - "${base_path}.vcf.gz" | bcftools sort -O z -o "${base_path}.norm.vcf.gz"
  tabix -f "${base_path}.norm.vcf.gz"

  echo "Done ${1}"
}

module load bcftools

tools=( longtr strdust strkit strkit-no-snv trgt )

for tool in "${tools[@]}"; do
  for f in ./out/calls/**/*.${tool}.vcf.gz; do
    if [[ -f "${f}" ]]; then
      truvari_norm "${f}"
    else
      echo "File does not exist: ${f}"
    fi
  done
  for f in ./out/calls/**/*.${tool}.phased.vcf.gz; do
    if [[ -f "${f}" ]]; then
      truvari_norm "${f}"
    else
      echo "File does not exist: ${f}"
    fi
  done
done
