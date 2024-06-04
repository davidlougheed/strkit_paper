#!/usr/bin/env python3

import os
import multiprocessing as mp
import subprocess
import sys

from datetime import datetime
from pathlib import Path

from common import REF, GIAB_DIR

cov = os.environ.get("COV")
tech = os.environ.get("TECH")
seed = os.environ.get("SEED", "323")
catalog = os.environ.get("CATALOG")
snv = os.environ.get("SNV", "").lower() == "true"

if not cov:
    print("no cov", file=sys.stderr)
    exit(1)

if not tech:
    print("no tech", file=sys.stderr)
    exit(1)


def exec_strkit(bam: str, sample: str, out_dir: Path, q: mp.Queue):
    s_dir = out_dir / sample
    subprocess.call(["mkdir", "-p", s_dir])
    os.chdir(s_dir)

    start_dt = datetime.now()

    with open(f"{sample}.strkit.tsv", "w") as of:
        subprocess.check_call([
            "strkit", "call",
            "--loci", catalog,
            "--ref", REF,
            "--min-reads", "4",
            "--min-allele-reads", "2",
            "--num-bootstrap", "100",
            "--processes", "1",
            "--respect-ref",
            *(("--realign", "--hq") if tech == "hifi" else ()),
            *(("--snv", "/home/dlough2/datasets/dbsnp/00-common_all.vcf.gz") if snv else ()),
            "--seed", seed,
            "--json", f"{sample}.strkit.json",
            "--no-tsv",
            bam,
        ], stdout=of)

    end_dt = datetime.now()

    with open(f"./{sample}_exec_time.txt", "w") as fh:
        fh.write(str(end_dt - start_dt) + "\n")

    q.put(sample)


def main():
    n_tasks = int(sys.argv[1])
    process_samples(
        str(GIAB_DIR / f"giab_bams.{tech}.{cov}x.txt"),  # just hg002 for now
        str(GIAB_DIR / f"giab_samples.strkit{'_snv' if snv else ''}.{tech}.{cov}x.done"),
        GIAB_DIR / f"strkit{'_snv' if snv else ''}_{tech}_{cov}x",
        exec_strkit,
        n_tasks,
        lambda s: s.split("/")[-1].split(".")[0])


if __name__ == "__main__":
    main()
