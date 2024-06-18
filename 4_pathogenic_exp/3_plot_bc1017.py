#!/usr/bin/env python3

import json
import seaborn.objects as so
from pandas import DataFrame
from seaborn import axes_style


def main():
    with open("./out/bc1017.strkit.json", "r") as fh:
        bc1017 = json.load(fh)

    exp_cns = DataFrame.from_records([{"cn": r["cn"]} for r in bc1017["results"][0]["reads"].values() if r["p"] == 1])

    (
        so.Plot(exp_cns, x="cn")
        .theme({**axes_style("white"), "axes.spines.top": False, "axes.spines.right": False})
        .add(so.Bars(edgewidth=0), so.Hist())
        .add(so.Line(color="#CC00CC"), data=DataFrame({"y": [0, 50]}).assign(x=107), x="x", y="y")
        .add(so.Line(color="#CC00CC"), data=DataFrame({"y": [0, 50]}).assign(x=134), x="x", y="y")
        .add(so.Line(color="#CC00CC"), data=DataFrame({"y": [0, 50]}).assign(x=175), x="x", y="y")
        .label(x="CAG copy number", y="# reads")
        .save("./out/bc1017_htt_peaks.png")
        .show()
    )


if __name__ == "__main__":
    main()
