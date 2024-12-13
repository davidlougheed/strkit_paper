#!/usr/bin/env bash

module load StdEnv/2023
module load python/3.11 rust/1.76.0 clang/17.0.6 scipy-stack/2023b parasail/2.6.2

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
pip install -vv -U strkit==0.19.0
deactivate
# END STRKIT

# BEGIN STRAGLR
#  - Straglr itself
if [[ ! -d "../envs/env_straglr" ]]; then
  python3 -m venv ../envs/env_straglr
fi
source ../envs/env_straglr/bin/activate || exit
pip install -v -U git+https://github.com/bcgsc/straglr.git@v1.5.3#egg=straglr
deactivate
#  - TRF
rm -rf ./TRF
git clone https://github.com/Benson-Genomics-Lab/TRF
cd TRF || exit
mkdir build
cd build || exit
../configure
make
cp src/trf ../../../bin
cd ../.. || exit
rm -rf ./TRF
# END STRAGLR

# BEGIN STRDUST
rm -rf ./STRdust
git clone https://github.com/wdecoster/STRdust.git
cd STRdust || exit
git checkout 3f3ebf0
sed -i 's/0.1.20/=0.1.20/g' Cargo.toml  # fix build issues with newer minimap2-rs
cargo add 'minimap2-sys@=0.1.19' # fix build issues with newer minimap2-sys
cargo build --release --verbose --jobs 12
cp ./target/release/STRdust ../../bin
cd .. || exit
rm -rf ./STRdust
# END STRDUST

# BEGIN LONGTR
module load googletest/1.14.0
rm -rf ./LongTR
git clone https://github.com/gymrek-lab/LongTR.git
cd LongTR || exit
git checkout v1.1
sed -i 's/-lspoa/-lspoa -ldeflate/g' Makefile  # need to edit Makefile to add -ldeflate
make
mv ./LongTR ../../bin
cd .. || exit
rm -rf ./LongTR
# END LONGTR

# BEGIN TRGT
trgt_version="v1.4.1"
trgt_rxiv="trgt-${trgt_version}-x86_64-unknown-linux-gnu.tar.gz"
wget "https://github.com/PacificBiosciences/trgt/releases/download/${trgt_version}/${trgt_rxiv}"
tar -xzvf "trgt-${trgt_version}-x86_64-unknown-linux-gnu.tar.gz"
trgt_dir="./trgt-${trgt_version}-x86_64-unknown-linux-gnu"
mv "${trgt_dir}/trgt" ../bin/trgt
rm -rf "${trgt_dir}" "${trgt_rxiv}"
chmod +x ../bin/trgt
# END TRGT
