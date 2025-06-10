#!/usr/bin/env bash

module load samtools

# BEGIN DATA ===========================================================================================================

cd data || exit

# - Reference ----------------------------------------------------------------------------------------------------------

REF_DIR="ref"
REF_FILE="hg38.analysisSet.fa"

mkdir -p ref
cd "${REF_DIR}" || exit
if [[ ! -f "${REF_FILE}" ]]; then
  wget https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/analysisSet/hg38.analysisSet.fa.gz
  gunzip -c hg38.analysisSet.fa.gz > "${REF_FILE}"
  rm hg38.analysisSet.fa.gz
fi
if [[ ! -f "${REF_FILE}.fai" ]]; then
  samtools faidx "${REF_FILE}"
fi
cd .. || exit

# - Reads --------------------------------------------------------------------------------------------------------------

mkdir -p hifi
mkdir -p ont-simplex
mkdir -p ont

cd hifi || exit # ------------------------------------------------------------------------------------------------------

hifi_unaligned () {
  # unaligned, unphased reads
  if [[ ! -f "HG002.bam" ]]; then
    wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG002-rep1/m84011_220902_175841_s1.hifi_reads.bam -O HG002.bam
  fi
  if [[ ! -f "HG003.bam" ]]; then
    wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG003-rep1/m84010_220919_235306_s2.hifi_reads.bam -O HG003.bam
  fi
  if [[ ! -f "HG004.bam" ]]; then
    wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG004-rep1/m84010_220919_232145_s1.hifi_reads.bam -O HG004.bam
  fi
}

hifi_unaligned

hifi_aligned_hp () {
  # aligned, phased reads (HP tags)
  if [[ ! -f "HG002.phased.aligned.bam" ]]; then
    wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG002-rep1/analysis/HG002.m84011_220902_175841_s1.GRCh38.bam -O "HG002.phased.aligned.bam"
    samtools index "HG002.phased.aligned.bam"
  fi
  if [[ ! -f "HG003.phased.aligned.bam" ]]; then
    wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG003-rep1/analysis/HG003.m84010_220919_235306_s2.GRCh38.bam -O "HG003.phased.aligned.bam"
    samtools index "HG003.phased.aligned.bam"
  fi
  if [[ ! -f "HG004.phased.aligned.bam" ]]; then
    wget https://downloads.pacbcloud.com/public/revio/2022Q4/HG004-rep1/analysis/HG004.m84010_220919_232145_s1.GRCh38.bam -O "HG004.phased.aligned.bam"
    samtools index "HG004.phased.aligned.bam"
  fi
}

hifi_aligned_hp

cd ../ont-simplex || exit # --------------------------------------------------------------------------------------------

ont_simplex_base_url="https://42basepairs.com/download/s3/ont-open-data/giab_2025.01/basecalling/sup"

if [[ ! -f "HG002.simplex.bam" ]]; then
  wget "${ont_simplex_base_url}/HG002/PAW70337/calls.sorted.bam" -O HG002.bam
fi
if [[ ! -f "HG003.simplex.bam" ]]; then
  wget "${ont_simplex_base_url}/HG003/PAY87794/calls.sorted.bam" -O HG003.bam
fi
if [[ ! -f "HG004.simplex.bam" ]]; then
  wget "${ont_simplex_base_url}/HG004/PAY87778/calls.sorted.bam" -O HG004.bam
fi

cd ../ont || exit # ----------------------------------------------------------------------------------------------------

ont_duplex_base_url="https://human-pangenomics.s3.amazonaws.com/submissions/0CB931D5-AE0C-4187-8BD8-B3A9C9BFDADE--UCSC_HG002_R1041_Duplex_Dorado/Dorado_v0.1.1/stereo_duplex"

if [[ ! -f "HG002-1.bam" ]]; then
  wget "${ont_duplex_base_url}/1_3_23_R1041_Duplex_HG002_1_Dorado_v0.1.1_400bps_sup_stereo_duplex.bam" -O HG002-1.bam
fi
if [[ ! -f "HG002-2.bam" ]]; then
  wget "${ont_duplex_base_url}/1_3_23_R1041_Duplex_HG002_2_Dorado_v0.1.1_400bps_sup_stereo_duplex.bam" -O HG002-2.bam
fi
if [[ ! -f "HG002-3.bam" ]]; then
  wget "${ont_duplex_base_url}/1_3_23_R1041_Duplex_HG002_3_Dorado_v0.1.1_400bps_sup_stereo_duplex.bam" -O HG002-3.bam
fi

cd ../.. || exit # -----------------------------------------------------------------------------------------------------

# END DATA =============================================================================================================

# BEGIN MINIMAP2 =======================================================================================================

rm -rf ./minimap2
git clone https://github.com/lh3/minimap2.git
cd minimap2 || exit
git checkout v2.28
make
mv ./minimap2 ../../bin/
cd .. || exit
rm -rf ./minimap2  # make sure we clean up at the end (with a backup at the start)

# END MINIMAP2 =========================================================================================================
