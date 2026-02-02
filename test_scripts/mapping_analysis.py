import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# total raw read number (format: <assembly_name>\t<count> )
readNumber = pd.read_csv('./readCount.tsv', sep='\t', header=None, names=['sample', 'count'])
readNumber = readNumber.set_index('sample')['count']
readNumber.loc['adhifi'] = readNumber[['ERR10905741', 'ERR10905742', 'ERR10905743']].sum()
readNumber.loc['human'] = readNumber[['SRR15275210', 'SRR15275211', 'SRR15275212', 'SRR15275213']].sum()

# quality information for MAGs without binning
quality1_df = pd.read_csv('./quality_circ-contig.csv')
quality1_df = quality1_df.dropna(axis=0)
# quality information for MAGs with binning
quality2_df = pd.read_csv('./quality_non-circ-contig.csv')
quality2_df = quality2_df.dropna(axis=0)
# combine quality information DataFrames into one
quality_df = pd.concat([quality1_df, quality2_df], ignore_index=True).drop_duplicates(subset=['assembler', 'sample', 'contig'])

# minimap2: filtered mapping DataFrame
mapping_df = pd.read_csv('./mapping.csv')
mapping_df = mapping_df.rename(columns={'tname':'contig'})

# merge quality and mapping DataFrames to get subset of both
data_df = pd.merge(mapping_df, quality_df, how = 'right', on=['contig', 'sample', 'assembler'])

# add column with specified quality information (based on paper)
conditions = [(data_df['completeness'] >= 90) & (data_df['contamination'] <= 5) & (data_df['circular/lin'] == 'circ'), (data_df['completeness'] >= 90) & (data_df['contamination'] <= 5) & (data_df['circular/lin'] == 'lin'), (data_df['completeness'] >= 70) & (data_df['contamination'] <= 10), (data_df['completeness'] >= 50) & (data_df['contamination'] <= 10)]
qualityOptions = [">1Mb near-complete circular contigs", "Near-complete non-circular MAGs", "High-quality Mags", "Medium-quality Mags"]
data_df['Quality'] = np.select(conditions, qualityOptions, default="NA")

# count total amount of reads mapped to MAGs
summary_df = data_df.groupby(['assembler', 'sample', 'Quality'])['read_count'].sum()

# get fractions by dividing with total raw read number 
fraction_mapped = summary_df.div(readNumber, axis=0, level='sample') * 100
fraction_mapped = fraction_mapped.reset_index().rename({0:'fraction'}, axis=1)
fraction_mapped = fraction_mapped.pivot(index=['assembler', 'sample'], columns='Quality', values='fraction')

# output csv file
data_df.to_csv('mappedReads_result.csv', index=False)