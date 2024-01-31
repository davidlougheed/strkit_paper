#!/usr/bin/env bash

module load python/3.9

REF="/lustre03/project/rrg-bourqueg-ad/dlough2/workdir2022/ref/hg38.analysisSet.fa"

mkdir -p ./out/calls/hifi/
mkdir -p ./out/calls/ont/

python ./run_all.py ./longtr.bash hifi
python ./run_all.py ./strkit.bash hifi
python ./run_all.py ./trgt.bash hifi
