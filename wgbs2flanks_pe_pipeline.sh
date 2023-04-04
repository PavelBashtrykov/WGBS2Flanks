#!/usr/bin/bash

################################################################################
# This script is written by Pavel Bashtrykov
# pavel.bashtrykov@ibtb.uni-stuttgart.de
# pavel.bashtrykov@gmail.com
################################################################################

SAMPLE=SRR7459034
PATH_SRA=~/HDD/ncbi/sra/
PATH_BISMARK_GENOME=~/HDD/genomes/mm10/
PATH_GENOME_FASTA=~/HDD/genomes/mm10/mm10.fa

prefetch ${SAMPLE}\
 --max-size 100GB

vdb-validate ${SAMPLE}

parallel-fastq-dump --sra-id ${PATH_SRA}${SAMPLE}.sra\
 --threads 8\
 --split-files

fastqc ${SAMPLE}_1.fastq ${SAMPLE}_2.fastq

trim_galore -j 8 --paired -q 20\
 ${SAMPLE}_1.fastq\
 ${SAMPLE}_2.fastq

fastqc ${SAMPLE}_1_val_1.fq ${SAMPLE}_2_val_2.fq

bismark --multicore 10\
 --genome ${PATH_BISMARK_GENOME}\
 -1 ${SAMPLE}_1_val_1.fq\
 -2 ${SAMPLE}_2_val_2.fq

samtools sort -m 100G -n\
 ${SAMPLE}_1_val_1_bismark_bt2_pe.bam\
 -o ${SAMPLE}_sorted.bam

deduplicate_bismark -p ${SAMPLE}_sorted.bam

bismark_methylation_extractor\
 --multicore 10 --buffer_size 100G\
 --genome_folder ${PATH_BISMARK_GENOME}\
 --no_overlap\
 --cytosine_report --CX\
 ${SAMPLE}_sorted.deduplicated.bam

python ./wgbs2bed.py\
 --infile ${SAMPLE}_sorted.deduplicated.CX_report.txt\
 --outfile ${SAMPLE}_coordinates.bed

bedtools getfasta -tab -s -name\
 -fi ${PATH_GENOME_FASTA}\
 -bed ${SAMPLE}_coordinates.bed\
 -fo ${SAMPLE}_coordinates_sequences.txt

python ./compute_flanks.py --depth 10\
 --infile ${SAMPLE}_coordinates_sequences.txt\
 --outfile ${SAMPLE}_flanks_methylation.csv
