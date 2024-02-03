#!/usr/bin/env bash

module load python/3.11 rust/1.70.0

# BEGIN DATA

cd data || exit

if [[ ! -f "./adotto_TRregions_v1.2.bed" ]]; then
  gunzip -c ./adotto_TRregions_v1.2.bed.gz > ./adotto_TRregions_v1.2.bed
fi

if [[ ! -f "./00-common_all.vcf.gz" ]]; then
  wget https://ftp.ncbi.nih.gov/snp/organisms/human_9606/VCF/00-common_all.vcf.gz
  wget https://ftp.ncbi.nih.gov/snp/organisms/human_9606/VCF/00-common_all.vcf.gz.tbi
fi

cd .. || exit

# END DATA

# BEGIN STRKIT
if [[ ! -d "../envs/env_strkit" ]]; then
  python3 -m venv ../envs/env_strkit
fi
source ../envs/env_strkit/bin/activate || exit
pip install -U strkit[rustdeps]==0.15.0a1
deactivate
# END STRKIT

# BEGIN LONGTR
module load googletest/1.13.0
rm -rf ./LongTR
git clone https://github.com/gymrek-lab/LongTR.git
cd LongTR || exit
sed -i 's/-lspoa/-lspoa -ldeflate/g' Makefile  # need to edit Makefile to add -ldeflate
make
mv ./LongTR ../../bin
cd .. || exit
# END LONGTR

# BEGIN TRGT
wget https://github.com/PacificBiosciences/trgt/releases/download/v0.7.0/trgt-v0.7.0-linux_x86_64.gz
gunzip trgt-v0.7.0-linux_x86_64.gz
mv ./trgt-v0.7.0-linux_x86_64 ../bin/trgt
chmod +x ../bin/trgt
# END TRGT
