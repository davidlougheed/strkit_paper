#!/usr/bin/env python3

import json
import pandas as pd
import seaborn as sns
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path

from common import CALLERS, LABELS, TECH_LABELS

PALETTE = [
    "#d95f02",  # LongTR
    "#984ea3",  # STRdust
    "#238b45",  # STRkit
    "#66c2a4",  # STRkit (no SNVs)
    # "#386cb0",  # Straglr
    "#e7298a",  # TRGT
]

mi_techs = ("hifi", "ont-simplex")
bench_base_dir = Path("./out/hg002_benchmark")


font_size = 10
font_rc = {
    "font.family": "Arial",
    "font.size": font_size,
    "axes.titlesize": font_size,
    "axes.labelsize": font_size,
    "xtick.labelsize": font_size,
    "ytick.labelsize": font_size,
    "legend.title_fontsize": font_size,
    "legend.fontsize": font_size,
}
mpl.rcParams.update(font_rc)


def load_mi_reports():
    reports = {}

    for tech in mi_techs:
        for caller in CALLERS:
            report_path = bench_base_dir / tech / caller / "mi_report.json"
            if not report_path.exists():
                print(f"{report_path} does not exist, skipping...")
                continue
            with open(report_path, "r") as fh:
                if tech not in reports:
                    reports[tech] = {}
                reports[tech][caller] = json.load(fh)

    return reports


def main():
    sns.set_theme(style="white", font="Arial", rc={"axes.spines.top": False, **font_rc})

    reports = load_mi_reports()

    for tech, sub_reports in reports.items():
        for caller, report in sub_reports.items():
            out_str = (
                f"{caller.rjust(40)}: n_loci_trio_called={report['n_loci_trio_called']} "
                f"cn={report['mi']['val']*100:.2f}"
            )

            for v in ("mi_seq", "mi_sl", "mi_sl_pm1"):
                if report[v] is not None:
                    out_str += f" {v[3:]}={report[v]['val']*100:.2f}"

            print(out_str)

    fig = plt.figure(figsize=(6.5, 7.5))
    fig.subplots_adjust(left=0.1, right=0.882, top=0.956, bottom=0.19, hspace=0.54)

    # subfigs = fig.subfigures(nrows=2, ncols=1)

    for t_idx, (tech, sub_reports) in enumerate(reports.items()):
        records = []
        count_records = []

        for caller, report in sub_reports.items():
            if caller == "straglr":
                continue

            # TODO: shouldn't be same bins as max_sizebin from Truvari at all!

            init_d = {
                "count": 0,
                "total": 0,
                "mi": 0.0,
                "mi_pm1": 0.0,
                "mi_95": 0.0,
                "mi_seq": 0.0,
                "mi_sl": 0.0,
                "mi_sl_pm1": 0.0,
            }

            bins = {
                "[0, 10)": {**init_d},
                "[10, 20)": {**init_d},
                "[20, 30)": {**init_d},
                "[30, 40)": {**init_d},
                "[40, 50)": {**init_d},
                "[50, 100)": {**init_d},
                "[100, 200)": {**init_d},
                "[200, 300)": {**init_d},
                "[300, 400)": {**init_d},
                "[400, 600)": {**init_d},
                "[800, 1k)": {**init_d},
                "[1k, 2.5k)": {**init_d},
                ">=5k": {**init_d},
            }

            for hist_bin in report["hist"]:
                if hist_bin["mi"] is None:
                    continue

                int_bin = hist_bin["bin"]
                if int_bin < 50:
                    str_bin = f"[{int_bin}, {int_bin + 10})"
                elif int_bin < 100:
                    str_bin = "[50, 100)"
                elif int_bin < 400:
                    b = (int_bin // 100) * 100
                    str_bin = f"[{b}, {b + 100})"
                elif int_bin < 600:
                    str_bin = "[400, 600)"
                elif int_bin < 1000:
                    str_bin = "[800, 1k)"
                elif int_bin < 2500:
                    str_bin = "[1k, 2.5k)"
                else:
                    str_bin = ">=5k"

                old_count = bins[str_bin]["count"]
                bins[str_bin]["count"] += hist_bin["bin_count"]
                # bins[str_bin]["total"] += hist_bin["bin_total"]
                bins[str_bin]["mi"] = (
                    ((bins[str_bin]["mi"] * old_count) + hist_bin["mi"] * hist_bin["bin_count"]) / bins[str_bin]["count"]
                )
                bins[str_bin]["mi_pm1"] = (
                    ((bins[str_bin]["mi_pm1"] * old_count) + hist_bin["mi_pm1"] * hist_bin["bin_count"])
                    / bins[str_bin]["count"]
                )

                if hist_bin["mi_95"] is not None:
                    bins[str_bin]["mi_95"] = (
                        ((bins[str_bin]["mi_95"] * old_count) + hist_bin["mi_95"] * hist_bin["bin_count"])
                        / bins[str_bin]["count"]
                    )

                if hist_bin["mi_seq"] is not None:
                    bins[str_bin]["mi_seq"] = (
                        ((bins[str_bin]["mi_seq"] * old_count) + hist_bin["mi_seq"] * hist_bin["bin_count"])
                        / bins[str_bin]["count"]
                    )

                if hist_bin["mi_sl"] is not None:
                    bins[str_bin]["mi_sl"] = (
                        ((bins[str_bin]["mi_sl"] * old_count) + hist_bin["mi_sl"] * hist_bin["bin_count"])
                        / bins[str_bin]["count"]
                    )

                if hist_bin["mi_sl_pm1"] is not None:
                    bins[str_bin]["mi_sl_pm1"] = (
                        ((bins[str_bin]["mi_sl_pm1"] * old_count) + hist_bin["mi_sl_pm1"] * hist_bin["bin_count"])
                        / bins[str_bin]["count"]
                    )

            for k, v in bins.items():
                if v["count"] == 0:
                    continue
                count_records.append({"c": "_" + caller, "Caller": LABELS[caller], "bin": k, "y": v["count"]})
                # records.append({"c": caller, "Caller": LABELS[caller],  "bin": k, "measure": "mi", "y": v["mi"]})
                # records.append({"c": caller, "Caller": LABELS[caller],  "bin": k, "measure": "mi_pm1", "y": v["mi_pm1"]})
                records.append({"c": caller, "Caller": LABELS[caller], "bin": k, "measure": "mi_seq", "y": v["mi_seq"]})
                # records.append({"c": caller, "Caller": LABELS[caller],  "bin": k, "measure": "mi_sl", "y": v["mi_sl"]})
                # records.append({
                #     "c": caller, "Caller": LABELS[caller], "bin": k, "measure": "mi_sl_pm1", "y": v["mi_sl_pm1"]
                # })

                # if v["mi_95"]:
                #     records.append({"caller": caller, "bin": k, "measure": "mi_95", "y": v["mi_95"]})

                # if k == ">=5k":
                #     print(caller, v)

        df = pd.DataFrame.from_records(records)
        df_count = pd.DataFrame.from_records(count_records)

        # landscape fig
        # fig = plt.figure(figsize=(9, 5))

        # fig.subplots_adjust(left=0.06, right=0.914, top=0.985, bottom=0.29)
        p = sns.color_palette(PALETTE)

        callers_hue_order = tuple("_" + c for c in CALLERS if c != "straglr")

        ax = fig.add_subplot(210 + (t_idx + 1))
        ax.set_title(TECH_LABELS[tech])
        ax.set_ylim(0.0, 1.0)

        ax2 = ax.twinx()
        ax2.set_ylim(0, 500000)

        ax.set_ylabel("Sequence Mendelian inheritance rate (fraction)")
        ax.set_xlabel("Locus size in reference genome (base pairs)")

        ax2.set_ylabel("# trio-called loci")

        # ax2.semilogy(10)

        sns.lineplot(x="bin", y="y", data=df, hue="Caller", palette=p, ax=ax)
        bp = sns.barplot(
            x="bin", y="y", data=df_count, hue="c", palette=p, ax=ax2, alpha=0.4, hue_order=callers_hue_order
        )

        for c in bp.containers:
            bp.bar_label(c, fontsize=6, rotation=90, padding=2, color="#999999")

        ax.get_legend().remove()
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        if t_idx == 1:
            # noinspection PyTypeChecker
            legend = fig.legend(
                title="Caller",
                loc="outside lower center",
                mode="expand",
                ncols=5,
                frameon=False,
                handles=[Line2D([0], [0], color=c) for c in PALETTE],
                labels=[
                    LABELS["longtr"],
                    LABELS["strdust"],
                    LABELS["strkit"],
                    LABELS["strkit-no-snv"],
                    # LABELS["straglr"],
                    LABELS["trgt"],
                ],
            )
            for line in legend.get_lines():
                line.set_linewidth(3)

    plt.savefig(f"./out/fig_sequence_mi_combined.png", dpi=300)
    plt.savefig(f"./out/fig_sequence_mi_combined.pdf", dpi=300)  # TODO: final proper name
    plt.show()


if __name__ == "__main__":
    main()
