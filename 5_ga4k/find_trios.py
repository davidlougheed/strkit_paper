#!/usr/bin/env python3

import json
import re
import sys

sample_pattern = re.compile(r"[a-z]{3}([0-9]{6})-0([0-9])")


def main():
    if len(sys.argv) != 2:
        print("Usage: ./find_trios.py path/to/output-trios.json", file=sys.stderr)
        exit(1)

    out_json = sys.argv[1]

    grouped_files = {}

    for line in sys.stdin:
        line = line.strip()
        s = sample_pattern.search(line)
        if not s:
            continue

        trio_id = s.group(1)
        rel = s.group(2)

        print(f"{s.group(0)}", file=sys.stderr)

        if trio_id in grouped_files:
            grouped_files[trio_id][rel] = line
        else:
            grouped_files[trio_id] = {rel: line}

    # filter final output to just complete trios
    final_trios = {
        k: {
            kk: vv
            for kk, vv in sorted(v.items(), key=lambda x: x[0])
        }
        for k, v in grouped_files.items()
        if tuple(sorted(v.keys())) == ("1", "2", "3")
    }
    print(f"found {len(final_trios)} trios", file=sys.stderr)

    with open(out_json, "w") as fh:
        json.dump(final_trios, fh)


if __name__ == "__main__":
    main()
