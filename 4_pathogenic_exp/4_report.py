import pysam
from pathlib import Path

OUT_PATH = Path(__file__).parent / "out"
TOOLS = ["strkit", "longtr", "straglr", "strdust", "trgt"]


def print_tool_genotypes(samples: tuple[str, ...], disease: str, var_idx: int, count_offset: int):
    print(f"{disease}")
    for sample in samples:
        for tool in TOOLS:
            path = OUT_PATH / (f"bc10{sample}.{tool}.vcf" + (".gz" if tool != "strkit" else ""))
            if not path.exists():
                print(f"Missing {path}")
                continue

            vf = pysam.VariantFile(str(path), "r")
            variant = list(vf.fetch())[var_idx]
            vf.close()

            genotype: tuple[int, ...] = (0, 0)
            if tool in ("strkit", "trgt"):
                genotype = variant.samples[0]["MC"]
            elif tool == "longtr":
                genotype = tuple(int(round((len(variant.alleles[g]) - 1) / 3)) for g in variant.samples[0]["GT"])
            # else: TODO

            print(genotype)

            # apply offset
            genotype = (genotype[0] - count_offset, genotype[1] - count_offset)

            print(f"{disease} bc10{sample} {tool}: {genotype}")

    print("")  # newline


def main():
    print_tool_genotypes(("15", "16", "17", "18", "19"), "HTT", 0, -2)
    print_tool_genotypes(("20", "21", "22", "19"), "FMR1", 1, -4)


if __name__ == "__main__":
    main()
