#!/bin/bash
#SBATCH --mem=4G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1-00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2020
module load python/3.10
source ../envs/env_laytr/bin/activate

laytr giabTR --regionsummary "${BENCH_DIR}/refine.regions.txt" \
	--includebed data/HG002_GRCh38_TandemRepeats_v1.0.bed.gz \
	--som data/adotto_TRv1.1_4mers.som \
	--sommap data/adotto_TRv1.1_4mers.map \
	--trcatalog ../2_giab_calls/data/adotto_TRregions_v1.2.bed.gz \
	--output "${BENCH_DIR}/laytr_report.html"
