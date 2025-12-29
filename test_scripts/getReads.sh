#!/bin/bash

for d in ERR* SRR*; do
   echo "Starting with $d"
   sra_toolkit/sratoolkit.3.2.1-ubuntu64/bin/fastq-dump --split-files --outdir ./reads/$d/ --gzip ./$d/$d.sra
done
