#!/usr/bin/env bash

module load samtools

# BEGIN DATA

cd data || exit

if [[ ! -f "./hs37d5.fa" ]]; then
  wget http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz
  gunzip -c hs37d5.fa.gz > hs37d5.fa
  samtools faidx hs37d5.fa
fi

samples=( bc1015 bc1016 bc1017 bc1018 bc1019 bc1020 bc1021 bc1022 )

for sample in "${samples[@]}"; do
  f="m64012_191221_044659.ccsset.${sample}--${sample}.bam"
  if [[ ! -f "${f}" ]]; then
    wget "https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/${f}"
    wget "https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/${f}.bai"
  else
    echo "already have ${f}"
  fi
done

cd .. || exit

# END DATA
