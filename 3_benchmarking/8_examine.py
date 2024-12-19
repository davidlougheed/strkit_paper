import pandas as pd
import pysam
import sys


# req: gunzip -c data/HG002_GRCh38_TandemRepeats_v1.0.bed.gz > data/HG002_GRCh38_TandemRepeats_v1.0.bed


# begin: (c) Adam English - see https://github.com/ACEnglish/laytr and https://github.com/ACEnglish/laytr/LICENSE ======

SZBINS = ['SNP', '[1,5)', '[5,10)', '[10,15)', '[15,20)', '[20,30)', '[30,40)',
          '[40,50)', '[50,100)', '[100,200)', '[200,300)', '[300,400)',
          '[400,600)', '[600,800)', '[800,1k)', '[1k,2.5k)', '[2.5k,5k)', '>=5k']
SZBINMAX = [1, 5, 10, 15, 20, 30, 40, 50, 100, 200,
            300, 400, 600, 800, 1000, 2500, 5000, sys.maxsize]


def get_sizebin(sz: int):
    """
    Bin a given size into :data:`truvari.SZBINS`

    :param sz: SVLEN to bin into the SZBINS

    :return: SZBIN
    :rtype: string
    """
    sz = abs(sz)
    for key, maxval in zip(SZBINS, SZBINMAX):
        if sz < maxval:
            return key
    return None


def get_maxadbin(x):
    sz = max(abs(x['ad1']), abs(x['ad2']))
    return get_sizebin(sz)


regions = pd.read_csv("./out/hg002_benchmark/hifi/strkit/refine.regions.txt", sep="\t")
regions.set_index(["chrom", "start", "end"], inplace=True)
print("Loaded refine.regions.txt")

bed = pd.read_csv(
    "./data/HG002_GRCh38_TandemRepeats_v1.0.bed",
    sep="\t",
    names=["chrom", "start", "end", "tier", "replicates", "var_flag", "entropy", "ad1", "ad2"]
)
bed.set_index(["chrom", "start", "end"], inplace=True)
print("Loaded HG002_GRCh38_TandemRepeats_v1.0.bed")

data = regions.join(bed)
print("Joined")

data["mx_szbin"] = data.apply(get_maxadbin, axis=1)

# end ==================================================================================================================

print(data[(data["mx_szbin"] == "[300,400)") & (data["state"] == "FN")].to_string())


# with open("./data/HG002_GRCh38_TandemRepeats_v1.0.bed", "r") as bf, open("./out/300_400_subset.bed", "w") as of:
#     for line in bf:
#         data = line.strip().split("\t")
#         val = max(abs(int(data[-2])), abs(int(data[-1])))
#         if 300 <= val < 400:
#             of.write(line)


# vf = pysam.VariantFile("./out/hg002_benchmark/hifi/strkit/fn.vcf.gz")
#
#
# for variant in vf.fetch():
#     sd = variant.info["SizeDiff"]
#     if sd is None:
#         continue
#     sdi = abs(int(sd))
#     if 300 <= sdi < 400:
#         print(variant, end="")

# with open("./out/hg002_benchmark/hifi/strkit/refine.regions.txt", "r") as fh:
#     next(fh)
#     for line in fh:
#         data = line.strip().split("\t")
#         size = int(data[2]) - int(data[1])
#         if 200 <= size < 300 and data[-1] == "FN":
#             print(line)
