#!/usr/bin/env python3

import subprocess

from common import SAMPLE_KTS, BASE_PATH, REF_GENOME, bam


def main():
    for sample, karyotype in SAMPLE_KTS.items():
        print("Straglr", sample, karyotype)
        subprocess.check_call([
            "straglr.py",
            bam(sample),
            REF_GENOME,
            "--loci", str(BASE_PATH / "data" / "catalog.strkit.bed"),
        ])


if __name__ == "__main__":
    main()
