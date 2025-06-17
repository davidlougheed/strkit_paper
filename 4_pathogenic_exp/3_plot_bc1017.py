#!/usr/bin/env python3

import json
import matplotlib as mpl
import seaborn as sns
import seaborn.objects as so
from pandas import DataFrame
from seaborn import axes_style


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


def add_text(plot, x: int, y: int, text: str):
    return plot.add(
        so.Text(halign="right"),
        data=DataFrame.from_records([{"x": x, "y": y, "text": text}]),
        x="x", y="y", text="text"
    )


def main():
    with open("./out/bc1017.strkit.json", "r") as fh:
        bc1017 = json.load(fh)

    exp_cns = DataFrame.from_records([
        {"cn": r["cn"], "HTT STR allele": "Normal" if r["p"] == 0 else "Expansion"}
        for r in bc1017["results"][0]["reads"].values()
    ])

    plot = (
        so.Plot(exp_cns, x="cn")
        .layout(size=(6.5, 4))
        .theme({
            **axes_style("white"),
            "axes.spines.top": False,
            "axes.spines.right": False,
            **font_rc,
            "patch.linewidth": 0,
        })
        .scale(color=sns.color_palette("muted", 2))
        .add(so.Bars(edgewidth=0), so.Hist(bins=90), color="HTT STR allele")
        .add(so.Line(color="#666666"), data=DataFrame({"y": [0, 80]}).assign(x=107), x="x", y="y")
    )

    plot = add_text(plot, 107, 80, "Main expansion peak (De Luca et al.)")

    plot = plot.add(so.Line(color="#666666"), data=DataFrame({"y": [0, 95]}).assign(x=134), x="x", y="y")
    plot = add_text(plot, 134, 95, "First mosaic peak (De Luca et al.)")

    plot = plot.add(so.Line(color="#666666"), data=DataFrame({"y": [0, 110]}).assign(x=175), x="x", y="y")
    plot = add_text(plot, 175, 110, "Second mosaic peak (De Luca et al.)")

    plot = plot.label(x="CAG copy number", y="# reads")

    ptr = plot.plot()
    # noinspection PyProtectedMember
    ptr._figure.legends[0].set_bbox_to_anchor((0.8, 0.9))
    # plot.show()
    ptr.save("./out/bc1017_htt_peaks.png", dpi=300)


if __name__ == "__main__":
    main()
