#!/bin/bash

pre="/teachstor/share/groupprojectWS25/groupC"

for sample in $pre/<assembly_tool>/circular_contigs/*; do
    ID="$(basename -- "$sample")"
    mag="$sample/__results/mag_singleCircularContigs/__checkmCircularContigs/checkm/__checkm/bins_"
    check="$sample/__results/mag_singleCircularContigs/__checkmCircularContigs/checkm/__checkm/checkm_results.txt"

    echo "starting with $ID" >&2

    for i in $mag/*; do
        for b in $i/*.fa; do
            bin="$(basename -- "$b")"
	        Bin=${bin::-3}

            echo "starting with $Bin" >&2

            echo "get lengths" >&2
            # bioawk: to get the length of a contig
            len=$(bioawk -t -c fastx '{print $name, length($seq)}' $b)

            echo "get checkm results" >&2
            # same checkm values for all contigs in bin file
            # get completeness and contamination from checkm results
            completeness=$(grep -w "$Bin" $check | awk '{ print $13 }')
            contamination=$(grep -w "$Bin" $check | awk '{ print $14 }')

            ### write information into file
            while read -r line; do
                IFS=$'\t' read -r -a contig <<< $line

                echo "${contig[0]},${contig[1]},${completeness},${contamination}"

            done <<< $len

            echo "done with $Bin" >&2
        done
    done > ./info_results/<tool>_${ID}_info.txt

    echo "done with $ID" >&2
done