#!/bin/bash

###### rRNA

contig_filter="s\S*.ctg\S*" # for hifiasm-meta (metaFlye: "contig\S*", metaMDBG: "ctg\S*")

echo "starting ..."

for sample in ./barrnap/<tool>/*; do
	name=$(basename -- "$sample")
	echo "starting $name ..."

	# 5S
	echo "starting 5S ..."

	for bin in $sample/*.gff; do
		for i in $(egrep -o 's\S*.ctg\S*' $bin | sort | uniq); do
		        echo -e "$i \t $(grep "$i" $bin | grep -c "5S")"
		done
	done > ./rRNA_results/<tool>_"$name"_5S.txt

        # 16S
	echo "starting 16S ..."

        for bin in $sample/*.gff; do
                for i in $(egrep -o 's\S*.ctg\S*' $bin | sort | uniq); do
                        echo -e "$i \t $(grep "$i" $bin | grep -c "16S")"
                done 
        done > ./rRNA_results/<tool>_"$name"_16S.txt

        # 23S
	echo "starting 23S ..."

        for bin in $sample/*.gff; do
                for i in $(egrep -o 's\S*.ctg\S*' $bin | sort | uniq); do
                        echo -e "$i \t $(grep "$i" $bin | grep -c "23S")"
                done 
        done > ./rRNA_results/<tool>_"$name"_23S.txt
done

echo "done"



###### tRNA

contig_filter="s\S*.ctg\S*" # for hifiasm-meta (metaFlye: "contig\S*", metaMDBG: "ctg\S*")

echo "starting ..."

for sample in ./infernal/<tool>/*; do
        name=$(basename -- "$sample")
        echo "starting $name ..."

        # tRNA
        echo "starting tRNA ..."

        for bin in $sample/*.gff; do
                for i in $(egrep -o $contig_filter $bin | sort | uniq); do
                        echo -e "$i \t $(grep "$i" $bin | grep -c "tRNA")"
                done
        done > ./tRNA_results/<tool>_"$name"_tRNA.txt

done

echo "done"
