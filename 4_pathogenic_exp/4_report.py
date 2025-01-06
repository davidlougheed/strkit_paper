import pysam
from pathlib import Path

OUT_PATH = Path(__file__).parent / "out"
TOOLS = ["strkit", "longtr", "straglr", "strdust", "trgt"]


def print_tool_genotypes(samples: tuple[str, ...], disease: str, var_idx: int, count_offset: int):
    print(f"{disease}")
    motif = "CAG" if disease == "HTT" else "CCG"
    for sample in samples:
        for tool in TOOLS:
            if tool != "straglr":
                path = OUT_PATH / (f"bc10{sample}.{tool}.vcf" + (".gz" if tool not in ("strkit", "strdust") else ""))
                if not path.exists():
                    print(f"Missing {path}")
                    continue

                vf = pysam.VariantFile(str(path), "r")
                variant = list(vf.fetch())[var_idx]
                vf.close()

                genotype: tuple[int, ...] = (0, 0)
                if tool in ("strkit", "trgt"):
                    genotype = tuple(map(int, variant.samples[0]["MC"]))
                elif tool == "longtr":
                    # HTT:  +1 for the CAA, which then gets subtracted off via offset (-2)
                    # FMR1: +4 for the interrupting four triplets which get subtracted off via offset (-4)
                    genotype = tuple(
                        (variant.alleles[g].count(motif) + (1 if disease == "HTT" else 4))
                        for g in variant.samples[0]["GT"]
                    )
                elif tool == "strdust":
                    # STRdust - need to get rid of the first base, plus seems to have an off-by-one error and include
                    # the last base too.
                    genotype = tuple(int(round((len(variant.alleles[g]) - 2) / 3)) for g in variant.samples[0]["GT"])

            else:
                path = OUT_PATH / f"bc10{sample}.{tool}.bed"
                if not path.exists():
                    print(f"Missing {path}")
                    continue
                with open(path, "r") as fh:
                    variant = [line.strip().split("\t") for line in fh.readlines()[1:]][var_idx]
                    a1 = int(round(float(variant[5])))
                    genotype = (a1, int(round(float(variant[8]))) if variant[8] != "-" else a1)

            # apply offset
            genotype = (genotype[0] + count_offset, genotype[1] + count_offset)

            print(f"{disease} bc10{sample} {tool}: {genotype}")

    print("")  # newline


def main():
    print_tool_genotypes(("15", "16", "17", "18", "19"), "HTT", 0, -2)
    print_tool_genotypes(("20", "21", "22", "19"), "FMR1", 1, -4)


if __name__ == "__main__":
    main()
