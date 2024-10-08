#!/bin/bash
#SBATCH --mem=12G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --account=rrg-bourqueg-ad

mkdir -p ./out/mi

strkit mi --caller strkit-vcf \
    "./out/calls/${CHILD}.strkit.vcf.gz" \
    "./out/calls/${FATHER}.strkit.vcf.gz" \
    "./out/calls/${MOTHER}.strkit.vcf.gz" \
    --hist \
    --json "${OUT_JSON}" \
    --test wmw \
    --mt-corr fdr_tsbky
