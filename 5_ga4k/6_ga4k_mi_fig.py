import json
import polars as pl

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


def main():
    with open("./data/trios.json", "r") as fh:
        trio_data: dict[str, dict[str, str]] = json.load(fh)

    df_list = []

    for caller in CALLERS:
        for trio_id in trio_data:
            with open(f"./out/mi/cmh{trio_id}.{caller}.json", "r") as fh:
                data = json.load(fh)
                cl = LABELS.get(caller, caller)
                df_list.extend([
                    {"MI metric": "copy number", "MI %": data["mi"]["val"], "Caller": cl},
                    {"MI metric": "copy number (±1)", "MI %": data["mi_pm1"]["val"], "Caller": cl},
                    {"MI metric": "sequence", "MI %": data["mi_seq"]["val"], "Caller": cl},
                    {"MI metric": "seq. len.", "MI %": data["mi_sl"]["val"], "Caller": cl},
                    {"MI metric": "seq. len. ±1bp", "MI %": data["mi_sl_pm1"]["val"], "Caller": cl},
                ])

    df = pl.from_dicts(df_list)

    plot = df.plot.mark_boxplot().encode(x="Caller", y="MI %", row="MI metric")
    plot.save("./out/ga4k_mi_fig.png", ppi=350)


if __name__ == "__main__":
    main()
