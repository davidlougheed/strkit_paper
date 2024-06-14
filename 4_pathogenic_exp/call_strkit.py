#!/usr/bin/env python3

import subprocess

from common import SAMPLE_KTS, BASE_PATH, REF_GENOME, bam


def main():
    for sample, karyotype in SAMPLE_KTS.items():
        print(sample, karyotype)
        subprocess.check_call([
            "strkit", "call",
            "--ref", REF_GENOME,
            "--loci", str(BASE_PATH / "data" / "catalog.strkit.bed"),
            "--sex-chr", karyotype,
            "--hq",
            "--realign",
            "--respect-ref",
            "--targeted",
            "--max-reads", "500",
            "-k", "peak",
            "--json", str(BASE_PATH / "out" / f"{sample}.strkit.json"),
            "--vcf", str(BASE_PATH / "out" / f"{sample}.strkit.vcf"),
            "--indent-json",
            bam(sample),
        ])


if __name__ == "__main__":
    main()
