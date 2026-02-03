#!/bin/bash

for d in ERR* SRR* *_hum*; do

   echo "Starting with $d"

   awk '/^S/{print ">"$2;print $3}' $d/asm.p_ctg.gfa | gzip > $d/contigs.p_ctg.fasta.gz

   echo "Done with $d"
done

