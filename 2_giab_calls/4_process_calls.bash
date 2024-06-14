#!/bin/bash
#SBATCH --mem=8G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --account=rrg-bourqueg-ad

module load samtools bcftools
cd out/calls || exit

for f in **/*.longtr.vcf; do
  bgzip -f $f
  tabix "${f}.gz"
done

for f in **/*.straglr.vcf; do
  bgzip -f $f
  tabix "${f}.gz"
done

for f in **/*.strkit.vcf; do
  bgzip -f $f
  tabix "${f}.gz"
done

for f in **/*.trgt.vcf.gz; do
  mv "${f}" "${f}_old"
  bcftools sort "${f}_old" -O z -o "${f}" || exit
  rm "${f}_old"
  tabix "${f}"
done

cd ../.. || exit
