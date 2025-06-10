#!/usr/bin/env bash

# laytr doesn't work with python 3.11 due to edlib erroring with:
#  edlib.bycython.cpp:198:12: fatal error: longintrepr.h: No such file or directory
module load StdEnv/2020
module load python/3.10

# BEGIN DATA

cd data || exit

giab_files=( "HG002_GRCh38_TandemRepeats_v1.0.bed.gz" "HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz" "HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz.tbi" "adotto_TRv1.1_4mers.map" "adotto_TRv1.1_4mers.som" )

for giab_file in "${giab_files[@]}"; do
  if [[ -n "${giab_file}" ]]; then
    wget "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/${giab_file}" -O "${giab_file}"
  fi
done

cd .. || exit

# END DATA

# BEGIN TRUVARI
python3 -m venv ../envs/env_truvari
source ../envs/env_truvari/bin/activate
pip install -U Truvari==5.3.0
deactivate
# END TRUVARI

# BEGIN LAYTR
python3 -m venv ../envs/env_laytr
source ../envs/env_laytr/bin/activate
pip install wheel
git clone https://github.com/ACEnglish/laytr.git
pip install -U ./laytr
rm -rf laytr
deactivate
# END LAYTR
