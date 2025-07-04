#!/usr/bin/env python3

import re

from common import TECHS, CALLS_OUT_DIR

ELAPSED_PATTERN = re.compile(r"((?:\d{1,2}:)?\d{1,2}:\d{2})(?:\.\d{2})?elapsed")

CALLERS_CORES = {
    "longtr": 1,
    "straglr": 8,
    "strdust": 8,
    "strkit": 8,
    "strkit-no-snv": 8,
    "trgt": 8,
}


def parse_time(time_file: str, cores: int) -> float:
    time_match = ELAPSED_PATTERN.search(time_file)
    if not time_match:
        return -1.0  # invalid
    time_str = time_match[1]
    time_parts = time_str.split(":")
    if len(time_parts) == 2:
        time_seconds = int(time_parts[0]) * 60 + int(time_parts[1])
    elif len(time_parts) == 3:
        time_seconds = int(time_parts[0]) * 3600 + int(time_parts[0]) * 60 + int(time_parts[1])
    else:
        raise NotImplementedError("time_parts must be mm:ss or [h]h:mm:ss")

    return time_seconds * cores


def main():
    for tech in TECHS:
        for caller, cores in CALLERS_CORES.items():
            for time_file in sorted((CALLS_OUT_DIR / tech).glob(f"HG00?.{caller}.time")):
                with open(time_file, "r") as fh:
                    elapsed_seconds = parse_time(fh.read(), cores)
                print(f"{time_file}: {elapsed_seconds}s {elapsed_seconds / 60:.1f}mins")


if __name__ == "__main__":
    main()
