#!/usr/bin/env python3

import json
import re
import sys

sample_pattern = re.compile(r"[a-z]{3}([0-9]{6})-0([0-9])")


def main():
    trio_files = {}

    for line in sys.stdin:
        line = line.strip()
        s = sample_pattern.match(line)
        if not s:
            continue

        trio_id = s.group(1)
        rel = s.group(2)

        print(f"{s}", file=sys.stderr)

        if trio_id in trio_files:
            trio_files[trio_id][rel] = line
        else:
            trio_files[trio_id] = {rel: line}

    print(json.dumps(trio_files))


if __name__ == "__main__":
    main()
