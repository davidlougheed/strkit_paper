#!/usr/bin/env python3

import json


SAMPLE_PREFIX = "cmh"


def main():
    with open("./data/trios.json", "r") as fh:
        trio_data: dict[str, dict[str, str]] = json.load(fh)

    for trio_id in trio_data.keys():
        with open(f"./out/mi/{SAMPLE_PREFIX}{trio_id}.json", "r") as fh:
            mi_report = json.load(fh)

        # TODO: create vcf objs

        for locus in mi_report["significant_loci"]:
            # TODO: load calls from vcf
            # TODO: edit distance filter with alleles - find most likely
            pass


if __name__ == "__main__":
    main()
