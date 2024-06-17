#!/usr/bin/env python3

import csv
import json


chr_order = (*map(lambda c: f"chr{c}", range(1, 23)), "chrX", "chrY")
print(f"chr_order={chr_order}")

MAX_MOTIF_SIZE = 10
MIN_PURITY = 90


def _get_non_overlapping_annos(seen_coords: set[tuple[str, int, int]], data: list[str]) -> list[dict]:
    anno_final: list[dict] = []
    json_data = json.loads(data[-1])

    by_span = sorted(json_data, key=lambda k: k["end"] - k["start"], reverse=True)

    if by_span and (len(by_span[0]["motif"]) > MAX_MOTIF_SIZE):
        return anno_final  # early return if our most spanning TR is above the STR motif size range

    for anno in by_span:
        motif = anno["motif"]

        if len(motif) > MAX_MOTIF_SIZE:
            continue
        if anno["purity"] < MIN_PURITY:
            continue
        if len(set(motif)) == 1:
            # skip homopolymers
            continue

        # In the JSON, they're 1-based closed coordinates. Change to 0-based half-open:
        anno["start"] -= 1
        start = anno["start"]
        end = anno["end"]
        coords = (anno["chrom"], start, end)

        overlapping: bool = False
        for sc in seen_coords:
            if start < sc[2] and end > sc[1]:  # overlap
                overlapping = True
                break

        if overlapping:
            continue

        seen_coords.add(coords)
        anno_final.append(anno)

    return anno_final


def process_catalog_strkit_line(data: list[str]):
    seen_coords: set[tuple[str, int, int]] = set()
    return [[anno["chrom"], anno["start"], anno["end"], anno["motif"]]
            for anno in _get_non_overlapping_annos(seen_coords, data)]


def process_catalog_longtr_line(data: list[str]):
    seen_coords: set[tuple[str, int, int]] = set()
    # LongTR runs counter to the BED spec: https://github.com/gymrek-lab/LongTR/issues/5
    return [[anno["chrom"], anno["start"] + 1, anno["end"], len(anno["motif"]), round(anno["copies"])]
            for anno in _get_non_overlapping_annos(seen_coords, data)]


def process_catalog_trgt_line(data: list[str]):
    seen_coords: set[tuple[str, int, int]] = set()
    return [
        [anno["chrom"], anno["start"], anno["end"], f"ID=anno{idx};MOTIFS={anno['motif']};STRUC=({anno['motif']})n"]
        for idx, anno in enumerate(_get_non_overlapping_annos(seen_coords, data))]


def main():
    catalog_strkit = []
    catalog_longtr = []
    catalog_trgt = []

    with open("./data/adotto_TRregions_v1.2.bed", "r") as fh:
        reader = csv.reader(fh, delimiter="\t")
        for line in reader:
            catalog_strkit.extend(process_catalog_strkit_line(line))
            catalog_longtr.extend(process_catalog_longtr_line(line))
            catalog_trgt.extend(process_catalog_trgt_line(line))

    print("catalog size (strkit, longTR, TRGT):", len(catalog_strkit), len(catalog_longtr), len(catalog_trgt))

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
