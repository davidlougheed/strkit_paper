#!/bin/bash
#SBATCH --mem=12G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=6:00:00
#SBATCH --account=rrg-bourqueg-ad

module load StdEnv/2023
module load python/3.11 scipy-stack/2023b parasail/2.6.2 samtools bcftools
source ../envs/env_strkit/bin/activate

bam_tmpdir="${SLURM_TMPDIR}/reads.bam"
cp "${BAM}" "${bam_tmpdir}"
cp "${BAM}.bai" "${bam_tmpdir}.bai"

snv_vcf_tmpdir="${SLURM_TMPDIR}/snvs.vcf.gz"
cp "../2_giab_calls/data/00-common_all.vcf.gz" "${snv_vcf_tmpdir}"
cp "../2_giab_calls/data/00-common_all.vcf.gz.tbi" "${snv_vcf_tmpdir}.tbi"


# --sex-chr "${KARYOTYPE}" \

out_vcf_tmp="${SLURM_TMPDIR}/${SAMPLE}.strkit.vcf"
out_vcf_gz="./out/calls/${SAMPLE}.strkit.vcf.gz"

#/usr/bin/time -o "./out/calls/${SAMPLE}.strkit.time"
strkit call \
  --ref "${REF}" \
  --loci ../2_giab_calls/out/adotto_catalog_strkit.bed \
  --hq \
  --incorporate-snvs "${snv_vcf_tmpdir}" \
  --min-reads 2 \
  --min-allele-reads 1 \
  --vcf "${out_vcf_tmp}" \
  --no-tsv \
  --seed "${SEED}" \
  --sample-id "${SAMPLE}" \
  --processes 8 \
  --log-level info \
  "${bam_tmpdir}" || exit

bgzip -f "${out_vcf_tmp}"
tabix "${out_vcf_tmp}.gz"
chown dlough2:rrg-bourqueg-ad "${out_vcf_tmp}.gz" "${out_vcf_tmp}.gz.tbi"

mv "${out_vcf_tmp}.gz" "${out_vcf_gz}"
mv "${out_vcf_tmp}.gz.tbi" "${out_vcf_gz}.tbi"
