#!/usr/bin/env bash

module load StdEnv/2023
module load python/3.11

# BEGIN DATA

cd data || exit

giab_files=( "HG002_GRCh38_TandemRepeats_v1.0.bed.gz" "HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz" "HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz.tbi" "adotto_TRv1.1_4mers.map" "adotto_TRv1.1_4mers.som" )

for giab_file in "${giab_files[@]}"; do
  if [[ -n "${giab_file}" ]]; then
    wget "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/TandemRepeats_v1.0/GRCh38/${giab_file}" -O "${giab_file}"
  fi
done

snv_benchmark="HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"

if [[ ! -f "${snv_benchmark}" ]]; then
  wget "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/${snv_benchmark}" -O "${snv_benchmark}"
  wget "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/${snv_benchmark}.tbi" -O "${snv_benchmark}.tbi"
fi

cd .. || exit

# END DATA

# BEGIN TRUVARI
python3 -m venv ../envs/env_truvari
source ../envs/env_truvari/bin/activate
pip install -U Truvari==5.3.0
# alliance pywfa install is broken
pip install --no-cache-dir --no-binary :all: --ignore-installed pywfa==0.5.1
deactivate
# END TRUVARI

# BEGIN LAYTR
python3 -m venv ../envs/env_laytr
source ../envs/env_laytr/bin/activate
pip install wheel
git clone https://github.com/ACEnglish/laytr.git
pip install -U ./laytr
# alliance pywfa install is broken
pip install --no-cache-dir --no-binary :all: --ignore-installed pywfa==0.5.1
rm -rf laytr
deactivate
# END LAYTR
