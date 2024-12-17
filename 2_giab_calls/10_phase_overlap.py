#!/usr/bin/env python3

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

            ps = v.samples[0].get("PS")
            if ps is None:
                continue

            if ps in phase_set_records:
                phase_set_records[ps].append(v)
            else:
                phase_set_records[ps] = [v]

        for k, vs in phase_set_records.items():
            if len(vs) <= 1:
                continue  # skip all entries with only one record, since we can't check for flips

            contig = vs[0].contig
            posns = [v.pos for v in vs]
            min_pos = min(posns)
            max_pos = max(posns)

            hp_vars = [v for v in vf_hp.fetch(contig, min_pos, max_pos) if v.samples[0].get("PS") is not None]

            print("vvvvvvvvvvvv")
            print([(v.pos, v.samples[0]["GT"], v.samples[0]["PS"]) for v in vs])
            print("---")
            print([(v.pos, v.samples[0]["GT"], v.samples[0]["PS"]) for v in hp_vars])
            print("^^^^^^^^^^^^")

            # TODO: compare to haplotype-phased.


if __name__ == "__main__":
    main()
