#!/bin/bash

pre="/teachstor/share/groupprojectWS25/groupC"

# MDBG
for d in assembled/ERR* assembled/SRR* assembled/co*; do
   
   contig="$d/contigs.fasta.gz"
   ID=$(basename -- "$d")
   
   echo "Starting with $ID MDBG"
   
   python3 MetaMDBG_Manuscript-main/computeMAG_binning.py $pre/assembled/non-circular_MAG/$ID $pre/$contig $pre/$contig mdbg 1000000 16 $pre/data/fastq/$ID.fastq.gz --circ

   echo "Done with $ID MDBG"
done


# FLYE
for d in assembled_flye/ERR* assembled_flye/SRR* assembled_flye/hum*; do
   
   contig="$d/assembly.fasta"
   ID=$(basename -- "$d")
   
   echo "Starting with $ID FLYE"
  
   python3 MetaMDBG_Manuscript-main/computeMAG_binning.py $pre/assembled_flye/non-circular_MAG/$ID $pre/$contig $pre/$d/assembly_info.txt metaflye 1000000 16 $pre/data/fastq/$ID.fastq.gz --circ
   
   echo "Done with $ID FLYE"
done


# HIFI
for d in assembled_hifi/ERR* assembled_hifi/SRR* assembled_hifi/*_hum*; do
   
   contig="$d/contigs.p_ctg.fasta.gz"
   ID=$(basename -- "$d")
   
   echo "Starting with $ID HIFI"
   
   python3 MetaMDBG_Manuscript-main/computeMAG_binning.py $pre/assembled_hifi/non-circular_MAG/$ID $pre/$contig $pre/$contig hifiasm 1000000 16 $pre/data/fastq/$ID.fastq.gz --circ
   
   echo "Done with $ID HIFI"
done
