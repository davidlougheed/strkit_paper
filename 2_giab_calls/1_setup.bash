#!/usr/bin/env bash

module load python/3.9 rust/1.70.0

# BEGIN DATA
if [[ ! -f "./data/adotto_TRregions_v1.2.bed" ]]; then
  gunzip -c ./data/adotto_TRregions_v1.2.bed.gz > ./data/adotto_TRregions_v1.2.bed
fi
# END DATA

# BEGIN STRKIT
python3 -m venv ../envs/env_strkit
source ../envs/env_strkit/bin/activate || exit
pip install -U strkit[rustdeps]
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
