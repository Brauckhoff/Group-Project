#!/usr/bin/env python3

# Script to analyze viral contig quality from CheckV outputs
# To asses the high qulity cirular viruses, also the circular information was extracted from the assembly files


import pandas as pd
import glob
import os

def analyze_viral_files(assembler):
    '''Analyze viral contig quality from CheckV outputs for a given assembler'''
    # Initialize lists
    summary_data = []
    high_quality_list = []

    # Find all quality tsv files in the folders for each asssembler
    search_path = os.path.join("checkV", assembler, "*", "results", "quality_summary.tsv")
    files = glob.glob(search_path)

    if not files:
        print("No files found. Please check your folder path.")
        return

    # Loop through each file
    for filepath in files:
        filename = os.path.basename(filepath)
        path_parts = filepath.split(os.sep)
        sample = path_parts[-3]

        try:
            # Read file
            df = pd.read_csv(filepath, sep='\t') 
            df.columns = df.columns.str.strip()
            
            # Extract information based on quality
            high_quality = df['checkv_quality'].str.contains('High', case=False, na=False)
            medium_quality = df['checkv_quality'].str.contains('Medium', case=False, na=False)
            low_quality = df['checkv_quality'].str.contains('Low', case=False, na=False)

            # Store high quality contigs
            hq_df = df[high_quality].copy()
            for contig_id in hq_df['contig_id']:
                high_quality_list.append({
                    'assembler': assembler,
                    'sample_id': sample,
                    'contig_id': contig_id
                })

            # Store qulity values
            summary_data.append({
                'Data': sample,
                'High_Quality': high_quality.sum(),
                'Medium_Quality': medium_quality.sum(),
                'Low_Quality': low_quality.sum()
            })


        except Exception as e:
            print(f"Error processing {filename}: {e}\n")

    # Print a summary table about the qulaity and save both lists as csv
    if summary_data:
        print("=" * 60)
        print(assembler.upper() + " FINAL ANALYSIS SUMMARY")
        print("=" * 60)
        summary_df = pd.DataFrame(summary_data)
        print(summary_df.to_string(index=False))
        summary_df.to_csv("checkV/" + assembler + "_virus_quality_summary.csv", index=False)

    if high_quality_list:
        hq_df_final = pd.DataFrame(high_quality_list)
        hq_df_final.to_csv("checkV/" + assembler + "_high_quality_viral_contigs.csv", index=False)

def analyze_circular_contigs(assembler):
    '''Extract information about circularity of contigs'''
    # Initialize list
    contig_list = []

    # Find all quality tsv files in the folders depending on assembler
    if assembler == "meta":
        search_path = os.path.join("assembled", "*", "contigs.fasta")
    elif assembler == "flye":
        search_path = os.path.join("assembled_flye", "*", "assembly_info.txt")

    files = glob.glob(search_path)

    if not files:
        print("No files found. Please check your folder path.")
        return

    # Loop through each file
    for filepath in files:
        filename = os.path.basename(filepath)
        path_parts = filepath.split(os.sep)
        sample = path_parts[-2]

        try:
            # Read the file
            df = pd.read_csv(filepath, sep='\t') 
            df.columns = df.columns.str.strip()

            # Store contig info
            if assembler == "meta":
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.startswith('>'):
                            # Split header line to extract contig ID and circularity
                            parts = line.strip().split()
                            contig_id = parts[0][1:] 
                            is_circular = 'circular=yes' in line
                            
                            contig_list.append({
                                'assembler': assembler,
                                'sample_id': sample,
                                'contig_id': contig_id,
                                'circular': is_circular
                            })

            elif assembler == "flye":
                for _, row in df.iterrows():
                    contig_list.append({
                        'assembler': assembler,
                        'sample_id': sample,
                        'contig_id': row['#seq_name'],
                        'circular': row['circ.'] == 'Y' 
                    })

            print(f"Processed {sample} successfully.")


        except Exception as e:
            print(f"Error processing {filename}: {e}\n")

    # Save contig circularity information as csv
    if contig_list:
        contig_df_final = pd.DataFrame(contig_list)
        contig_df_final.to_csv("checkV/" + assembler + "_contig_info.csv", index=False)


# --- EXECUTION ---
analyze_viral_files("meta")
analyze_viral_files("hifi")
analyze_viral_files("flye")
analyze_circular_contigs("meta")
analyze_circular_contigs("flye")