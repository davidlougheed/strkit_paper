#!/usr/bin/env bash

module load python/3.9

# BEGIN DATA

cd data || exit

wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/HG002_GRCh38_TandemRepeats_v1.0.bed.gz
wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/HG002_GRCh38_TandemRepeats_v1.0.vcf.gz
wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/HG002_GRCh38_TandemRepeats_v1.0.vcf.gz.tbi

gunzip adotto_TRregions_v1.2.bed.gz

cd .. || exit

# END DATA

# BEGIN TRUVARI
python3 -m venv ./env_truvari
source env/bin/activate
pip install -r Truvari==4.2.0
deactivate
# END TRUVARI

# BEGIN STRKIT
python3 -m venv ./env_truvari
source env/bin/activate
pip install -r Truvari==4.2.0
deactivate
# END STRKIT

# BEGIN LONGTR
git clone https://github.com/gymrek-lab/LongTR.git
cd LongTR || exit
make
mv ./LongTR ../bin
cd .. || exit
# END LONGTR

# BEGIN TRGT
cd bin || exit
wget https://github.com/PacificBiosciences/trgt/releases/download/v0.7.0/trgt-v0.7.0-linux_x86_64.gz
gunzip trgt-v0.7.0-linux_x86_64.gz
mv ./trgt-v0.7.0-linux_x86_64 ./trgt
cd .. || exit
# END TRGT
