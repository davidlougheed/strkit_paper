#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --account=rrg-bourqueg-ad

module load samtools bcftools
cd out/calls || exit

vcf_process () {
  bgzip -f "${1}"
  tabix -f "${1}.gz"
}

# LongTR ------------------------------------------------------------

for f in **/*.longtr.vcf.gz; do
  tabix -f "${f}"
done
for f in **/*.longtr.phased.vcf.gz; do
  tabix -f "${f}"
done

# Straglr -----------------------------------------------------------

for f in **/*.straglr.vcf; do
  vcf_process "${f}"
done

# STRdust -----------------------------------------------------------

# Re-enable if not failed
#for f in **/*.strdust.vcf; do
#  bgzip -f $f
#  tabix "${f}.gz"
#done

# STRkit ------------------------------------------------------------

for f in **/*.strkit.vcf; do
  vcf_process "${f}"
done

for f in **/*.strkit.phased.vcf; do
  vcf_process "${f}"
done

for f in **/*.strkit-no-snv.vcf; do
  vcf_process "${f}"
done

# TRGT --------------------------------------------------------------

trgt_process () {
  mv "${1}" "${1}_old"
  bcftools sort "${1}_old" -O z -o "${1}" || exit
  rm "${1}_old"
  tabix -f "${1}"
}

for f in **/*.trgt.vcf.gz; do
  trgt_process "${f}"
done

for f in **/*.trgt.phased.vcf.gz; do
  trgt_process "${f}"
done

# -------------------------------------------------------------------

cd ../.. || exit
