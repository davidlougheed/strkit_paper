import altair as alt
import json
import os.path
import polars as pl
import sys

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
    # "#386cb0",  # Straglr
    "#e7298a",  # TRGT
]


def main():
    with open("./data/trios.json", "r") as fh:
        trio_data: dict[str, dict[str, str]] = json.load(fh)

    df_list = []

    for caller in tqdm(CALLERS, desc="caller"):
        for trio_id in trio_data:
            path = f"./out/mi/cmh{trio_id}.{caller}.json"
            if not os.path.exists(path):
                print(f"ERROR: path does not exist: {path}", file=sys.stderr)
                continue
            with open(f"./out/mi/cmh{trio_id}.{caller}.json", "r") as fh:
                data = json.load(fh)
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
