#!/usr/bin/env python3

import json
import subprocess


REF = "../1_cov_subsetting/data/ref/hg38.analysisSet.fa"
SAMPLE_PREFIX = "cmh"


def main():
    with open("./data/trios.json", "r") as fh:
        trio_data: dict[str, dict[str, str]] = json.load(fh)

    for trio_id, bams in trio_data.items():
        for ind_key, bam in bams.items():
            subprocess.check_call(" ".join((
                "sbatch",
                (
                    f"--export="
                    f"SEED=1234,"
                    f"SAMPLE={SAMPLE_PREFIX}{trio_id}-{ind_key},"
                    f"BAM={bam},",
                    f"REF={REF}"
                ),
                "./strkit_job.bash",
            )), shell=True)


if __name__ == "__main__":
    main()
