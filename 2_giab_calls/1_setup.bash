#!/usr/bin/env bash

module load StdEnv/2023
module load python/3.11 rust/1.76.0 clang/17.0.6 scipy-stack/2023b

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
pip install -v -U strkit==0.15.0a11
pip install wheel
pip install 'parasail>=1.3.4'
deactivate
# END STRKIT

# BEGIN LONGTR
module load googletest/1.14.0
rm -rf ./LongTR
git clone https://github.com/gymrek-lab/LongTR.git
cd LongTR || exit
git checkout v1.0
sed -i 's/-lspoa/-lspoa -ldeflate/g' Makefile  # need to edit Makefile to add -ldeflate
make
mv ./LongTR ../../bin
cd .. || exit
# END LONGTR

# BEGIN TRGT
trgt_version="v1.0.0"
wget "https://github.com/PacificBiosciences/trgt/releases/download/${trgt_version}/trgt-${trgt_version}-x86_64-unknown-linux-gnu.tar.gz"
tar -xzvf "trgt-${trgt_version}-x86_64-unknown-linux-gnu.tar.gz"
trgt_dir="./trgt-${trgt_version}-x86_64-unknown-linux-gnu"
mv "${trgt_dir}/trgt" ../bin/trgt
rm -rf "${trgt_dir}"
chmod +x ../bin/trgt
# END TRGT
