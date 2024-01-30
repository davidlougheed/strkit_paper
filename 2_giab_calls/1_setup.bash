#!/usr/bin/env bash

module load python/3.9

# BEGIN DATA
gunzip -c ./data/adotto_TRregions_v1.2.bed.gz > ./data/adotto_TRregions_v1.2.bed
# END DATA

# BEGIN STRKIT
python3 -m venv ../envs/env_strkit
source ../envs/env_strkit/bin/activate
pip install -U strkit[rustdeps]
deactivate
# END STRKIT

# BEGIN LONGTR
rm -rf ./LongTR
git clone https://github.com/gymrek-lab/LongTR.git
cd LongTR || exit
make
mv ./LongTR ../../bin
cd .. || exit
# END LONGTR

# BEGIN TRGT
wget https://github.com/PacificBiosciences/trgt/releases/download/v0.7.0/trgt-v0.7.0-linux_x86_64.gz
gunzip trgt-v0.7.0-linux_x86_64.gz
mv ./trgt-v0.7.0-linux_x86_64 ../bin/trgt
# END TRGT
