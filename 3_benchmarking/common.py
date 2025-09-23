CALLERS = ("longtr", "strdust", "strkit", "strkit-no-snv", "straglr", "trgt")

TECHS = ("hifi", "ont-simplex", "ont")
TECH_LABELS = {
    "hifi": "PacBio HiFi (32×)",
    "ont-simplex": "ONT R10 simplex (32×)",
    "ont": "ONT R10 duplex (12×)",
}

LABELS = {
    # callers:
    "longtr": "LongTR",
    "straglr": "Straglr",
    "strdust": "STRdust",
    "strkit": "STRkit",
    "strkit-no-snv": "STRkit (no SNVs)",
    "trgt": "TRGT",
    # measures:
    "F1": "F1 score",
    "PPV": "Precision (PPV)",
    "TPR": "Recall (TPR)",
}
