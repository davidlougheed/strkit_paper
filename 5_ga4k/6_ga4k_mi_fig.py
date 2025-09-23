# import altair as alt
import orjson
import os.path
# import polars as pl
import pandas as pd
import seaborn.objects as so
import sys

from scipy.stats import ttest_ind
from statistics import mean
from tqdm import tqdm

CALLERS = ("longtr", "strdust", "strkit", "strkit-no-snv", "straglr", "trgt")

LABELS = {
    # callers:
    "longtr": "LongTR",
    "straglr": "Straglr",
    "strdust": "STRdust",
    "strkit": "STRkit",
    "strkit-no-snv": "STRkit (no SNVs)",
    "trgt": "TRGT",
    # measures:
    "F1": "F1 score",
    "PPV": "Precision (PPV)",
    "TPR": "Recall (TPR)",
}

PALETTE = [
    "#d95f02",  # LongTR
    "#984ea3",  # STRdust
    "#238b45",  # STRkit
    "#66c2a4",  # STRkit (no SNVs)
    "#386cb0",  # Straglr
    "#e7298a",  # TRGT
]


def main():
    with open("./data/trios.json", "rb") as fh:
        trio_data: dict[str, dict[str, str]] = orjson.loads(fh.read())

    df_list = []

    coverages = pd.read_csv("./out/ga4k_coverages.csv")
    coverages["avg"] = coverages[["child", "p1", "p2"]].mean(axis=1)

    for caller in tqdm(CALLERS, desc="caller"):
        for trio_id in trio_data:
            cov_val = coverages[coverages["trio"] == trio_id]["avg"]
            print(f"trio coverage: {trio_id}={cov_val}")
            if cov_val >= 25:
                cov = "25-30x"
            elif cov_val >= 10:
                cov = "10-15x"
            else:
                cov = "<10x"

            path = f"./out/mi/cmh{trio_id}.{caller}.json"
            if not os.path.exists(path):
                print(f"ERROR: path does not exist: {path}", file=sys.stderr)
                continue
            with open(f"./out/mi/cmh{trio_id}.{caller}.json", "rb") as fh:
                data = orjson.loads(fh.read())
                cl = LABELS.get(caller, caller)
                df_list.extend([
                    *([
                        {"MI metric": "copy number", "MI %": data["mi"]["val"], "Caller": cl, "Coverage": cov},
                        {"MI metric": "copy number (±1)", "MI %": data["mi_pm1"]["val"], "Caller": cl, "Coverage": cov},
                    ] if caller in ("straglr", "strkit", "strkit-no-snv", "trgt") else []),
                    *([
                        {"MI metric": "sequence", "MI %": data["mi_seq"]["val"], "Caller": cl, "Coverage": cov},
                        {"MI metric": "seq. len.", "MI %": data["mi_sl"]["val"], "Caller": cl, "Coverage": cov},
                        {"MI metric": "seq. len. ±1bp", "MI %": data["mi_sl_pm1"]["val"], "Caller": cl,
                         "Coverage": cov},
                    ] if caller != "straglr" else []),
                ])

    # df = pl.from_dicts(df_list)
    df = pd.DataFrame.from_records(df_list)

    # def _df_metric_caller_mi_percent(m: str, c: str):
    #     return df.filter((pl.col("MI metric") == m) & (pl.col("Caller") == c))["MI %"].to_list()

    def _df_metric_caller_mi_percent(m: str, c: str):
        return df[(df["MI metric"] == m) & (df["Caller"] == c)]["MI %"].tolist()

    for metric in ("copy number", "copy number (±1)", "sequence", "seq. len.", "seq. len. ±1bp"):
        mis_strkit = _df_metric_caller_mi_percent(metric, "STRkit")
        mis_strkit_no_snv = _df_metric_caller_mi_percent(metric, "STRkit (no SNVs)")
        mis_trgt = _df_metric_caller_mi_percent(metric, "TRGT")

        print(f"{mis_strkit=}")
        print(f"{mis_strkit_no_snv=}")
        print(f"{mis_trgt=}")

        print(f"metric {metric}")
        print(f"    strkit mean: {mean(mis_strkit)}")
        print(f"    strkit-no-snv mean: {mean(mis_strkit_no_snv)}")
        print(f"    trgt mean: {mean(mis_trgt)}")

        print(f"    t test strkit vs trgt:        {ttest_ind(mis_trgt, mis_strkit, alternative='less').pvalue}")
        print(f"    t test strkit-no-snv vs trgt: {ttest_ind(mis_trgt, mis_strkit_no_snv, alternative='less').pvalue}")

    plot = (
        so.Plot(df, x="Caller", y="MI %", color="Caller", marker="Coverage")
        .layout(size=(9, 6))
        .add(so.Dot(), so.Jitter(0.5))
        .scale(
            color=so.Nominal({c: v for c, v in zip(CALLERS, PALETTE)}),
            marker=so.Nominal({
                "25-30x": "^",
                "10-15x": "o",
                "<10x": "v",
            }),
        )
    )

    ptr = plot.plot()
    ptr.save("./out/ga4k_mi_fig.png", dpi=300)
    ptr.save("./out/Supplemental_Fig_S2.pdf", dpi=300)

    # Altair:
    # plot = (
    #     alt.Chart(df)
    #     .mark_tick()
    #     .encode(
    #         x=alt.X("Caller").title(None),
    #         y=alt.Y("MI %", scale=alt.Scale(domain=[0.55, 1.0])),
    #         column="MI metric",
    #         color=alt.Color("Caller").scale(range=PALETTE).legend(None)
    #     )
    #     .resolve_scale(x="shared")
    # )
    # plot.save("./out/ga4k_mi_fig.png", ppi=300)
    # plot.save("./out/Supplemental_Fig_S2.pdf", ppi=300)


if __name__ == "__main__":
    main()
