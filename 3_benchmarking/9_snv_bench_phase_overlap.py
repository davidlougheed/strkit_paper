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

    with pysam.VariantFile(f"./data/HG002_GRCh38_1_22_v4.2.1_benchmark_hifiasm_v11_phasetransfer_passed.vcf.gz") as vf:
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

        total: int = 0  # Total common between STRkit and benchmark
        false_hets: int = 0
        flips: int = 0
        correct: int = 0

        current_ps: int = -1
        current_ps_snvs = []
        current_ps_bench_snvs = []

        for v in tqdm(vf_snv.fetch(), desc="STRkit SNVs"):
            gt = v.samples[0].get("GT")

            if gt is None or None in gt or v.info.get("VT") != "snv":
                continue

            ps = v.samples[0].get("PS")

            if ps is None:  # SNVs without phase sets (shouldn't happen, but just in case)
                continue

            if ps != current_ps:
                if (ct := len(current_ps_snvs)) > 1 and current_ps != -1:
                    total += ct

                    # Quantify: # correct, # false hets, # flips  ---  we only call hets
                    fl1 = 0
                    fl2 = 0

                    for snv, bench_snv in zip(current_ps_snvs, current_ps_bench_snvs):
                        if len(set(bench_snv)) == 1 and len(set(snv)) == 2:
                            false_hets += 1
                        elif bench_snv == snv[::-1]:
                            fl1 += 1
                        elif bench_snv == snv:
                            fl2 += 1

                    if fl1 <= fl2:  # phase sets match without a flip
                        flips += fl1
                        correct += fl2
                    else:
                        flips += fl2
                        correct += fl1

                current_ps = ps
                current_ps_snvs.clear()
                current_ps_bench_snvs.clear()

            bench = benchmark_snvs.get((v.contig, v.pos))
            if not bench:
                # print("bench not found", v)
                # false_hets += 1
                continue

            gt_alleles = get_sample_0_alleles(v)

            current_ps_snvs.append(gt_alleles)
            current_ps_bench_snvs.append(bench)

        # Final tally
        print(f"    {total=}")
        print(f"    {false_hets=} ({false_hets/total*100:.4f}%)")
        print(f"    {flips=} ({flips/total*100:.4f}%)")
        print(f"    {correct=} ({correct/total*100:.4f}%)")
        print(f"    {false_hets+flips+correct=}")


if __name__ == "__main__":
    main()
