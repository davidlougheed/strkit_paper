import random
import subprocess

from pathlib import Path
from typing import Tuple

__all__ = [
    "GIAB_DIR",
    "SUBSAMP_COVS",
    "CALL_SEEDS",
    "COVS_BY_TECH",
    "SEEDS_BY_TECH",
    "REF",
    "call_script_at_covs",
]

random.seed(432)

GIAB_DIR = Path("/lustre03/project/rrg-bourqueg-ad/dlough2/workdir2022/giab/")

SUBSAMP_COVS = (60, 50, 40, 30, 25, 20, 15, 10, 8, 6, 4)
CALL_SEEDS = tuple(random.randint(0, 4069) for _ in SUBSAMP_COVS)

COVS_BY_TECH = {
    "ont-ul": (42, *SUBSAMP_COVS[2:]),
    "hifi": (53, *SUBSAMP_COVS[1:]),
    "illumina": SUBSAMP_COVS,
    "ill250": SUBSAMP_COVS,
}
SEEDS_BY_TECH = {k: CALL_SEEDS[(len(SUBSAMP_COVS)-len(v)):] for k, v in COVS_BY_TECH.items()}

REF = "/lustre03/project/rrg-bourqueg-ad/dlough2/workdir2022/ref/hg38.analysisSet.fa"


def call_script_at_covs(script: str, covs: Tuple[int, ...] = (), seeds: Tuple[int] = (), extra_env: str = ""):
    covs = covs or SUBSAMP_COVS
    seeds = seeds or CALL_SEEDS

    for cov, seed in zip(covs, seeds):
        print(f"{cov=}")
        subprocess.check_call(" ".join((
            "sbatch",
            f"--export=COV={cov},SEED={seed}{',' + extra_env if extra_env else ''}",
            script
        )), shell=True)
