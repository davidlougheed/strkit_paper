#!/usr/bin/env python3

import subprocess

from common import SAMPLE_KTS, BASE_PATH, REF_GENOME, bam


def main():
    for sample, karyotype in SAMPLE_KTS.items():
        print("STRdust", sample, karyotype)
        with open(BASE_PATH / "out" / f"{sample}.strdust.vcf", "w") as fh:
            subprocess.check_call([
                "../bin/STRdust",
                "-R", str(BASE_PATH / "data" / "catalog.strkit.bed"),
                "--somatic",
                "--unphased",
                *(("--haploid", "X,Y") if karyotype == "XY" else ()),
                REF_GENOME,
                bam(sample),
            ], stdout=fh)


if __name__ == "__main__":
    main()
