#!/usr/bin/env python3

import json
import subprocess


SAMPLE_PREFIX = "cmh"


def main():
    with open("./data/trios.json", "r") as fh:
        trio_data: dict[str, dict[str, str]] = json.load(fh)

    for trio_id, bams in trio_data.items():
        subprocess.check_call(" ".join((
            "sbatch",
            (
                f"--export="
                f"SEED=1234,"
                f"CHILD={SAMPLE_PREFIX}{trio_id}-1,"
                f"FATHER={SAMPLE_PREFIX}{trio_id}-2,"
                f"MOTHER={SAMPLE_PREFIX}{trio_id}-3,"
                f"OUT_JSON=./out/mi/{SAMPLE_PREFIX}{trio_id}.json"
            ),
            "./strkit_mi_job.bash",
        )), shell=True)


if __name__ == "__main__":
    main()
