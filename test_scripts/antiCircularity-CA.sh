#!/bin/bash

pre="/teachstor/share/groupprojectWS25/groupC"
fastq="$pre/data/fastq"

# MDBG
echo "Starting with human-CA MDBG"
   
python3 MetaMDBG_Manuscript-main/computeMAG_binning.py $pre/assembled/non-circular_MAG/co-assembly_human $pre/assembled/co-assembly_human/contigs.fasta.gz $pre/assembled/co-assembly_human/contigs.fasta.gz mdbg 1000000 16 $fastq/SRR15275213.fastq.gz $fastq/SRR15275212.fastq.gz $fastq/SRR15275211.fastq.gz $fastq/SRR15275210.fastq.gz --circ

echo "Done with human-CA MDBG"

echo "Starting with adhifi-CA MDBG"
   
python3 MetaMDBG_Manuscript-main/computeMAG_binning.py $pre/assembled/non-circular_MAG/co-assembly_adhifi $pre/assembled/co-assembly_adhifi/contigs.fasta.gz $pre/assembled/co-assembly_adhifi/contigs.fasta.gz mdbg 1000000 16 $fastq/ERR10905741.fastq.gz $fastq/ERR10905742.fastq.gz $fastq/ERR10905743.fastq.gz --circ

echo "Done with adhifi-CA MDBG"

# -----------------------------

# FLYE   
echo "Starting with human-CA FLYE"
  
python3 MetaMDBG_Manuscript-main/computeMAG_binning.py $pre/assembled_flye/non-circular_MAG/humanGut_CA $pre/assembled_flye/humanGut_CA/assembly.fasta $pre/assembled_flye/humanGut_CA/assembly_info.txt metaflye 1000000 16 $fastq/SRR15275213.fastq.gz $fastq/SRR15275212.fastq.gz $fastq/SRR15275211.fastq.gz $fastq/SRR15275210.fastq.gz --circ
   
echo "Done with human-CA FLYE"

# -----------------------------

# HIFI
echo "Starting with human-CA HIFI"
   
python3 MetaMDBG_Manuscript-main/computeMAG_binning.py $pre/assembled_hifi/non-circular_MAG/co-assembly_human $pre/assembled_hifi/co-assembly_human/contigs.p_ctg.fasta.gz $pre/assembled_hifi/co-assembly_human/contigs.p_ctg.fasta.gz hifiasm 1000000 16 $fastq/SRR15275213.fastq.gz $fastq/SRR15275212.fastq.gz $fastq/SRR15275211.fastq.gz $fastq/SRR15275210.fastq.gz --circ
   
echo "Done with human-CA HIFI"
