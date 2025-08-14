#!/usr/bin/env python3

import csv
import json


chr_order = (*map(lambda c: f"chr{c}", range(1, 23)), "chrX", "chrY")
print(f"chr_order={chr_order}")

MAX_MOTIF_SIZE = 10
# MIN_PURITY = 80


def get_minimized_motif(motif: str, p: bool = False) -> str:
    # turns e.g. TATA => TA
    motif_len = len(motif)
    for mini in range(2, motif_len // 2 + 1):
        mini_motif = motif[:mini]
        mcm = motif.count(mini_motif) * mini
        if mcm == motif_len:
            if p and mini_motif:
                print(motif, mini_motif)
            return mini_motif
    return motif


def _get_non_overlapping_annos(seen_coords: set[tuple[str, int, int]], data: list[str]) -> list[dict]:
    anno_final: list[dict] = []
    json_data = json.loads(data[-1])

    if len(json_data) > 1:
        return []

    by_span = sorted(json_data, key=lambda k: k["end"] - k["start"], reverse=True)

    if by_span and (len(get_minimized_motif(by_span[0]["motif"])) > MAX_MOTIF_SIZE):
        return anno_final  # early return if our most spanning TR is above the STR motif size range

    for anno in by_span:
        motif = get_minimized_motif(anno["motif"])

        if len(motif) > MAX_MOTIF_SIZE:
            continue

        # if anno["purity"] < MIN_PURITY:
        #     continue

        if len(set(motif)) == 1:
            # skip homopolymers
            continue

        # Update anno motif
        anno["motif"] = motif

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


def process_catalog_strkit_line(_idx: int, data: list[str]):
    seen_coords: set[tuple[str, int, int]] = set()
    return [[anno["chrom"], anno["start"], anno["end"], anno["motif"]]
            for anno in _get_non_overlapping_annos(seen_coords, data)]


def process_catalog_longtr_line(idx: int, data: list[str]):
    seen_coords: set[tuple[str, int, int]] = set()
    # LongTR runs counter to the BED spec: https://github.com/gymrek-lab/LongTR/issues/5
    return [[anno["chrom"], anno["start"] + 1, anno["end"], anno["motif"], f"LOC{idx+1}"]
            for anno in _get_non_overlapping_annos(seen_coords, data)]


def process_catalog_trgt_line(idx: int, data: list[str]):
    seen_coords: set[tuple[str, int, int]] = set()
    return [
        [anno["chrom"], anno["start"], anno["end"], f"ID=anno{idx+1};MOTIFS={anno['motif']};STRUC=({anno['motif']})n"]
        for anno in _get_non_overlapping_annos(seen_coords, data)]


def main():
    catalog_strkit = []
    catalog_longtr = []
    catalog_trgt = []

    with open("./data/adotto_TRregions_v1.2.bed", "r") as fh:
        reader = csv.reader(fh, delimiter="\t")
        for idx, line in enumerate(reader):
            catalog_strkit.extend(process_catalog_strkit_line(idx, line))
            catalog_longtr.extend(process_catalog_longtr_line(idx, line))
            catalog_trgt.extend(process_catalog_trgt_line(idx, line))

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
