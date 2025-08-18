#!/usr/bin/env python3

import subprocess
import sys
from common import REF, TECHS, SAMPLES_BY_TECH, KARYOTYPES_BY_SAMPLE

if __name__ == "__main__":
    script = sys.argv[-3]
    tech = sys.argv[-2]  # hifi or ont
    phased = sys.argv[-1]  # phased BAM: 1 or blank/0
    phased = "1" if phased == "1" else ""  # normalize to 1 or blank

    assert tech in TECHS

    for sample in SAMPLES_BY_TECH[tech]:
        sex_kary = KARYOTYPES_BY_SAMPLE[sample]
        haploid_chrs = ",".join(tuple(sex_kary))
        print(f"tech={tech} script={script} phased='{phased}' sample={sample}:")
        bam_part = "aligned" + (".subsam" if tech == "ont-simplex" else "")
        subprocess.check_call(" ".join((
            "sbatch",
            (
                f"--export="
                f"SEED=1234,"
                f"REF={REF},"
                f"TECH={tech},"
                f"SAMPLE={sample},"
                f"BAM=../1_alignment/data/{tech}/{sample}.{'phased.' if phased else ''}{bam_part}.bam,"
                f"HAPLOID_CHRS={haploid_chrs},"
                f"KARYOTYPE={sex_kary},"
                # for Straglr; all of these samples have normal sex karyotypes:
                f"SEX={'f' if sex_kary == 'XX' else 'm'},"
                f"PHASED={phased}"
            ),
            script,
        )), shell=True)
