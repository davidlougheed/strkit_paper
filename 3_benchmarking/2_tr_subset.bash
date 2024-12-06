#!/usr/bin/env bash

module load bcftools
bcftools view \
  -e 'INFO/TRFperiod=1' \
  -Oz -o data/HG002_GRCh38_TandemRepeats_v1.0.1.no_homopolymers.vcf.gz \
  data/HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz
tabix 'data/HG002_GRCh38_TandemRepeats_v1.0.1.no_homopolymers.vcf.gz'
