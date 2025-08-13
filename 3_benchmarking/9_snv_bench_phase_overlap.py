#!/usr/bin/env python3

import pysam
from tqdm import tqdm


def get_sample_0_alleles(variant: pysam.VariantRecord) -> tuple[str, str] | None:
    alleles = variant.alleles
    gt = variant.samples[0].get("GT")
    if not gt:
        return None
    return tuple(alleles[g] for g in gt)


def load_benchmark_snvs() -> dict[tuple[str, int], tuple[str, ...]]:
    snvs: dict[tuple[str, int], tuple[str, ...]] = {}

    with pysam.VariantFile(f"./data/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz") as vf:
        for variant in tqdm(vf.fetch(), desc="loading benchmark SNVs"):
            alleles = variant.alleles
            if any(len(a) > 1 for a in alleles):
                continue
            gt_alleles = get_sample_0_alleles(variant)
            snvs[(variant.contig, variant.pos)] = gt_alleles

    return snvs


def main():
    # Load all benchmark SNVs
    benchmark_snvs = load_benchmark_snvs()

    for tech in ("hifi", "ont-simplex"):
        print(f"{tech=}")

        # 1. Load STRkit SNVs
        vf_snv = pysam.VariantFile(f"../2_giab_calls/out/calls/{tech}/HG002.strkit.vcf.gz")

        # 2. Iterate through STRkit SNVs and collect benchmark SNVs which match plus build STRkit SNV blocks which share
        #    a phase set, so we can look for phase flips / incorrect calls properly

        total: int = 0
        false_hets: int = 0
        correct: int = 0

        for v in tqdm(vf_snv.fetch(), desc="STRkit SNVs"):
            gt = v.samples[0].get("GT")

            if gt is None or None in gt or v.info.get("VT") != "snv":
                continue

            total += 1

            bench = benchmark_snvs.get((v.contig, v.pos))
            if not bench:
                # print("bench not found", v)
                # false_hets += 1
                continue

            gt_alleles = get_sample_0_alleles(v)

            if len(set(bench)) == 1 and len(set(gt_alleles)) == 2:
                false_hets += 1
                print(v)

        # 4. Quantify: # correct, # false hets, # flips
        #     - we only call hets
        # 5.

        # TODO
        print(f"    {total=}")
        print(f"    {false_hets=}")


if __name__ == "__main__":
    main()
