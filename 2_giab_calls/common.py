REF = "../1_cov_subsetting/data/ref/hg38.analysisSet.fa"

TECH_HIFI = "hifi"
TECH_ONT = "ont"
TECHS = (TECH_HIFI, TECH_ONT)

SAMPLES = ("HG002", "HG003", "HG004")
SAMPLES_BY_TECH = {
    TECH_HIFI: SAMPLES,
    TECH_ONT: ("HG002",),
}

KARYOTYPES_BY_SAMPLE = {
    "HG002": "XY",
    "HG003": "XY",
    "HG004": "XX",
}
