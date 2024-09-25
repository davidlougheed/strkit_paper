#!/usr/bin/env python3

import subprocess

from common import SAMPLE_KTS, BASE_PATH, REF_GENOME, bam


def main():
    for sample, karyotype in SAMPLE_KTS.items():
        print("LongTR", sample, karyotype)
        subprocess.check_call([
            "../bin/LongTR",
            "--bams", bam(sample),
            "--lib-from-samp",
            "--fasta", REF_GENOME,
            "--regions", str(BASE_PATH / "data" / "catalog.longtr.bed"),
            # "--skip-assembly",
            "--max-tr-len", "3000",
            "--tr-vcf", str(BASE_PATH / "out" / f"{sample}.longtr.vcf.gz"),
            *(["--haploid-chrs", "X,Y"] if "Y" in karyotype else []),
        ])


if __name__ == "__main__":
    main()
