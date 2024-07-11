#!/usr/bin/env python3

import json
import pysam
from pathlib import Path


bench_dir = Path("./out/hg002_benchmark")
call_dir = Path("../2_giab_calls/out/calls")
techs = ("hifi", "ont")
callers = ("longtr", "strkit", "trgt")


def load_truscore_dist():
    truscores_by_tech_and_caller = {}

    for tech in techs:
        truscores_by_tech_and_caller[tech] = truscores_by_tech_and_caller.get(tech) or dict()
        for caller in callers:
            v = bench_dir / tech / caller / "phab_bench" / "tp-comp.vcf.gz"

            if not v.exists():
                print(f"{v} does not exist")
                continue

            res = []

            with pysam.VariantFile(v) as vf:
                for var in vf.fetch():
                    res.append({
                        "seq": var.info["PctSeqSimilarity"],
                        "siz": var.info["PctSizeSimilarity"],
                        "rec": var.info["PctRecOverlap"],
                        "tru": var.info["TruScore"],
                        # TODO: sequence % (A/T/G/C)
                    })

            truscores_by_tech_and_caller[tech][caller] = res

    return truscores_by_tech_and_caller


def load_gt_stats():
    gt_stats_by_tech_and_caller = {}

    for tech in techs:
        gt_stats_by_tech_and_caller[tech] = gt_stats_by_tech_and_caller.get(tech) or dict()
        for caller in callers:
            p = bench_dir / tech / caller / "phab_bench" / "summary.json"
            if not p.exists():
                print(f"{p} does not exist")
                continue

            with open(p, "r") as fh:
                gt_stats_by_tech_and_caller[tech][caller] = json.load(fh)

    return gt_stats_by_tech_and_caller


def main():
    gt_stats = load_gt_stats()
    seq_stats = load_truscore_dist()

    for tech in techs:
        for caller in callers:
            x = gt_stats[tech].get(caller)
            if not x:
                continue

            gtm = x["gt_matrix"]

            hom_alt_m = gtm["(1, 1)"]
            het_m_1 = gtm["(0, 1)"]
            het_m_2 = gtm["(1, 0)"]

            total_p = sum(hom_alt_m.values()) + sum(het_m_1.values()) + sum(het_m_2.values())

            false_het = (hom_alt_m["(1, 0)"] + hom_alt_m["(0, 1)"]) / total_p
            false_hom_alt = (het_m_1["(1, 1)"] + het_m_2["(1, 1)"]) / total_p
            false_hom_ref = x["FN"] / x["base cnt"]

            print(f"{tech}\t{caller}\tfalse het: {false_het:.3f}; false hom alt: {false_hom_alt:.3f}; FNR: {false_hom_ref}")

    for tech in techs:
        for caller in callers:
            s = seq_stats[tech].get(caller)
            if not s:
                continue

            avg_seq = sum(x["seq"] for x in s) / len(s)
            avg_t = sum(x["tru"] for x in s) / len(s)

            print(f"{tech}\t{caller}\tavg truscore: {avg_t:.2f}\tavg seq sim: {avg_seq:.4f}")


if __name__ == "__main__":
    main()
