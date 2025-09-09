#!/usr/bin/env bash

module load samtools

REF_URL="https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz"
REF_FILE="GRCh38_no_alt_analysis_set.fna"
REF_FILE_GZ="GRCh38_no_alt_analysis_set.fna.gz"

# Download reference genome
mkdir -p data/ref
cd ./data/ref || exit
if [[ ! -f "${REF_FILE}" ]]; then
  wget "${REF_URL}" -O "${REF_FILE_GZ}"
  gunzip -c "${REF_FILE_GZ}" > "${REF_FILE}"
  rm "${REF_FILE_GZ}"
  samtools faidx "${REF_FILE}"
fi
cd ../.. || exit

# Copy catalogs from step 2 for use inside jobs
cp ../2_giab_calls/out/adotto_catalog_* ./out/

# Set up out directory
mkdir -p out/calls/hifi
