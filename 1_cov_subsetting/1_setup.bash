#!/usr/bin/env bash

# BEGIN DATA

cd data || exit

mkdir -p ref
cd ref || exit
wget https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/analysisSet/hg38.analysisSet.fa.gz
cd .. || exit

mkdir -p hifi
mkdir -p ont

cd hifi || exit

wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG002-rep1/m84011_220902_175841_s1.hifi_reads.bam -O HG002.bam
wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG003-rep1/m84010_220919_235306_s2.hifi_reads.bam -O HG003.bam
wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG004-rep1/m84010_220919_232145_s1.hifi_reads.bam -O HG004.bam

cd ../ont || exit

wget https://human-pangenomics.s3.amazonaws.com/submissions/0CB931D5-AE0C-4187-8BD8-B3A9C9BFDADE--UCSC_HG002_R1041_Duplex_Dorado/Dorado_v0.1.1/stereo_duplex/1_3_23_R1041_Duplex_HG002_1_Dorado_v0.1.1_400bps_sup_stereo_duplex.bam -O HG002-1.bam
wget https://human-pangenomics.s3.amazonaws.com/submissions/0CB931D5-AE0C-4187-8BD8-B3A9C9BFDADE--UCSC_HG002_R1041_Duplex_Dorado/Dorado_v0.1.1/stereo_duplex/1_3_23_R1041_Duplex_HG002_2_Dorado_v0.1.1_400bps_sup_stereo_duplex.bam -O HG002-2.bam
wget https://human-pangenomics.s3.amazonaws.com/submissions/0CB931D5-AE0C-4187-8BD8-B3A9C9BFDADE--UCSC_HG002_R1041_Duplex_Dorado/Dorado_v0.1.1/stereo_duplex/1_3_23_R1041_Duplex_HG002_3_Dorado_v0.1.1_400bps_sup_stereo_duplex.bam -O HG002-3.bam

cd ../.. || exit

# END DATA

# BEGIN MINIMAP2

rm -rf ./minimap2
git clone https://github.com/lh3/minimap2.git
cd minimap2 || exit
git checkout v2.26
make
mv ./minimap2 ../bin/

# END MINIMAP2
