#!/usr/bin/env python3

import csv
import json
import pysam
import re
from io import StringIO
from pathlib import Path
from urllib.parse import unquote as url_unquote

from common import CALLERS, LABELS, TECHS


bench_dir = Path("./out/hg002_benchmark")
call_dir = Path("../2_giab_calls/out/calls")

measures = ("F1", "PPV", "TPR")


def build_transl(f, dx, dy):
    from matplotlib.transforms import ScaledTranslation
    return ScaledTranslation(dx / f.dpi, dy / f.dpi, f.dpi_scale_trans)


def load_truscore_dist():
    truscores_by_tech_and_caller = {}

    for tech in TECHS:
        truscores_by_tech_and_caller[tech] = truscores_by_tech_and_caller.get(tech) or dict()
        for caller in CALLERS:
            vs = (
                bench_dir / tech / caller / "phab_bench" / "tp-comp.vcf.gz",
                bench_dir / tech / caller / "phab_bench" / "fn.vcf.gz",
                bench_dir / tech / caller / "phab_bench" / "fp.vcf.gz",
            )

            res = []

            for v in vs:
                if not v.exists():
                    print(f"{v} does not exist")
                    continue
                with pysam.VariantFile(v) as vf:
                    for var in vf.fetch():
                        if (tru := var.info["TruScore"]) is None:
                            continue  # missed call, no score
                        res.append({
                            "seq": var.info["PctSeqSimilarity"],
                            "siz": var.info["PctSizeSimilarity"],
                            "rec": var.info["PctRecOverlap"],
                            "tru": tru,
                            # TODO: sequence % (A/T/G/C)
                        })

            truscores_by_tech_and_caller[tech][caller] = res

    return truscores_by_tech_and_caller


def load_gt_stats():
    gt_stats_by_tech_and_caller = {}

    for tech in TECHS:
        gt_stats_by_tech_and_caller[tech] = gt_stats_by_tech_and_caller.get(tech) or dict()
        for caller in CALLERS:
            p = bench_dir / tech / caller / "phab_bench" / "summary.json"
            if not p.exists():
                print(f"{p} does not exist")
                continue

            with open(p, "r") as fh:
                gt_stats_by_tech_and_caller[tech][caller] = json.load(fh)

    return gt_stats_by_tech_and_caller


def load_region_breakdown():
    sizebin_csv_pattern = re.compile(
        r'<a href="data:text/csv;charset=utf-8,([a-zA-Z0-9.\-%,]+)" '
        r'download="sizebin.csv" class="download-button">Download</a>'
    )

    region_breakdown_by_tech_and_caller = {}
    n_dist_by_tech_and_caller = {}

    for tech in TECHS:
        region_breakdown_by_tech_and_caller[tech] = {}
        n_dist_by_tech_and_caller[tech] = {}
        for caller in CALLERS:
            report = bench_dir / tech / caller / "laytr_report.html"

            if not report.exists():
                print(f"{report} does not exist")
                continue

            with open(report, "r") as fh:
                report_html = fh.read()

            total_alleles: int = 0
            total_alleles_sub_50: int = 0
            total_alleles_sub_200: int = 0

            # [2:] to skip SNP and 1-5 bins, which shouldn't even be there...
            report_csv = list(csv.DictReader(StringIO(url_unquote(sizebin_csv_pattern.findall(report_html)[0]))))[2:]

            acc = []
            for entry in report_csv:
                entry_bin = entry[""]

                # hacky: get int repr of bin end
                entry_bin_end = 0 if entry_bin == "SNP" else int(
                    entry_bin.split(",")[-1]
                    .replace(")", "")
                    .replace("1k", "1000")
                    .replace("2.5k", "2500")
                    .replace("5k", "5000")
                    .replace(">=", "100000")
                )

                ta = int(entry["base P"]) + int(entry["base N"])
                total_alleles += ta
                if entry_bin_end <= 50:
                    total_alleles_sub_50 += ta
                if entry_bin_end <= 200:
                    total_alleles_sub_200 += ta

                for m in measures:
                    acc.append(
                        {
                            "bin": entry_bin,
                            "y": float(entry[m]),
                            "measure": m,
                        }
                    )

            print(
                f"{tech}\t{caller}\tTotal alleles: {total_alleles}; "
                f"sub 50: {total_alleles_sub_50} ({total_alleles_sub_50 / total_alleles * 100:.1f}%); "
                f"sub 200: {total_alleles_sub_200} ({total_alleles_sub_200 / total_alleles * 100:.1f}%)")

            region_breakdown_by_tech_and_caller[tech][caller] = acc

            region_breakdown_by_tech_and_caller[tech][caller] = [
                {
                    "bin": entry[""],
                    "y": float(entry[m]),
                    "measure": m,
                }
                for entry in report_csv
                # F1, precision, sensitivity
                for m in measures  # , ACC
                # {
                #     "bin": entry[""],
                #     "n": int(entry["base P"]) + int(entry["base N"]) + int(entry["comp P"]) + int(entry["comp N"]),
                #     "ppv": float(entry["PPV"]),
                #     "tpr": float(entry["TPR"]),
                #     "acc": float(entry["ACC"]),
                #     "f1": float(entry["F1"]),
                # }
                # for entry in report_csv
            ]

            n_dist_by_tech_and_caller[tech][caller] = [
                {
                    "bin": entry[""],
                    "n": int(entry["base P"]) + int(entry["base N"]) + int(entry["comp P"]) + int(entry["comp N"]),
                    # TODO: break down by true/false positive/negative? since some of these fluctuate based on very few
                }
                for entry in report_csv
            ]

            # region_breakdown_by_tech_and_caller[tech][caller] = [
            #     {
            #         "bin": entry[""],
            #         "n": int(entry["base P"]) + int(entry["base N"]) + int(entry["comp P"]) + int(entry["comp N"]),
            #         "ppv": float(entry["PPV"]),
            #         "tpr": float(entry["TPR"]),
            #         "acc": float(entry["ACC"]),
            #         "f1": float(entry["F1"]),
            #     }
            #     for entry in report_csv
            # ]

    return region_breakdown_by_tech_and_caller, n_dist_by_tech_and_caller


def main():
    gt_stats = load_gt_stats()
    seq_stats = load_truscore_dist()

    for tech in TECHS:
        for caller in CALLERS:
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

            print(
                f"{tech}\t{caller}\tfalse het: {false_het:.3f}; false hom alt: {false_hom_alt:.3f}; "
                f"FNR: {false_hom_ref}"
            )

    for tech in TECHS:
        for caller in CALLERS:
            s = seq_stats[tech].get(caller)
            if not s:
                continue

            avg_seq = sum(x["seq"] for x in s) / len(s)
            avg_t = sum(x["tru"] for x in s) / len(s)

            print(f"{tech}\t{caller}\tavg truscore: {avg_t:.2f}\tavg seq sim: {avg_seq:.4f}")

    rb, ns = load_region_breakdown()

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_theme(style="ticks", rc={"axes.spines.top": False, "font.family": "Helvetica"})
    # sns.set(font="Helvetica")

    fig = plt.figure(figsize=(15, 10))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.215, top=0.95, wspace=0.25, hspace=0.38)

    bar_df = pd.DataFrame.from_records(ns["hifi"][next(iter(ns["hifi"].keys()))])

    subfigs = fig.subfigures(nrows=2, ncols=1)

    for ti, (tech, subfig) in enumerate(zip(TECHS, subfigs), 1):
        subfig.suptitle("PacBio HiFi" if tech == "hifi" else "ONT R10 Duplex")
        for mi, m in enumerate(measures, 1):
            ax1 = subfig.add_subplot(1, 3, mi)
            ax2 = ax1.twinx()

            ax1.set_xlabel("Absolute change in allele size vs. HG38 (∆bp)")
            ax1.set_ylabel(LABELS[m])
            ax1.grid(False)
            ax1.tick_params(axis="x", labelrotation=60, labelsize=9)
            ax1.set_zorder(ax2.get_zorder() + 1)
            ax1.set_facecolor("#FF000000")
            ax1.set_ylim([0.3, 1.02])

            # apply offset to all xticklabels
            offset = build_transl(fig, -7, 5)
            for label in ax1.xaxis.get_majorticklabels():
                label.set_transform(label.get_transform() + offset)

            ax2.semilogy(10)
            ax2.grid(False)
            if mi < len(measures):
                ax2.set_yticks([])
            else:
                ax2.set_ylabel("# regions", rotation=-90, labelpad=18)

            line_df = pd.DataFrame.from_records([
                {"c": caller, "Caller": LABELS[caller], **rec}
                for caller in rb[tech]
                for rec in rb[tech][caller]
                if rec["measure"] == m
            ])

            palette = [
                "#d95f02",
                "#984ea3",
                "#238b45",
                "#66c2a4",
                "#e7298a",
            ]

            p = sns.color_palette(palette)

            sns.barplot(x="bin", y="n", data=bar_df, color="#DFDFDF", ax=ax2, width=1)
            sns.lineplot(
                x="bin", y="y", hue="Caller", data=line_df, ax=ax1, errorbar=None, legend="auto" if mi == 1 else None,
                palette=p
            )

            # df = pd.DataFrame.from_records([{"caller": caller, **rec} for caller in rb["hifi"] for rec in rb["hifi"][caller]])
            # sns.relplot(data=df, x="bin", y="y", kind="line", col="measure", hue="caller")
            #
            # df2 = pd.DataFrame.from_records([{"caller": caller, **rec} for caller in rb["ont"] for rec in rb["ont"][caller]])
            # sns.relplot(data=df2, x="bin", y="y", kind="line", col="measure", hue="caller")

    plt.savefig("./out/fig_scores.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
