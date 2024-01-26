#!/usr/bin/env bash

module load python/3.9
source env/bin/activate

cd out || exit
python -m ../../giab_benchmarking/run_all.py ../../giab_benchmarking/strkit.bash
