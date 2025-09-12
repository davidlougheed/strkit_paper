#!/usr/bin/env python3

import json
import subprocess


SAMPLE_PREFIX = "cmh"

CALLER_TO_MI_CALLER = {
    "strkit": "strkit-vcf",
    "strkit-no-snv": "strkit-vcf",
}


def main():
    with open("./data/trios.json", "r") as fh:
        trio_data: dict[str, dict[str, str]] = json.load(fh)

    for caller in ("longtr", "strdust", "strkit", "strkit-no-snv", "straglr", "trgt"):
        for trio_id, bams in trio_data.items():
            mi_caller = CALLER_TO_MI_CALLER.get(caller, caller)
            subprocess.check_call(" ".join((
                "sbatch",
                (
                    f"--export="
                    f"SEED=1234,"
                    f"CHILD={SAMPLE_PREFIX}{trio_id}-1,"
                    f"FATHER={SAMPLE_PREFIX}{trio_id}-2,"
                    f"MOTHER={SAMPLE_PREFIX}{trio_id}-3,"
                    f"CALLER={caller},"
                    f"MI_CALLER={mi_caller},"
                    f"OUT_JSON=./out/mi/{SAMPLE_PREFIX}{trio_id}.{caller}.json"
                ),
                "./strkit_mi_job.bash",
            )), shell=True)


if __name__ == "__main__":
    main()
