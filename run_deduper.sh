#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --output=dedup%j.out
#SBATCH --error=dedup%j.err
#SBATCH --time=10:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=16GB
#SBATCH --job-name=dedup

/usr/bin/time -v python Balakrishnan_deduper.py -u STL96.txt -f /gpfs/projects/bgmp/diyab/bioinfo/Bi624/Deduper-diyab3/C1_SE_uniqAlign_sorted.sam \
-o /projects/bgmp/diyab/bioinfo/Bi624/Deduper-diyab3/C1_SE_uniqAlign_sorted_deduped.sam