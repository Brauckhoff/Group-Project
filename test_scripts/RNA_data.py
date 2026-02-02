import os
import pandas as pd

### rRNA

# path to txt files
pathR = './rRNA_results/'

rRNA_list = []

# read in txt files and save in a list
for file in os.listdir(pathR):

    # get information about file for df
    f_split = file.split("_")
    assembler = f_split[0]
    sample = f_split[1]
    rRNA_size = f_split[2].split(".")[0]

    with open(os.path.join(pathR, file)) as f:
        for l in f:
            line = l.split()
            contig = line[0]
            count = int(line[1])

            # save each entry as a dictionary
            rRNA_list.append({'assembler' : assembler, 'sample' : sample, 'contig' : contig, 'rRNA' : rRNA_size, 'count' : count})

# turn list into dataframe with 5S, 16S and 23S columns
rRNA_df = pd.DataFrame(rRNA_list)
rRNA_df = rRNA_df.pivot(index=['assembler', 'sample', 'contig'], columns='rRNA', values='count').reset_index()
rRNA_df.columns.name = None


### tRNA

# path to txt files
pathT = './tRNA_results/'

tRNA_list = []

# read in txt files and save in a list
for file in os.listdir(pathT):

    # get information about file for df
    f_split = file.split("_")
    assembler = f_split[0]
    sample = f_split[1]

    with open(os.path.join(pathT, file)) as f:
        for l in f:
            line = l.split()
            contig = line[0]
            count = int(line[1])

            # save each entry as a dictionary
            tRNA_list.append({'assembler' : assembler, 'sample' : sample, 'contig' : contig, 'tRNA' : count})

# turn list into dataframe
tRNA_df = pd.DataFrame(tRNA_list)


### quality information

# path to txt files
pathI = './info_results/'

info_list = []

# read in txt files and save in a list
for file in os.listdir(pathI):

    # get information about file for df
    f_split = file.split("_")
    assembler = f_split[0]
    sample = f_split[1]

    with open(os.path.join(pathI, file)) as f:
        for l in f:
            line = l.split(",")

            contig = line[0]

            length = line[1]
            completeness = line[2]
            contamination = line[3].strip()

            # save each entry as a dictionary
            info_list.append({'assembler' : assembler, 'sample' : sample, 'contig' : contig, 'length' : length, 'completeness' : completeness, 'contamination' : contamination})

# turn list into dataframe
info_df = pd.DataFrame(info_list)

### merge all three dataframes based on assembler and contig
rnas = pd.merge(rRNA_df, tRNA_df, how='left', on=['assembler', 'sample', 'contig'])
RNA_df = pd.merge(rnas, info_df, how='left', on=['assembler', 'sample', 'contig'])

# write datafram to csv file
RNA_df.to_csv('./RNA_data.csv', index=False)