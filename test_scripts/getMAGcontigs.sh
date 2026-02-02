#!/bin/bash

pre="/teachstor/share/groupprojectWS25/groupC"

# get all contigs from circular_contigs (without binning) and non-circular_MAG (with binning)
for sample in $pre/<assemblies_tool>/<circular_contigs / non-circular_MAG>/*; do    # traverse all sample folders for both options
    ID="$(basename -- "$sample")"
    mag="$sample/__results/mag_singleContigs/__checkmCircularContigs/checkm/__checkm/bins_"
    check="$sample/__results/mag_singleContigs/__checkmCircularContigs/checkm/__checkm/checkm_results.txt"

    echo "starting with $ID" >&2

    for i in $mag/*; do
        for b in $i/*.fa; do
            bin="$(basename -- "$b")"
	        Bin=${bin::-3}

            echo "starting with $Bin" >&2

            # get information if MAG is circular or not
	        if [[ $bin == *"circ"* ]]; then
		        circ="circ"
	        else
		        circ="lin"
	        fi

            echo "get lengths" >&2
            # bioawk to get length of contig
            len=$(bioawk -t -c fastx '{print $name, length($seq)}' $b)

            echo "get checkm results" >&2
            # same checkm values for all contigs within a bin file
            # get completeness and contamination values for MAGs and therefore contigs within MAGs
            completeness=$(grep -w "$Bin" $check | awk '{ print $13 }')
            contamination=$(grep -w "$Bin" $check | awk '{ print $14 }')

            ### write information into file
            while read -r line; do
                IFS=$'\t' read -r -a contig <<< $line

                echo "${contig[0]},${contig[1]},${completeness},${contamination},${circ}"

            done <<< $len

            echo "done with $Bin" >&2
        done
    done > ./quality_info/hifi_${ID}_info.txt   # write information into txt file

    echo "done with $ID" >&2
done