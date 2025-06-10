#!/usr/bin/env python3

import pysam
from collections import Counter

from common import TECH_HIFI, SAMPLES


def cns_to_rel(cns: tuple[int] | tuple[int, int]) -> int:
    if len(cns) == 1 or cns[0] == cns[1]:
        return 0
    return -1 if cns[0] < cns[1] else 1


def main():
    for sample in SAMPLES:
        phase_set_records: dict[int, list[pysam.VariantRecord]] = {}

        vf_snv = pysam.VariantFile(f"./out/calls/{TECH_HIFI}/{sample}.strkit.vcf.gz")
        vf_hp = pysam.VariantFile(f"./out/calls/{TECH_HIFI}/{sample}.strkit.phased.vcf.gz")

        for v in vf_snv.fetch():
            gt = v.samples[0].get("GT")
            if gt is None or None in gt or v.info.get("VT") != "str":
                continue

            if len(set(gt)) == 1:  # not informative, skip non-het loci
                continue

            # todo: skip non-het copy number or allele length loci too

            ps = v.samples[0].get("PS")
            if ps is None:
                continue

            if ps in phase_set_records:
                phase_set_records[ps].append(v)
            else:
                phase_set_records[ps] = [v]

        n_flips = Counter()

        for k, vs in phase_set_records.items():
            if len(vs) <= 1:
                continue  # skip all entries with only one record, since we can't check for flips

            contig = vs[0].contig
            posns = [v.pos for v in vs]
            min_pos = min(posns)
            max_pos = max(posns)

            hp_vars = [
                v for v in vf_hp.fetch(contig, min_pos, max_pos)
                if (
                   v.samples[0].get("PS") is not None
                   and len(set(v.samples[0]["GT"])) > 1
                   and (v.pos in posns or v.pos - 1 in posns or v.pos + 1 in posns)
                )
            ]
            hp_posns = {v.pos for v in hp_vars}

            if len(hp_vars) <= 1:
                continue

            s_vars = [v for v in vs if v.pos in hp_posns or v.pos - 1 in hp_posns or v.pos + 1 in hp_posns]

            gts_snv = tuple(v.samples[0]["GT"] for v in s_vars)
            gts_hp = tuple(v.samples[0]["GT"] for v in hp_vars)
            gts_hp_rev = tuple(map(lambda x: x[::-1], gts_hp))

            cns_snv = tuple(v.samples[0]["MC"] for v in s_vars)  # TODO: use seq instead?
            cns_hp = tuple(v.samples[0]["MC"] for v in hp_vars)  # TODO: use seq instead?
            cns_hp_rev = tuple(map(lambda x: x[::-1], cns_hp))  # TODO: use seq instead?

            if gts_snv == gts_hp or gts_snv == gts_hp_rev or cns_snv == cns_hp or cns_snv == cns_hp_rev:
                n_flips.update((0,))
                continue

            rels_snv = tuple(map(cns_to_rel, cns_snv))
            rels_hp = tuple(map(cns_to_rel, cns_hp))
            rels_hp_inv = tuple(-1 * x for x in rels_hp)

            if rels_snv == rels_hp or rels_snv == rels_hp_inv:
                n_flips.update((0,))
                continue

            n_flips.update((1,))

            print("vvvvvvvvvvvv")
            print([(v.pos, v.samples[0]["GT"], v.samples[0]["PS"], v.samples[0]["MC"], v.samples[0]["NSNV"]) for v in s_vars])
            print(rels_snv)
            print("---")
            print([(v.pos, v.samples[0]["GT"], v.samples[0]["PS"], v.samples[0]["MC"]) for v in hp_vars])
            print(rels_hp)
            print("^^^^^^^^^^^^")

            # TODO: compare to haplotype-phased.

        print(sample, n_flips, f"{n_flips[1] / n_flips.total() * 100:.2f}%")


if __name__ == "__main__":
    main()
