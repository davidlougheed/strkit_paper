#!/usr/bin/env python3

import json
import os.path
import subprocess


REF = "./data/ref/GRCh38_no_alt_analysis_set.fna"
SAMPLE_PREFIX = "cmh"


def non_zero_time_file(path: str):
    with open(path, "r") as fh:
        contents = fh.read()
    return "non-zero status" in contents


def main():
    with open("./data/trios.json", "r") as fh:
        trio_data: dict[str, dict[str, str]] = json.load(fh)

    force = ()
    for script in ("longtr", "strdust", "strkit", "strkit-no-snv", "straglr", "trgt"):
        for trio_id, bams in trio_data.items():
            for ind_key, bam in bams.items():
                sample = f"{SAMPLE_PREFIX}{trio_id}-{ind_key}"
                time_file = f"./out/calls/hifi/{sample}.{script}.time"
                if not os.path.exists(time_file) or non_zero_time_file(time_file) or script in force:
                    # hacky resubmission check - if time file not found or exists but mentions a non-zero status code.
                    subprocess.check_call(" ".join((
                        "sbatch",
                        (
                            f"--export="
                            f"SEED=1234,"
                            f"REF={REF},"
                            f"TECH=hifi,"
                            f"SAMPLE={sample},"
                            f"HAPLOID_CHRS=X,X,"  # dummy karyotype values - we'll just analyze autosomes
                            f"KARYOTYPE=XX,"  # "
                            f"SEX=f,"  # "
                            f"PHASED=,"
                            f"EXECUTABLE=./trgt/target/release/trgt,"  # trgt without haplotags
                            f"BAM={bam}"
                        ),
                        f"../2_giab_calls/{script}.bash",
                    )), shell=True)


if __name__ == "__main__":
    main()
