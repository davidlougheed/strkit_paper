#!/usr/bin/env python3

import sys

from .common import call_script_at_covs, COVS_BY_TECH, SEEDS_BY_TECH

tech = sys.argv[2].strip()
catalog = sys.argv[3].strip()

if __name__ == "__main__":
    call_script_at_covs(
        sys.argv[1],
        covs=COVS_BY_TECH[tech],
        seeds=SEEDS_BY_TECH[tech],
        extra_env=f"TECH={tech},CATALOG={catalog},SNV=true",
    )
