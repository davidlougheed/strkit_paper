#!/usr/bin/env python3
# Needs `module load samtools` first

import orjson
import polars
import polars as pl
import subprocess


def get_bam_depth(bf: str) -> float:
    p_depth = subprocess.Popen(("samtools", "depth", "-a", bf), stdout=subprocess.PIPE)
    res = subprocess.check_output(("awk", '{sum+=$3} END { print "Average = ",sum/NR}'), stdin=p_depth.stdout)
    p_depth.wait()
    res_strs: list[str] = res.decode("ascii").strip().split(" ")
    return float(res_strs[-1])


def compute_coverages():
    records = []

    with open("./data/trios.json", "rb") as fh:
        trios = orjson.loads(fh.read())

    for idx, (trio_id, trio_data) in enumerate(trios.items(), 1):
        child_bam = trio_data["1"]
        p1_bam = trio_data["2"]
        p2_bam = trio_data["3"]
        child_depth = get_bam_depth(child_bam)
        p1_depth = get_bam_depth(p1_bam)
        p2_depth = get_bam_depth(p2_bam)

        rec = {"idx": idx, "trio": trio_id, "child": child_depth, "p1": p1_depth, "p2": p2_depth}
        print(rec)
        records.append(rec)

    df = polars.from_dicts(records)
    with pl.Config(tbl_rows=50):
        print(df)

    df.write_csv("./out/ga4k_coverages.csv")


def main():
    compute_coverages()


if __name__ == "__main__":
    main()
