# Step 1: alignment and coverage subsetting

```bash
nohup ./1_setup.bash &
sbatch ./2_combine_ont.bash
./3_align.bash
sbatch ./4_index_print_coverages.bash
```
