#!/usr/bin/env python3

import subprocess

from common import SAMPLE_KTS, BASE_PATH, REF_GENOME, bam


def main():
    for sample, karyotype in SAMPLE_KTS.items():
        print(sample, karyotype)
        subprocess.check_call([
            "../bin/trgt", "-v", "genotype",
            "--reads", bam(sample),
            "--genome", REF_GENOME,
            "--repeats", str(BASE_PATH / "data" / "catalog.trgt.bed"),
            "--output-prefix", str(BASE_PATH / "out" / f"{sample}.trgt"),
            "--karyotype", karyotype,
        ])


if __name__ == "__main__":
    main()
