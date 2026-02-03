import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# read in results: reconstruction (us) and Benoit et al. (paper)
df_us = pd.read_csv('./RNA_data.csv')
df_paper = pd.read_csv('./paper_12.csv')

# column to filter for contigs that have expected RNA genes
df_us['isRNA'] = (df_us[['5S', '16S', '23S']] >= 1).all(axis=1) & (df_us['tRNA'] >= 18)
df_paper['isRNA'] = (df_paper[['5S', '16S', '23S']] >= 1).all(axis=1) & (df_paper['tRNA'] >= 18)

# add column with specified quality information (based on description in paper)
conditions_us = [(df_us['CheckM-completeness'] >= 90) & (df_us['CheckM-contamination'] <= 5), (df_us['CheckM-completeness'] >= 70) & (df_us['CheckM-contamination'] <= 10), (df_us['CheckM-completeness'] >= 50) & (df_us['CheckM-contamination'] <= 10)]
conditions_paper = [(df_paper['CheckM-completeness'] >= 90) & (df_paper['CheckM-contamination'] <= 5), (df_paper['CheckM-completeness'] >= 70) & (df_paper['CheckM-contamination'] <= 10), (df_paper['CheckM-completeness'] >= 50) & (df_paper['CheckM-contamination'] <= 10)]
qualityOptions = ["complete", "high", "medium"]
df_us['Quality'] = np.select(conditions_us, qualityOptions, default="NA")
df_paper['Quality'] = np.select(conditions_paper, qualityOptions, default="NA")

# get counts for total number of circular contigs and number of contigs that contain expected number of RNA genes
summary_us_total = df_us.groupby(['Software', 'Dataset', 'Quality']).size()
summary_paper_total = df_paper.groupby(['Software', 'Dataset', 'Quality']).size()
summary_us = df_us.groupby(['Software', 'Dataset', 'Quality', 'isRNA']).size()
summary_paper = df_paper.groupby(['Software', 'Dataset', 'Quality', 'isRNA']).size()

# turn groupby into DataFrame with important values
datasets_paper = ['AD-HiFi', 'Human gut', 'Sheep rumen']
software_paper = ['metaMDBG', 'hifiasm-meta', 'metaflye']
datasets_us = ['human', 'adhifi', 'ERR10905741', 'ERR10905742', 'ERR10905743', 'SRR14289618', 'SRR15275210', 'SRR15275211', 'SRR15275212', 'SRR15275213']
software_us = ['mdbg', 'hifi', 'flye']

data_df = pd.DataFrame(columns=['Source', 'Software', 'Dataset', 'isTotal', 'count'])

for tool in software_paper:
    for data in datasets_paper:
        count_total = summary_paper_total.get((tool, data, 'complete'), 0)
        count = summary_paper.get((tool, data, 'complete', True), 0)

        data_df.loc[len(data_df)] = {'Source': 'paper', 'Software' : tool, 'Dataset' : data, 'isTotal' : False, 'count' : count_total}
        data_df.loc[len(data_df)] = {'Source': 'paper', 'Software' : tool, 'Dataset' : data, 'isTotal' : True, 'count' : count}

for tool in software_us:
    for data in datasets_us:

        if (tool, data, 'complete') not in summary_us_total.index: continue

        count_total = summary_us_total.get((tool, data, 'complete'), 0)
        count = summary_us.get((tool, data, 'complete', True), 0)

        t = ""
        if tool == 'mdbg': t = 'metaMDBG'
        elif tool == 'flye': t = 'metaflye'
        elif tool == 'hifi': t = 'hifiasm-meta'

        if data == 'human': data = 'Human gut'
        if data == 'SRR14289618': data = 'Sheep rumen'
        if data == 'adhifi': data = 'AD-HiFi'

        data_df.loc[len(data_df)] = {'Source': 'us', 'Software' : t, 'Dataset' : data, 'isTotal' : False, 'count' : count_total}
        data_df.loc[len(data_df)] = {'Source': 'us', 'Software' : t, 'Dataset' : data, 'isTotal' : True, 'count' : count}

result_df = data_df.pivot_table(index=['Source', 'Software', 'Dataset'], columns='isTotal', values='count').reset_index()
result_df.columns = ['Source', 'Software', 'Dataset', 'Total_Complete', 'With_RNA']

# calculate fractions of circular contigs with RNA genes
result_df['Match_Rate'] = (result_df['With_RNA'] / result_df['Total_Complete']) * 100
