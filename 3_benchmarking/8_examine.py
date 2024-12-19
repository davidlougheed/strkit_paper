import pandas as pd
import pysam


# req: gunzip -c data/HG002_GRCh38_TandemRepeats_v1.0.bed.gz > data/HG002_GRCh38_TandemRepeats_v1.0.bed


# begin: (c) Adam English - see https://github.com/ACEnglish/laytr and https://github.com/ACEnglish/laytr/LICENSE

regions = pd.read_csv("./out/hg002_benchmark/hifi/strkit/refine.regions.txt", sep="\t")
bed = pd.read_csv(
    "./data/HG002_GRCh38_TandemRepeats_v1.0.bed",
    sep="\t",
    names=["chrom", "start", "end", "tier", "replicates", "var_flag", "entropy", "ad1", "ad2"]
)

data = regions.join(bed)

# end

print(data)


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
