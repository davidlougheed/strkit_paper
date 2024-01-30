#!/usr/bin/env python3

import csv
import json


chr_order = (*map(lambda c: f"chr{c}", range(1, 23)), "chrX", "chrY")
print(f"chr_order={chr_order}")


def _get_non_overlapping_annos(data: list[str]) -> list[dict]:
    seen_coords: set[tuple[int, int]] = set()
    anno_final: list[dict] = []

    for anno in json.loads(data[-1]):
        coords = (int(anno["start"]), int(anno["end"]))
        overlapping: bool = False
        for sc in seen_coords:
            if coords[0] <= sc[1] and coords[1] >= sc[0]:  # overlap
                overlapping = True
        if overlapping:
            continue
        seen_coords.add(coords)
        anno_final.append(anno)

    return anno_final


def process_catalog_strkit_line(data: list[str]):
    return [[anno["chrom"], anno["start"], anno["end"], anno["motif"]] for anno in _get_non_overlapping_annos(data)]


def process_catalog_longtr_line(data: list[str]):
    return [[anno["chrom"], anno["start"], anno["end"], len(anno["motif"]), round(anno["copies"])]
            for anno in _get_non_overlapping_annos(data)]


def process_catalog_trgt_line(data: list[str]):
    return [
        [anno["chrom"], anno["start"], anno["end"], f"ID=anno{idx},MOTIFS={anno['motif']},STRUC=({anno['motif']})n"]
        for idx, anno in enumerate(_get_non_overlapping_annos(data))]


def main():
    catalog_strkit = []
    catalog_longtr = []
    catalog_trgt = []

    with open("../3_benchmarking/data/adotto_TRregions_v1.2.bed", "r") as fh:
        reader = csv.reader(fh, delimiter="\t")
        for line in reader:
            catalog_strkit.extend(process_catalog_strkit_line(line))
            catalog_longtr.extend(process_catalog_longtr_line(line))
            catalog_trgt.extend(process_catalog_trgt_line(line))

    catalog_strkit.sort(key=lambda x: (chr_order.index(x[0]), int(x[1])))
    catalog_longtr.sort(key=lambda x: (chr_order.index(x[0]), int(x[1])))
    catalog_trgt.sort(key=lambda x: (chr_order.index(x[0]), int(x[1])))

    with open("./out/adotto_catalog_strkit.bed", "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerows(catalog_strkit)

    with open("./out/adotto_catalog_longtr.bed", "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerows(catalog_longtr)

    with open("./out/adotto_catalog_trgt.bed", "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerows(catalog_trgt)


if __name__ == "__main__":
    main()
