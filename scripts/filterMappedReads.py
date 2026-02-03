import pandas as pd
from pathlib import Path

### filter mapped reads to get only one contig for each read

# path to mapped reads: minimap -x asm20
path = ""   # input the path to your output folder here
pathMapping = Path(path)

# output list: to store individual filtered mappings
list_mapping = []

# paf column names
colNames = ['qname', 'qlen', 'qstart', 'qend', 'strand', 'tname', 'tlen', 'tstart', 'tend', 'nmatch', 'alen', 'mapq']

# traverse directories with pathlib
for assemblerDir in pathMapping.iterdir():
    for file in assemblerDir.glob("*.paf"):

        # turn paf file into pandas dataframe
        df = pd.read_csv(file, sep="\t", header=None, usecols=range(12), names=colNames) # only use the first 12 columns of the paf files to avoid conflicts

        # filter: alignment length >= 80 % of read length
        df_80 = df[(df['alen']/df['qlen'] >= 0.8)].copy()

        # choose one contig per read (longest alignment; choose randomly if there are two contigs with the same alignment length)
        unique_mapping = (df_80.sort_values(by=['qname', 'alen'], ascending=[True, False]).drop_duplicates(subset='qname'))

        # count number of mapped reads per contig
        mapped = unique_mapping.groupby('tname').size().reset_index(name="read_count")

        # add information about assembly (needed, to later merge with quality information)
        mapped['assembler'] = assemblerDir.name
        mapped['sample'] = file.stem.split('_')[1]

        # output
        list_mapping.append(mapped)

# combine the list elements into one DataFrame
df_mapping = pd.concat(list_mapping, ignore_index=True)

# output final DataFrame of filtered mapped reads
df_mapping.to_csv('mapping.csv', index=False)