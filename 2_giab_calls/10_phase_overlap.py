#!/usr/bin/env python3
from collections import Counter

import pysam

SAMPLES = ("HG002", "HG003", "HG004")


def main():
    for sample in SAMPLES:
        phase_set_records: dict[int, list[pysam.VariantRecord]] = {}
        pass

        vf_snv = pysam.VariantFile(f"./out/calls/hifi/{sample}.strkit.vcf.gz")
        vf_hp = pysam.VariantFile(f"./out/calls/hifi/{sample}.strkit.phased.vcf.gz")

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
                if v.samples[0].get("PS") is not None and len(set(v.samples[0]["GT"])) > 1
            ]

            if len(hp_vars) <= 1:
                continue

            gts_snv = tuple(v.samples[0]["GT"] for v in vs)
            gts_hp = tuple(v.samples[0]["GT"] for v in hp_vars)
            gts_hp_rev = tuple(map(lambda x: x[::-1], gts_hp))

            cns_snv = tuple(v.samples[0]["MC"] for v in vs)  # TODO: use seq instead?
            cns_hp = tuple(v.samples[0]["MC"] for v in hp_vars)  # TODO: use seq instead?
            cns_hp_rev = tuple(v.samples[0]["MC"] for v in hp_vars)  # TODO: use seq instead?

            if gts_snv == gts_hp or gts_snv == gts_hp_rev or cns_snv == cns_hp or cns_snv == cns_hp_rev:
                n_flips.update((0,))
                continue

            # TODO
            n_flips.update((1,))

            # print("vvvvvvvvvvvv")
            # print([(v.pos, v.samples[0]["GT"], v.samples[0]["PS"], v.samples[0]["MC"], v.samples[0]["NSNV"]) for v in vs])
            # print("---")
            # print([(v.pos, v.samples[0]["GT"], v.samples[0]["PS"], v.samples[0]["MC"]) for v in hp_vars])
            # print("^^^^^^^^^^^^")

            # TODO: compare to haplotype-phased.

        print(sample, n_flips)


if __name__ == "__main__":
    main()
