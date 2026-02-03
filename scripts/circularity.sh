#!/bin/bash

for d in assembled_hifi/ERR* assembled_hifi/SRR* assembled_hifi/*_hum*; do
   
   # MDBG: for d in assembled/ERR* assembled/SRR* assembled/co*; do
   # FLYE: for d in assembled_flye/ERR* assembled_flye/SRR* assembled_flye/hum*; do
   
   # MDBG: contig="$d/contigs.fasta.gz"
   # FLYE: contig="$d/assembly.fasta"
   # HIFI: 
   contig="$d/contigs.p_ctg.fasta.gz"
   ID=$(basename -- "$d")
   
   echo "Starting with $ID"
   
   # MDBG
   #python3 MetaMDBG_Manuscript-main/run_singleContigs.py /teachstor/share/groupprojectWS25/groupC/assembled/circular_contigs/$ID /teachstor/share/groupprojectWS25/groupC/$contig /teachstor/share/groupprojectWS25/groupC/$contig mdbg 16
   
   # FLYE
   #python3 MetaMDBG_Manuscript-main/run_singleContigs.py /teachstor/share/groupprojectWS25/groupC/assembled_flye/circular_contigs/$ID /teachstor/share/groupprojectWS25/groupC/$contig /teachstor/share/groupprojectWS25/groupC/$d/assembly_info.txt metaflye 16
   
   # HIFI
   python3 MetaMDBG_Manuscript-main/run_singleContigs.py /teachstor/share/groupprojectWS25/groupC/assembled_hifi/circular_contigs/$ID /teachstor/share/groupprojectWS25/groupC/$contig /teachstor/share/groupprojectWS25/groupC/$contig hifiasm 16
   
   echo "Done with $ID"
done

