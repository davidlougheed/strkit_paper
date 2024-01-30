#!/usr/bin/env bash

module load samtools

# BEGIN DATA

cd data || exit

if [[ ! -f "./hs37d5.fa" ]]; then
  wget http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz
  gunzip -c hs37d5.fa.gz > hs37d5.fa
  samtools faidx hs37d5.fa
fi

wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1015--bc1015.bam
wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1015--bc1015.bam.bai

wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1016--bc1016.bam
wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1016--bc1016.bam.bai

wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1017--bc1017.bam
wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1017--bc1017.bam.bai

wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1018--bc1018.bam
wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1018--bc1018.bam.bai

wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1019--bc1019.bam
wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1019--bc1019.bam.bai

wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1020--bc1020.bam
wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1020--bc1020.bam.bai

wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1021--bc1021.bam
wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1021--bc1021.bam.bai

wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1022--bc1022.bam
wget https://downloads.pacbcloud.com/public/dataset/RepeatExpansionDisorders_NoAmp/analysis/align/m64012_191221_044659.ccsset.bc1022--bc1022.bam.bai

cd .. || exit

# END DATA
