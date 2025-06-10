#!/usr/bin/env python3

import pysam

from common import CALLERS, CALLS_OUT_DIR, TECHS

TOTAL_VARIANTS = 914676  # wc -l out/adotto_catalog_strkit.bed


def filter_default(v: pysam.VariantRecord) -> bool:
    gt = v.samples[0].get("GT")
    return gt is not None and None not in gt


def filter_strkit_snv(v: pysam.VariantRecord) -> bool:
    return filter_default(v) and v.info.get("VT") == "str"


def main():
    for tech in TECHS:
        for caller in CALLERS:
            f = CALLS_OUT_DIR / tech / f"HG002.{caller}.vcf.gz"

            if not f.exists():
                continue

            with pysam.VariantFile(str(f)) as vf:
                n_called = sum(
                    1 for _ in filter(filter_default if caller != "strkit" else filter_strkit_snv, vf.fetch())
                )

            print(f"{tech.rjust(4)} {caller.rjust(15)} {str(n_called).ljust(6)} {n_called / TOTAL_VARIANTS * 100:.2f}%")


if __name__ == "__main__":
    main()
