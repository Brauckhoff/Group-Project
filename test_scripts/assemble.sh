#!/bin/bash

SRRs=("SRR15275213 SRR15275212 SRR15275211 SRR15275210 ERR10905741 ERR10905742 ERR10905743 SRR14289618")

# iterate over individual assemblies
for i in $SRRs
do
   metaMDBG asm --out-dir ./$i/ --in-hifi /teachstor/share/groupprojectWS25/groupC/data/fastq/$i.fastq.gz --threads 16 --kmer-size 13
done

# do co-assembly for human gut
g1="/teachstor/share/groupprojectWS25/groupC/data/fastq/SRR15275213.fastq.gz"
g2="/teachstor/share/groupprojectWS25/groupC/data/fastq/SRR15275212.fastq.gz"
g3="/teachstor/share/groupprojectWS25/groupC/data/fastq/SRR15275211.fastq.gz"
g4="/teachstor/share/groupprojectWS25/groupC/data/fastq/SRR15275210.fastq.gz"

metaMDBG asm --out-dir ./co-assembly_human/ --in-hifi $g1 $g2 $g3 $g4 --threads 16 --kmer-size 13

# do co-assembly for ad-hifi
ad1="/teachstor/share/groupprojectWS25/groupC/data/fastq/ERR10905741.fastq.gz"
ad2="/teachstor/share/groupprojectWS25/groupC/data/fastq/ERR10905742.fastq.gz"
ad3="/teachstor/share/groupprojectWS25/groupC/data/fastq/ERR10905743.fastq.gz"

metaMDBG asm --out-dir ./co-assembly_human/ --in-hifi $ad1 $ad2 $ad3 --threads 16 --kmer-size 13
