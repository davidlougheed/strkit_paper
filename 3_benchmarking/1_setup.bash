#!/usr/bin/env bash

# laytr doesn't work with python 3.11 due to edlib erroring with:
#  edlib.bycython.cpp:198:12: fatal error: longintrepr.h: No such file or directory
module load python/3.9

# BEGIN DATA

cd data || exit

wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/HG002_GRCh38_TandemRepeats_v1.0.bed.gz
wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz
wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz.tbi
wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/adotto_TRv1.1_4mers.map
wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/adotto_TRv1.1_4mers.som

cd .. || exit

# END DATA

# BEGIN TRUVARI
python3 -m venv ../envs/env_truvari
source ../envs/env_truvari/bin/activate
pip install -U Truvari==4.2.2
deactivate
# END TRUVARI

# BEGIN LAYTR
python3 -m venv ../envs/env_laytr
source ../envs/env_laytr/bin/activate
git clone https://github.com/ACEnglish/laytr.git
pip install -U ./laytr
rm -rf laytr
deactivate
# END LAYTR
