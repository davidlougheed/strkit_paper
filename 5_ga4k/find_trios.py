#!/usr/bin/env python3

import json
import re
import sys

sample_pattern = re.compile(r"[a-z]{3}([0-9]{6})-0([0-9])")


def main():
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
    final_trios = {k: v for k, v in grouped_files.items() if tuple(sorted(v.keys())) == ("1", "2", "3")}
    print(f"found {len(final_trios)} trios", file=sys.stderr)

    print(json.dumps(final_trios))


if __name__ == "__main__":
    main()
