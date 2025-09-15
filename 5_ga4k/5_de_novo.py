#!/usr/bin/env python3

import json
import os.path
import subprocess


SAMPLE_PREFIX = "cmh"

CALLER_TO_MI_CALLER = {
    "strkit": "strkit-vcf",
    "strkit-no-snv": "strkit-vcf",
}


def main():
    with open("./data/trios.json", "r") as fh:
        trio_data: dict[str, dict[str, str]] = json.load(fh)

    force = ()
    for caller in ("longtr", "strdust", "strkit", "strkit-no-snv", "straglr", "trgt"):
        for trio_id, bams in trio_data.items():
            mi_caller = CALLER_TO_MI_CALLER.get(caller, caller)
            out_path = f"./out/mi/{SAMPLE_PREFIX}{trio_id}.{caller}.json"
            if os.path.exists(out_path) and caller not in force:
                print(f"SKIPPING [EXISTS] {out_path}")
                continue
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
                    f"EXT={'vcf.gz' if mi_caller != 'straglr' else 'tsv'},"
                    f"TECH=hifi,"
                    f"OUT_JSON={out_path}"
                ),
                "./strkit_mi_job.bash",
            )), shell=True)


if __name__ == "__main__":
    main()
