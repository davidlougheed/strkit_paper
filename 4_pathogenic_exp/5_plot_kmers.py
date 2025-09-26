import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import seaborn.objects as so
from collections import defaultdict, deque

cat_strs = "".join


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


def themed(plot_):
    return plot_.theme({
        **sns.axes_style("white"),
        "axes.spines.top": False,
        "axes.spines.bottom": False,
        "axes.spines.right": False,
        **font_rc,
        "patch.linewidth": 0,
    })


# from strkit:
def normalize_motif(normalized_motifs_cache: set, motif: str):
    motif_deque = deque(motif)

    print(normalized_motifs_cache, motif)

    for _ in range(len(motif)):
        if (c := cat_strs(motif_deque)) in normalized_motifs_cache:
            return c
        motif_deque.rotate(1)

    if len(motif) == 3 and "C" in motif:
        if motif.count("C") == 2:
            # special case: if len(motif) == 3 and we have two C, rotate until we start with two Cs
            while not (motif_deque[0] == "C" and motif_deque[1] == "C"):
                motif_deque.rotate(1)
            return cat_strs(motif_deque)
        else:
            # special case: if len(motif) == 3 and we have a C, rotate until we start with C
            while motif_deque[0] != "C":
                motif_deque.rotate(1)
            return cat_strs(motif_deque)
    else:
        for _ in range(len(motif)):
            if (c := cat_strs(motif_deque)) in normalized_motifs_cache:
                return c
            motif_deque.rotate(1)
        normalized_motifs_cache.add(motif)
        return motif


def main():
    cn_records = []
    kmer_records = []

    samples = ("1015", "1016", "1017", "1018", "1019", "1020", "1021", "1022")
    loci_names = ("HTT", "FMR1")

    normalize = True
    normalized_motifs_cache = set()

    for sample in samples:
        with open(f"./out/bc{sample}.strkit.json", "r") as fh:
            data = json.load(fh)

        for li, locus in enumerate(data["results"]):
            base = {
                "Sample": f"bc{sample}",
                "Locus": loci_names[li],
            }

            for r in locus["reads"].values():
                cn_records.append({**base, "Copy number": r["cn"]})

            kmers_dict: dict[tuple[str, str], float] = defaultdict(lambda: 0.0)
            for pi, p in enumerate(locus["peaks"]["kmers"]):
                for k, v in p.items():
                    # print("k=", k)
                    vnorm = v / (locus["peaks"]["n_reads"][pi] * (len(k) if normalize else 1))
                    kmers_dict[
                        str(pi + 1), normalize_motif(normalized_motifs_cache, k) if normalize else k
                    ] += vnorm

            # print(kmers_dict)

            for (pi, kmer), count in kmers_dict.items():
                kmer_records.append({
                    **base,
                    "Allele": "Normal" if pi == "1" else "Expanded",
                    "k-mer": kmer,
                    "Count": count,
                })

    f = plt.figure(layout="constrained", figsize=(6.5, 8))
    subfigs = f.subfigures(len(samples[5:]), 1)

    kmers_df = pd.DataFrame.from_records(kmer_records)
    for si, s in enumerate(samples[5:]):
        # for li, locus in enumerate(loci_names):
        subfigs[si].suptitle(f"bc{s} - $\\it{{FMR1}}$")
        # print(kmers_df[(kmers_df["Sample"] == f"bc{s}") & (kmers_df["Locus"] == locus)])
        kmers_plot = (
            themed(
                so.Plot(
                    kmers_df[(kmers_df["Sample"] == f"bc{s}") & (kmers_df["Locus"] == "FMR1") & (kmers_df["Count"] > 1)],
                    x="k-mer",
                    y="Count",
                )
            )
            .facet(col="Allele")
            .share(x=False)
            .add(so.Bar(), so.Dodge())
            .on(subfigs[si])
        )
        kmers_ptr = kmers_plot.plot()
        kmers_ptr._figure.axes[si * 2].xaxis.set_tick_params(rotation=90)
        kmers_ptr._figure.axes[si * 2 + 1].xaxis.set_tick_params(rotation=90)

    f.savefig("./out/fmr1_kmers.png", dpi=300)
    f.savefig("./out/Supplemental_Fig_S3.pdf", dpi=300)


if __name__ == "__main__":
    main()
