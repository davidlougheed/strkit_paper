import pathlib

SAMPLE_KTS = {
    "bc1015": "XY",
    "bc1016": "XX",
    "bc1017": "XY",
    "bc1018": "XY",

    "bc1020": "XX",
    "bc1021": "XX",
    "bc1022": "XX",

    "bc1019": "XX",  # Weird cell line asterisk here
}

BASE_PATH = pathlib.Path(__file__).parent

REF_GENOME = str(BASE_PATH / "data" / "hs37d5.fa")


def bam(sample: str) -> str:
    return str(BASE_PATH / "data" / f"m64012_191221_044659.ccsset.{sample}--{sample}.bam")
