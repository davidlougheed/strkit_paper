#!/usr/bin/env bash

CMH_DATA='/lustre03/project/6007512/C3G/projects/CMH_Data'

find "${CMH_DATA}" -name '*.bam' | grep -vE '\.az' | ./find_trios.py data/trios.json
