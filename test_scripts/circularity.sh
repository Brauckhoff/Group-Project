#!/bin/bash

for d in assembled/ERR* assembled/SRR* assembled/co*; do
   
   contig="$d/contigs.fasta.gz"
   ID=$(basename -- "$d")
   
   echo	"Starting with $ID"
   
   python3 MetaMDBG_Manuscript-main/run_singleContigs.py /teachstor/share/groupprojectWS25/groupC/assembled/circular_contigs/$ID $contig $contig mdbg 16
   echo "Done with $ID"
done
