#!/usr/bin/env python3

import subprocess
import sys
# from common import call_script_at_covs, COVS_BY_TECH, SEEDS_BY_TECH
from common import REF, TECHS, SAMPLES_BY_TECH, KARYOTYPES_BY_SAMPLE

if __name__ == "__main__":
    script = sys.argv[-2]
    tech = sys.argv[-1]  # hifi or ont

    assert tech in TECHS

    for sample in SAMPLES_BY_TECH[tech]:
        sex_kary = KARYOTYPES_BY_SAMPLE[sample]
        haploid_chrs = ",".join(tuple(sex_kary))
        print(f"{sample}:")
        subprocess.check_call(" ".join((
            "sbatch",
            (
                f"--export="
                f"SEED=1234,"
                f"REF={REF},"
                f"TECH={tech},"
                f"SAMPLE={sample},"
                f"BAM=../1_cov_subsetting/data/{tech}/{sample}.aligned.bam,"
                f"HAPLOID_CHRS={haploid_chrs},"
                f"KARYOTYPE={sex_kary}"
            ),
            script,
        )), shell=True)

    # call_script_at_covs(
    #     sys.argv[1],
    #     covs=COVS_BY_TECH[tech],
    #     seeds=SEEDS_BY_TECH[tech],
    #     extra_env="TECH=" + tech,
    # )
