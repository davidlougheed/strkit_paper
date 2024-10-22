GRCH38_SIZE = sum([
    248956422,
    242193529,
    198295559,
    190214555,
    181538259,
    170805979,
    159345973,
    145138636,
    138394717,
    133797422,
    135086622,
    133275309,
    114364328,
    107043718,
    101991189,
    90338345,
    83257441,
    80373285,
    58617616,
    64444167,
    46709983,
    50818468,
    156040895,
    57227415,
])  # contig sizes

span = 0

with open("./out/adotto_catalog_strkit.bed", "r") as fh:
    for line in fh:
        data = line.strip().split("\t")
        span += int(data[2]) - int(data[1])

print(f"Bases covered: {span}; total bases: {GRCH38_SIZE}; percent: {(span / GRCH38_SIZE * 100):.2f}%")
