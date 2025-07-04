from collections import Counter
from pysam import VariantFile

from common import CALLS_OUT_DIR, TECHS


def main():
    for tech in TECHS:
        for vp in (CALLS_OUT_DIR / tech).glob(f"*.strkit.vcf.gz"):
            # type_c = Counter()
            ps_c = Counter()
            vf = VariantFile(str(vp))
            for variant in vf:
                if variant.info["VT"] != "str":
                    continue
                s = variant.samples[0]

                ps_c.update((s["PM"],) if "PM" in s else ("not_called",))

            n_strs = ps_c.total()

            print(vp)
            for e in ps_c.items():
                print(f"    {e[0]}: {e[1] / n_strs * 100:.2f}%")
            print(f"    total snv: {(ps_c['snv'] + ps_c['snv+dist']) / n_strs * 100:.2f}%")


if __name__ == "__main__":
    main()
