import altair as alt
import orjson
import os.path
import polars as pl
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

    for caller in tqdm(CALLERS, desc="caller"):
        for trio_id in trio_data:
            path = f"./out/mi/cmh{trio_id}.{caller}.json"
            if not os.path.exists(path):
                print(f"ERROR: path does not exist: {path}", file=sys.stderr)
                continue
            with open(f"./out/mi/cmh{trio_id}.{caller}.json", "rb") as fh:
                data = orjson.loads(fh.read())
                cl = LABELS.get(caller, caller)
                df_list.extend([
                    *([
                        {"MI metric": "copy number", "MI %": data["mi"]["val"], "Caller": cl},
                        {"MI metric": "copy number (±1)", "MI %": data["mi_pm1"]["val"], "Caller": cl},
                    ] if caller in ("straglr", "strkit", "strkit-no-snv", "trgt") else []),
                    *([
                        {"MI metric": "sequence", "MI %": data["mi_seq"]["val"], "Caller": cl},
                        {"MI metric": "seq. len.", "MI %": data["mi_sl"]["val"], "Caller": cl},
                        {"MI metric": "seq. len. ±1bp", "MI %": data["mi_sl_pm1"]["val"], "Caller": cl},
                    ] if caller != "straglr" else []),
                ])

    df = pl.from_dicts(df_list)

    for metric in ("copy number", "copy number (±1)", "sequence", "seq. len.", "seq. len. ±1bp"):
        mis_strkit = df.filter((pl.col("MI metric") == metric) & (pl.col("Caller") == "strkit"))["MI %"].to_list()
        mis_strkit_no_snv = df.filter(
            (pl.col("MI metric") == metric) & (pl.col("Caller") == "strkit-no-snv"))["MI %"].to_list()
        mis_trgt = df.filter((pl.col("MI metric") == metric) & (pl.col("Caller") == "trgt"))["MI %"].to_list()

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
        df.plot
        .boxplot()
        .encode(
            x=alt.X("Caller").title(None),
            y=alt.Y("MI %", scale=alt.Scale(domain=[0.55, 1.0])),
            column="MI metric",
            color=alt.Color("Caller").scale(range=PALETTE).legend(None)
        )
        .resolve_scale(x="shared")
    )
    plot.save("./out/ga4k_mi_fig.png", ppi=350)


if __name__ == "__main__":
    main()
