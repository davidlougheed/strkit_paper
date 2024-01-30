#!/bin/bash
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3-00
#SBATCH --account=rrg-bourqueg-ad

module load python/3.9
source env_laytr/bin/activate

# TODO

laytr giabTR --regionsummary bench_result/refine.regions.txt \
	--includebed data/HG002_GRCh38_TandemRepeats_v1.0.bed.gz \
	--som data/adotto_TRv1.1_4mers.som \
	--somap data/adotto_TRv1.1_4mers.map \
	--trcatalog data/adotto_TRregions_v1.2.bed.gz \
	--output your_report.html  # TODO
