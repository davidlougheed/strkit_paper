#!/usr/bin/env python3

import subprocess
import sys
# from common import call_script_at_covs, COVS_BY_TECH, SEEDS_BY_TECH
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
        print(f"tech={tech} phased='{phased}' sample={sample}:")
        subprocess.check_call(" ".join((
            "sbatch",
            (
                f"--export="
                f"SEED=1234,"
                f"REF={REF},"
                f"TECH={tech},"
                f"SAMPLE={sample},"
                f"BAM=../1_alignment/data/{tech}/{sample}.{'phased.' if phased else ''}aligned.bam,"
                f"HAPLOID_CHRS={haploid_chrs},"
                f"KARYOTYPE={sex_kary},"
                f"PHASED={phased}"
            ),
            script,
        )), shell=True)

    # call_script_at_covs(
    #     sys.argv[1],
    #     covs=COVS_BY_TECH[tech],
    #     seeds=SEEDS_BY_TECH[tech],
    #     extra_env="TECH=" + tech,
    # )
