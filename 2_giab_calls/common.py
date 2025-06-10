from pathlib import Path

CALLERS = ("longtr", "straglr", "strdust", "strkit", "strkit-no-snv", "trgt")
CALLS_OUT_DIR = Path(__file__).parent / "out" / "calls"

REF = "../1_alignment/data/ref/hg38.analysisSet.fa"

TECH_HIFI = "hifi"
TECH_ONT_SIMPLEX = "ont-simplex"
TECH_ONT = "ont"
TECHS = (TECH_HIFI, TECH_ONT_SIMPLEX, TECH_ONT)

SAMPLES = ("HG002", "HG003", "HG004")
SAMPLES_BY_TECH = {
    TECH_HIFI: SAMPLES,
    TECH_ONT_SIMPLEX: SAMPLES,
    TECH_ONT: ("HG002",),
}

KARYOTYPES_BY_SAMPLE = {
    "HG002": "XY",
    "HG003": "XY",
    "HG004": "XX",
}
