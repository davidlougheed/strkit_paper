import json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pathlib import Path


hifi_bench_dir = Path("./out/hg002_benchmark/hifi")
callers = ("longtr", "strkit", "strkit-no-snv", "straglr", "trgt")


def load_mi_reports():
    reports = {}

    for caller in callers:
        report_path = hifi_bench_dir / caller / "mi_report.json"
        if not report_path.exists():
            print(f"{report_path} does not exist, skipping...")
            continue
        with open(report_path, "r") as fh:
            reports[caller] = json.load(fh)

    return reports


def main():
    reports = load_mi_reports()

    bin_labels = [
        "[0, 10)",
        "[10, 20)",
        "[20, 30)",
        "[30, 40)",
        "[40, 50)",
        "[50, 100)",
        "[100, 200)",
        "[200, 300)",
        "[300, 400)",
        "[400, 600)",
        "[800, 1k)",
        "[1k, 2.5k)",
        ">=5k",
    ]
    records = []
    count_records = []

    for caller, report in reports.items():
        # TODO: shouldn't be same bins as max_sizebin from Truvari at all!

        init_d = {"count": 0, "total": 0, "mi": 0.0, "mi_pm1": 0.0, "mi_95": 0.0}

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

        for k, v in bins.items():
            if v["count"] == 0:
                continue
            count_records.append({"caller": caller, "bin": k, "y": v["count"]})
            records.append({"caller": caller, "bin": k, "measure": "mi", "y": v["mi"]})
            records.append({"caller": caller, "bin": k, "measure": "mi_pm1", "y": v["mi_pm1"]})

            # if v["mi_95"]:
            #     records.append({"caller": caller, "bin": k, "measure": "mi_95", "y": v["mi_95"]})

            if k == ">=5k":
                print(caller, v)

    df = pd.DataFrame.from_records(records)
    df_count = pd.DataFrame.from_records(count_records)

    fig = plt.figure(figsize=(15, 5))
    p = sns.color_palette([
        "#d95f02",
        "#238b45",
        "#66c2a4",
        "#386cb0",
        "#e7298a",
    ])

    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    ax2.set_ylim(0, 1000000)
    # ax2.semilogy(10)

    sns.lineplot(x="bin", y="y", data=df, style="measure", hue="caller", palette=p, ax=ax)
    bp = sns.barplot(x="bin", y="y", data=df_count, hue="caller", palette=p, ax=ax2, alpha=0.4, hue_order=callers)

    for c in bp.containers:
        bp.bar_label(c, fontsize=8, rotation=90, padding=3, color="#CCCCCC")

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    ax2.get_legend().remove()

    plt.show()


if __name__ == "__main__":
    main()
