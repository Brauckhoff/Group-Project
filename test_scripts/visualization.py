import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

# File path for paper figures
filepath_in = '/Users/johannaengeln/Downloads/41587_2023_1983_MOESM2_ESM.xlsx'
filepath_out = '/Users/johannaengeln/Desktop/Uni/GroupProject/graphs_paper/'

# File path for selfmade figures
filepath_in = '/Users/johannaengeln/Library/CloudStorage/OneDrive-UTCloud/GroupProject/GroupProjectSummary.xlsx'
filepath_out = '/Users/johannaengeln/Desktop/Uni/GroupProject/graphs_ours/'

# -----------------------------------------------------------------------
# Load and Clean Data of Table S3 (Running time, memory, MAG counts)
# -----------------------------------------------------------------------
df = pd.read_excel(filepath_in, sheet_name='Table S3', header=2)

# Clean column names (remove newlines like \n inside headers)
df.columns = [c.replace('\n', ' ').strip() for c in df.columns]

# Fill the column with the sample for all rows of that sample
df['Clean_Dataset'] = df['Dataset'].where(df['Assembler'] == 'metaMDBG')
df['Dataset'] = df['Clean_Dataset'].ffill()
df = df[df['Assembler'].notna()]

# Translate 'Run time (h)' to numeric hours
df['Run time (h)'] = pd.to_timedelta(df['Run time (h)'].astype(str), errors='coerce').dt.total_seconds() / 3600

# Convert these columns to numeric, turning errors (like "not possible") into NaN
metrics = [
    'Peak memory (GB)',
    '>1Mb near-complete linear contigs',
    '>1Mb Circular contigs',
    '>1Mb near-complete circular contigs',
    'Near-complete Mags',
    'High-quality Mags',
    'Medium-quality Mags'
]
for col in metrics:
    df[col] = pd.to_numeric(df[col], errors='coerce')
# Add value for Near-complete non-circular MAGS
df['Near-complete non-circular MAGs'] = df['Near-complete Mags'] - df['>1Mb near-complete circular contigs']
# Delete rows where Assembler is 'rust-mdbg'
df = df[df['Assembler'] != 'rust-mdbg']

# -----------------------------------------------------------------------
# Visualization of Run Time and Peak Memory
# -----------------------------------------------------------------------
# Set global style
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.1)
palette = {
    'metaMDBG': "#FF002B",      # Vermilion (Red-ish)
    'hifiasm-meta': "#FF9602",  # Orange (Replaces Green)
    'metaflye': "#07A8FF",      # Strong Blue
}

# Set special notations and order
double_thread_datasets = ['co-assembly', 'sheep rumen'] 
hue_order = df['Assembler'].unique()
dataset_order = df['Dataset'].unique().tolist()
sheep_label = 'Sheep rumen (SRR14289618)' 
if sheep_label in dataset_order:
    dataset_order.remove(sheep_label)
    dataset_order.append(sheep_label)

# Helper function to annotate bars with special symbols
def annotate_bars(ax, df, x_col, y_col, hue_col, hue_list, special_datasets):
    n_hues = len(hue_list)
    bar_width = 0.8 / n_hues
    x_labels = [label.get_text() for label in ax.get_xticklabels()]

    for x_i, dataset_name in enumerate(x_labels):
        is_special = any(d.lower() in dataset_name.lower() for d in special_datasets)
        
        for h_i, assembler_name in enumerate(hue_list):
            x_pos = x_i - 0.4 + (h_i * bar_width) + (bar_width / 2)
            val = df[(df[x_col] == dataset_name) & (df[hue_col] == assembler_name)][y_col]
            
            if val.empty or pd.isna(val.values[0]):
                ax.text(x_pos, 0, 'X', ha='center', va='bottom', 
                        color='#2f3542', fontsize=12, fontweight='bold')
            elif is_special:
                height = val.values[0]
                ax.text(x_pos, height, '*', ha='center', va='bottom', 
                        color='#2f3542', fontsize=15, fontweight='bold')

    # Legend
    missing_handle = mlines.Line2D([], [], color='#2f3542', marker='X', linestyle='None',
                                  markersize=8, label='Missing value')
    double_thread_handle = mlines.Line2D([], [], color='#2f3542', marker='*', linestyle='None',
                                  markersize=10, label='32 threads')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles + [missing_handle, double_thread_handle], 
              title='Assembler', bbox_to_anchor=(1.05, 1), loc='upper left')


# Plot Run Time
plt.figure(figsize=(10, 6))
ax1 = sns.barplot(
    data=df, 
    x='Dataset', 
    y='Run time (h)', 
    hue='Assembler',
    hue_order=hue_order,
    order=dataset_order, 
    palette=palette,
    edgecolor='#2f3542',
    linewidth=0.8
)

annotate_bars(ax1, df, 'Dataset', 'Run time (h)', 'Assembler', hue_order, double_thread_datasets)

plt.title('Assembly Run Time', fontweight='bold', pad=15)
plt.ylabel('Run time (Hours)', fontweight='bold')
plt.xlabel('Dataset', fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(filepath_out + 'Run_Time.png', dpi=300, bbox_inches='tight')
plt.close()


# Plot Peak Memory
plt.figure(figsize=(10, 6))
ax2 = sns.barplot(
    data=df, 
    x='Dataset', 
    y='Peak memory (GB)', 
    hue='Assembler', 
    hue_order=hue_order,
    order=dataset_order,
    palette=palette,
    edgecolor='#2f3542',
    linewidth=0.8
)

annotate_bars(ax2, df, 'Dataset', 'Peak memory (GB)', 'Assembler', hue_order, double_thread_datasets)

plt.title('Peak Memory Usage', fontweight='bold', pad=15)
plt.ylabel('Peak memory (GB)', fontweight='bold')
plt.xlabel('Dataset', fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(filepath_out + 'Memory_Usage.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# Visualization of Contig and MAG Counts paper style
# -----------------------------------------------------------------------
# Setup Data and Order
selected_samples = [
    'Human gut (co-assembly)', 
    'AD-HiFi (co-assembly)',
    'Sheep rumen (SRR14289618)', 
]
# Map your long ID names to the short clean names axis labels
name_mapping = {
    'Human gut (co-assembly)': 'Human gut',
    'AD-HiFi (co-assembly)': 'AD-HiFi',
    'Sheep rumen (SRR14289618)': 'Sheep rumen'
}
df_filtered = df[df['Dataset'].isin(selected_samples)].copy()

# Order the data like in the paper
df_filtered['Dataset'] = pd.Categorical(
    df_filtered['Dataset'], 
    categories=selected_samples, 
    ordered=True
)
df_filtered = df_filtered.sort_values(['Dataset'])

# Setup Metrics and Colors
stack_metrics = [
    '>1Mb near-complete circular contigs',
    'Near-complete non-circular MAGs',
    'High-quality Mags',
    'Medium-quality Mags'
]
df_filtered[stack_metrics] = df_filtered[stack_metrics].fillna(0)
cust_colors = ['#7CE97A', '#66B3E7', '#AFBDC7', '#C2C9CD']

# Plotting
plot_data = df_filtered.set_index(['Dataset', 'Assembler'])[stack_metrics]

ax = plot_data.plot(
    kind='bar', 
    stacked=True, 
    figsize=(10, 7), 
    edgecolor='black',
    linewidth=0.8,
    width=0.8,
    color=cust_colors
)
ax.grid(False)
# Add Numbers Inside Bars
for container in ax.containers:
    labels = [int(v) if v > 0 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='center', fontsize=10)

# Custom X-axis Labels with Grouping
# A. Set the Assembler Labels (bottom level)
assembler_labels = plot_data.index.get_level_values(1)
ax.set_xticks(range(len(assembler_labels)))
ax.set_xticklabels(assembler_labels, rotation=45, ha='right', fontsize=11)
# B. Add Dataset Group Labels (top level)
unique_datasets = plot_data.index.get_level_values(0).unique()

start_idx = 0
for dataset in unique_datasets:
    count = len(plot_data.loc[dataset])
    center_idx = start_idx + (count - 1) / 2
    
    # Get the clean short name
    clean_name = name_mapping.get(dataset, dataset)
    
    # Add the text label lower down
    ax.text(
        center_idx, -0.2, clean_name, 
        ha='center', va='top', 
        transform=ax.get_xaxis_transform(),
        fontweight='normal', fontsize=12
    )
    
    start_idx += count

ax.set_ylim(0, 800)

# Final Formatting
plt.xlabel('')
plt.ylabel('Number of MAGs', fontweight='bold', fontsize=12)
plt.title('CheckM evaluation', fontweight='bold', fontsize=14, loc='left')
legend_mapping = {
    '>1Mb near-complete circular contigs': 'Near-complete circular contigs >1Mb',
    'Near-complete non-circular MAGs':     'Near-complete non-circular MAGs',
    'High-quality Mags':                   'High-quality MAGs',
    'Medium-quality Mags':                 'Medium-quality MAGs'
}
handles, labels = ax.get_legend_handles_labels()
new_labels = [legend_mapping.get(l, l) for l in labels]
plt.legend(
    handles, new_labels, 
    bbox_to_anchor=(0.02, 0.98), loc='upper left', 
    frameon=False, fontsize=10
)
sns.despine()
plt.tight_layout()
plt.savefig(filepath_out + 'MAG_summary.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# Visualization of Ad-HiFI data
# -----------------------------------------------------------------------
# Setup Data and Order
selected_samples = [
    'AD2W1 (ERR10905741)', 
    'AD2W20 (ERR10905742)',
    'AD2W40 (ERR10905743)', 
]
# Map your long ID names to the short clean names axis labels
name_mapping = {
    'AD2W1 (ERR10905741)': 'ERR10905741',
    'AD2W20 (ERR10905742)': 'ERR10905742',
    'AD2W40 (ERR10905743)': 'ERR10905743'
}
df_filtered = df[df['Dataset'].isin(selected_samples)].copy()

# Order the data like in the paper
df_filtered['Dataset'] = pd.Categorical(
    df_filtered['Dataset'], 
    categories=selected_samples, 
    ordered=True
)
df_filtered = df_filtered.sort_values(['Dataset'])

# Setup Metrics and Colors
stack_metrics = [
    '>1Mb near-complete circular contigs',
    'Near-complete non-circular MAGs',
    'High-quality Mags',
    'Medium-quality Mags'
]
df_filtered[stack_metrics] = df_filtered[stack_metrics].fillna(0)
cust_colors = ['#7CE97A', '#66B3E7', '#AFBDC7', '#C2C9CD']

# Plotting
plot_data = df_filtered.set_index(['Dataset', 'Assembler'])[stack_metrics]

ax = plot_data.plot(
    kind='bar', 
    stacked=True, 
    figsize=(10, 7), 
    edgecolor='black',
    linewidth=0.8,
    width=0.8,
    color=cust_colors
)
ax.grid(False)
# Add Numbers Inside Bars
for container in ax.containers:
    labels = [int(v) if v > 0 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='center', fontsize=10)

# Custom X-axis Labels with Grouping
# A. Set the Assembler Labels (bottom level)
assembler_labels = plot_data.index.get_level_values(1)
ax.set_xticks(range(len(assembler_labels)))
ax.set_xticklabels(assembler_labels, rotation=45, ha='right', fontsize=11)
# B. Add Dataset Group Labels (top level)
unique_datasets = plot_data.index.get_level_values(0).unique()

start_idx = 0
for dataset in unique_datasets:
    count = len(plot_data.loc[dataset])
    center_idx = start_idx + (count - 1) / 2
    
    # Get the clean short name
    clean_name = name_mapping.get(dataset, dataset)
    
    # Add the text label lower down
    ax.text(
        center_idx, -0.2, clean_name, 
        ha='center', va='top', 
        transform=ax.get_xaxis_transform(),
        fontweight='normal', fontsize=12
    )
    
    start_idx += count

ax.set_ylim(0, 320)

# Final Formatting
plt.xlabel('')
plt.ylabel('Number of MAGs', fontweight='bold', fontsize=12)
plt.title('CheckM evaluation', fontweight='bold', fontsize=14, loc='left')
legend_mapping = {
    '>1Mb near-complete circular contigs': 'Near-complete circular contigs >1Mb',
    'Near-complete non-circular MAGs':     'Near-complete non-circular MAGs',
    'High-quality Mags':                   'High-quality MAGs',
    'Medium-quality Mags':                 'Medium-quality MAGs'
}
handles, labels = ax.get_legend_handles_labels()
new_labels = [legend_mapping.get(l, l) for l in labels]
plt.legend(
    handles, new_labels, 
    bbox_to_anchor=(0.02, 0.98), loc='upper left', 
    frameon=False, fontsize=10
)
sns.despine()
plt.tight_layout()
plt.savefig(filepath_out + 'MAG_AD-HiFi.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# Visualization of Human data
# -----------------------------------------------------------------------
# Setup Data and Order
selected_samples = [
    'HumanV2 (SRR15275210)', 
    'HumanV1 (SRR15275211)',
    'HumanO2 (SRR15275212)', 
    'HumanO1 (SRR15275213)'
]
# Map your long ID names to the short clean names axis labels
name_mapping = {
    'HumanV2 (SRR15275210)': 'SRR15275210',
    'HumanV1 (SRR15275211)': 'SRR15275211',
    'HumanO2 (SRR15275212)': 'SRR15275212',
    'HumanO1 (SRR15275213)': 'SRR15275213'
}
df_filtered = df[df['Dataset'].isin(selected_samples)].copy()

# Order the data like in the paper
df_filtered['Dataset'] = pd.Categorical(
    df_filtered['Dataset'], 
    categories=selected_samples, 
    ordered=True
)
df_filtered = df_filtered.sort_values(['Dataset'])

# Setup Metrics and Colors
stack_metrics = [
    '>1Mb near-complete circular contigs',
    'Near-complete non-circular MAGs',
    'High-quality Mags',
    'Medium-quality Mags'
]
df_filtered[stack_metrics] = df_filtered[stack_metrics].fillna(0)
cust_colors = ['#7CE97A', '#66B3E7', '#AFBDC7', '#C2C9CD']

# Plotting
plot_data = df_filtered.set_index(['Dataset', 'Assembler'])[stack_metrics]

ax = plot_data.plot(
    kind='bar', 
    stacked=True, 
    figsize=(10, 7), 
    edgecolor='black',
    linewidth=0.8,
    width=0.8,
    color=cust_colors
)
ax.grid(False)
# Add Numbers Inside Bars
for container in ax.containers:
    labels = [int(v) if v > 0 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='center', fontsize=10)

# Custom X-axis Labels with Grouping
# A. Set the Assembler Labels (bottom level)
assembler_labels = plot_data.index.get_level_values(1)
ax.set_xticks(range(len(assembler_labels)))
ax.set_xticklabels(assembler_labels, rotation=45, ha='right', fontsize=11)
# B. Add Dataset Group Labels (top level)
unique_datasets = plot_data.index.get_level_values(0).unique()

start_idx = 0
for dataset in unique_datasets:
    count = len(plot_data.loc[dataset])
    center_idx = start_idx + (count - 1) / 2
    
    # Get the clean short name
    clean_name = name_mapping.get(dataset, dataset)
    
    # Add the text label lower down
    ax.text(
        center_idx, -0.2, clean_name, 
        ha='center', va='top', 
        transform=ax.get_xaxis_transform(),
        fontweight='normal', fontsize=12
    )
    
    start_idx += count

ax.set_ylim(0, 190)

# Final Formatting
plt.xlabel('')
plt.ylabel('Number of MAGs', fontweight='bold', fontsize=12)
plt.title('CheckM evaluation', fontweight='bold', fontsize=14, loc='left')
legend_mapping = {
    '>1Mb near-complete circular contigs': 'Near-complete circular contigs >1Mb',
    'Near-complete non-circular MAGs':     'Near-complete non-circular MAGs',
    'High-quality Mags':                   'High-quality MAGs',
    'Medium-quality Mags':                 'Medium-quality MAGs'
}
handles, labels = ax.get_legend_handles_labels()
new_labels = [legend_mapping.get(l, l) for l in labels]
plt.legend(
    handles, new_labels, 
    bbox_to_anchor=(0.02, 0.98), loc='upper left', 
    frameon=False, fontsize=10
)
sns.despine()
plt.tight_layout()
plt.savefig(filepath_out + 'MAG_Human.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# Load and Clean Data of Table S4 (Mock community completeness and ANI)
# -----------------------------------------------------------------------

df_mock = pd.read_excel(filepath_in, sheet_name='Table S4', header=[3, 4])
# Correct dataset column
df_mock[('Dataset', 'Unnamed: 0_level_1')] = df_mock[('Dataset', 'Unnamed: 0_level_1')].astype(str)
mask_garbage = df_mock[('Dataset', 'Unnamed: 0_level_1')].str.contains('Gb|GB', case=False, regex=True)
df_mock.loc[mask_garbage, ('Dataset', 'Unnamed: 0_level_1')] = np.nan
df_mock[('Dataset', 'Unnamed: 0_level_1')] = df_mock[('Dataset', 'Unnamed: 0_level_1')].replace('nan', np.nan)  
df_mock[('Dataset', 'Unnamed: 0_level_1')] = df_mock[('Dataset', 'Unnamed: 0_level_1')].ffill()


# Extract data for completeness from different assemblers
complete_cols = [
    ('Dataset', 'Unnamed: 0_level_1'), 
    ('Species', 'Unnamed: 1_level_1'),      
    ('metaMDBG', 'completeness'),               
    ('hifiasm-meta', 'completeness'),
    ('metaflye', 'completeness')
]
df_complete = df_mock[complete_cols].copy()
df_complete.columns = df_complete.columns.droplevel(1)

# Extract data for ANI from different assemblers
ani_cols = [
    ('Dataset', 'Unnamed: 0_level_1'), 
    ('Species', 'Unnamed: 1_level_1'),      
    ('metaMDBG', 'ANI'),               
    ('hifiasm-meta', 'ANI'),
    ('metaflye', 'ANI')
]
df_ani = df_mock[ani_cols].copy()
df_ani.columns = df_ani.columns.droplevel(1)

# Prepare data to numeric
numeric_cols = ['metaMDBG', 'hifiasm-meta', 'metaflye']
for col in numeric_cols:
    df_complete[col] = pd.to_numeric(df_complete[col], errors='coerce').fillna(0)
    df_ani[col] = pd.to_numeric(df_ani[col], errors='coerce').fillna(0)

# Filter for the Zymo dataset
df_complete_zymo = df_complete[df_complete['Dataset'].str.contains('Zymo', case=False)].copy()
df_ani_zymo = df_ani[df_ani['Dataset'].str.contains('Zymo', case=False)].copy()

# Reshape data for plotting
df_complete_long = df_complete_zymo.melt(
    id_vars=['Dataset', 'Species'], 
    value_name='Completeness', 
    var_name='Assembler'
)
df_ani_long = df_ani_zymo.melt(
    id_vars=['Dataset', 'Species'], 
    value_name='ANI', 
    var_name='Assembler'
)

# -----------------------------------------------------------------------
# Plotting Completeness for Zymo Dataset
# -----------------------------------------------------------------------

# Set Global Style
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.1)
palette = {
    'metaMDBG': "#FF002B",      
    'hifiasm-meta': "#FF9602",  
    'metaflye': "#07A8FF",      
}
hue_order = ['metaMDBG', 'hifiasm-meta', 'metaflye']

# Plot
plt.figure(figsize=(12, 6))
ax1 = sns.barplot(
    data=df_complete_long,               # Use the new 'long' dataframe
    x='Species',                # Changed to 'Species' (see note below)
    y='Completeness', 
    hue='Assembler',
    hue_order=hue_order,
    palette=palette,
    edgecolor='#2f3542',
    linewidth=0.8
)

# Formatting
plt.title('Completeness of Zymo Dataset', fontweight='bold', pad=15)
plt.ylabel('Completeness', fontweight='bold')
plt.xlabel('') # Remove X label as species names are self-explanatory
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0) # Move legend outside
plt.tight_layout()
plt.savefig(filepath_out + 'Mock_Completeness_summary.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# Plotting ANI for Zymo Dataset
# -----------------------------------------------------------------------
# Plot
plt.figure(figsize=(12, 6))
ax1 = sns.barplot(
    data=df_ani_long,               # Use the new 'long' dataframe
    x='Species',                # Changed to 'Species' (see note below)
    y='ANI', 
    hue='Assembler',
    hue_order=hue_order,
    palette=palette,
    edgecolor='#2f3542',
    linewidth=0.8
)

# Formatting
plt.title('Average nucleotide identity of Zymo Dataset', fontweight='bold', pad=15)
plt.ylabel('ANI', fontweight='bold')
plt.xlabel('') # Remove X label as species names are self-explanatory
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0) # Move legend outside
plt.tight_layout()
plt.savefig(filepath_out + 'Mock_ANI_summary.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# ZOOM-IN: Plotting Completeness for Escherichia Species Only
# -----------------------------------------------------------------------

# Filter the "long" dataframe for Escherichia species
df_escherichia = df_complete_long[df_complete_long['Species'].str.contains('Escherichia', case=False)].copy()

# Plot
plt.figure(figsize=(8, 6))
ax_zoom = sns.barplot(
    data=df_escherichia,
    x='Species',
    y='Completeness',
    hue='Assembler',
    hue_order=hue_order,
    palette=palette,
    edgecolor='#2f3542',
    linewidth=0.8
)

# Formatting
plt.title('Completeness Zymo Dataset: Escherichia Strains', fontweight='bold', pad=15)
plt.ylabel('Completeness', fontweight='bold')
plt.xlabel('') 
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.savefig(filepath_out + 'Mock_Completeness_Escherichia.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# Load and Clean Data of Table S7 (Virus and Plasmids)
# -----------------------------------------------------------------------

df_viral = pd.read_excel(filepath_in, sheet_name='Table S7', header=2)

# Clean column names (remove newlines like \n inside headers)
df_viral.columns = [c.replace('\n', ' ').strip() for c in df_viral.columns]
df_viral['Dataset'] = df_viral['Dataset'].ffill()
df_viral = df_viral[df_viral['Software'].notna()]

# -----------------------------------------------------------------------
# Visualization of Virus and Plasmids all samples
# -----------------------------------------------------------------------
selected_samples_viral = [
    'Human gut (co-assembly)', 
    'AD-HiFi (co-assembly)',
    'Sheep rumen (SRR14289618)', 
]
name_mapping_viral = {
    'Human gut (co-assembly)': 'Human gut',
    'AD-HiFi (co-assembly)': 'AD-HiFi',
    'Sheep rumen (SRR14289618)': 'Sheep rumen'
}
df_viral_filtered = df_viral[df_viral['Dataset'].isin(selected_samples_viral)].copy()

# Enforce strict order
df_viral_filtered['Dataset'] = pd.Categorical(
    df_viral_filtered['Dataset'], 
    categories=selected_samples_viral, 
    ordered=True
)
df_viral_filtered = df_viral_filtered.sort_values(['Dataset'])
stack_metrics_viral = [
    'Plasmids',
    'Circular Plasmids',
    'Virus',
    'Circular Virus'
]
for col in stack_metrics_viral:
    df_viral_filtered[col] = pd.to_numeric(df_viral_filtered[col], errors='coerce').fillna(0)

# Colors: Orange/Blue theme (Color Blind Friendly)
cust_colors_viral = ['#07A8FF', '#66B3E7', '#FF9602', '#EBCA49']

# Plotting
plot_data_viral = df_viral_filtered.set_index(['Dataset', 'Software'])[stack_metrics_viral]
ax = plot_data_viral.plot(  
    kind='bar', 
    stacked=True, 
    figsize=(10, 7), 
    edgecolor='black',
    linewidth=0.8,
    width=0.8,
    color=cust_colors_viral
)
ax.grid(False)
# Add numbers inside bars
for container in ax.containers:
    labels = [int(v) if v > 0 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='center', fontsize=10)

# Custom X-axis Labels with Grouping
# A. Set the Tick Labels to be just the Assembler names
assembler_labels = plot_data_viral.index.get_level_values(1)
ax.set_xticks(range(len(assembler_labels)))
ax.set_xticklabels(assembler_labels, rotation=45, ha='right', fontsize=11)
# B. Add the Group Labels (Dataset names) below
unique_datasets = plot_data_viral.index.get_level_values(0).unique()

start_idx = 0
for dataset in unique_datasets:
    count = len(plot_data_viral.loc[dataset])
    center_idx = start_idx + (count - 1) / 2
    
    # Get the clean short name
    clean_name = name_mapping_viral.get(dataset, dataset)
    
    # Add the text label lower down
    ax.text(
        center_idx, -0.2, clean_name, 
        ha='center', va='top', 
        transform=ax.get_xaxis_transform(),
        fontweight='normal', fontsize=12
    )
    
    start_idx += count

# Final Formatting
plt.xlabel('') # Remove the default X label
plt.ylabel('Amount', fontweight='bold', fontsize=12)
plt.title("Number of plasmids and virus", fontweight='bold', fontsize=14, loc='left')
handles, labels = ax.get_legend_handles_labels()
plt.legend(
    handles, labels, 
    bbox_to_anchor=(0.02, 0.98), loc='upper left', 
    frameon=False, fontsize=10
)

# Remove top and right spines for a cleaner scientific look (like the screenshot)
sns.despine()
plt.tight_layout()
plt.savefig(filepath_out + 'Viruses_summary.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# Visualization of Virus and Plasmids AD-Hifi only
# -----------------------------------------------------------------------
selected_samples_viral = [
    'AD2W1',
    'AD2W20',
    'AD2W40', 
]
name_mapping_viral = {
    'AD2W1': 'ERR10905741',
    'AD2W20': 'ERR10905742',
    'AD2W40': 'ERR10905743'
}
df_viral_filtered = df_viral[df_viral['Dataset'].isin(selected_samples_viral)].copy()

# Enforce strict order
df_viral_filtered['Dataset'] = pd.Categorical(
    df_viral_filtered['Dataset'], 
    categories=selected_samples_viral, 
    ordered=True
)
df_viral_filtered = df_viral_filtered.sort_values(['Dataset'])
stack_metrics_viral = [
    'Plasmids',
    'Circular Plasmids',
    'Virus',
    'Circular Virus'
]
for col in stack_metrics_viral:
    df_viral_filtered[col] = pd.to_numeric(df_viral_filtered[col], errors='coerce').fillna(0)

# Colors: Orange/Blue theme (Color Blind Friendly)
cust_colors_viral = ['#07A8FF', '#66B3E7', '#FF9602', '#EBCA49']

# Plotting
plot_data_viral = df_viral_filtered.set_index(['Dataset', 'Software'])[stack_metrics_viral]
ax = plot_data_viral.plot(  
    kind='bar', 
    stacked=True, 
    figsize=(10, 7), 
    edgecolor='black',
    linewidth=0.8,
    width=0.8,
    color=cust_colors_viral
)
ax.grid(False)
# Add numbers inside bars
for container in ax.containers:
    labels = [int(v) if v > 0 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='center', fontsize=10)

# Custom X-axis Labels with Grouping
# A. Set the Tick Labels to be just the Assembler names
assembler_labels = plot_data_viral.index.get_level_values(1)
ax.set_xticks(range(len(assembler_labels)))
ax.set_xticklabels(assembler_labels, rotation=45, ha='right', fontsize=11)
# B. Add the Group Labels (Dataset names) below
unique_datasets = plot_data_viral.index.get_level_values(0).unique()

start_idx = 0
for dataset in unique_datasets:
    count = len(plot_data_viral.loc[dataset])
    center_idx = start_idx + (count - 1) / 2
    
    # Get the clean short name
    clean_name = name_mapping_viral.get(dataset, dataset)
    
    # Add the text label lower down
    ax.text(
        center_idx, -0.2, clean_name, 
        ha='center', va='top', 
        transform=ax.get_xaxis_transform(),
        fontweight='normal', fontsize=12
    )
    
    start_idx += count

# Final Formatting
plt.xlabel('') # Remove the default X label
plt.ylabel('Amount', fontweight='bold', fontsize=12)
plt.title("Number of plasmids and virus", fontweight='bold', fontsize=14, loc='left')
handles, labels = ax.get_legend_handles_labels()
plt.legend(
    handles, labels, 
    bbox_to_anchor=(0.02, 0.98), loc='upper left', 
    frameon=False, fontsize=10
)

# Remove top and right spines for a cleaner scientific look (like the screenshot)
sns.despine()
plt.tight_layout()
plt.savefig(filepath_out + 'Viruses_AD-Hifi.png', dpi=300, bbox_inches='tight')
plt.close()

# -----------------------------------------------------------------------
# Visualization of Virus and Plasmids Human only
# -----------------------------------------------------------------------
selected_samples_viral = [
    'HumanV2 (SRR15275210)', 
    'HumanV1 (SRR15275211)',
    'HumanO2 (SRR15275212)', 
    'HumanO1 (SRR15275213)'
]
name_mapping_viral = {
    'HumanV2 (SRR15275210)': 'SRR15275210',
    'HumanV1 (SRR15275211)': 'SRR15275211',
    'HumanO2 (SRR15275212)': 'SRR15275212', 
    'HumanO1 (SRR15275213)': 'SRR15275213'
}
df_viral_filtered = df_viral[df_viral['Dataset'].isin(selected_samples_viral)].copy()

# Enforce strict order
df_viral_filtered['Dataset'] = pd.Categorical(
    df_viral_filtered['Dataset'], 
    categories=selected_samples_viral, 
    ordered=True
)
df_viral_filtered = df_viral_filtered.sort_values(['Dataset'])
stack_metrics_viral = [
    'Plasmids',
    'Circular Plasmids',
    'Virus',
    'Circular Virus'
]
for col in stack_metrics_viral:
    df_viral_filtered[col] = pd.to_numeric(df_viral_filtered[col], errors='coerce').fillna(0)

# Colors: Orange/Blue theme (Color Blind Friendly)
cust_colors_viral = ['#07A8FF', '#66B3E7', '#FF9602', '#EBCA49']

# Plotting
plot_data_viral = df_viral_filtered.set_index(['Dataset', 'Software'])[stack_metrics_viral]
ax = plot_data_viral.plot(  
    kind='bar', 
    stacked=True, 
    figsize=(10, 7), 
    edgecolor='black',
    linewidth=0.8,
    width=0.8,
    color=cust_colors_viral
)
ax.grid(False)
# Add numbers inside bars
for container in ax.containers:
    labels = [int(v) if v > 0 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='center', fontsize=10)

# Custom X-axis Labels with Grouping
# A. Set the Tick Labels to be just the Assembler names
assembler_labels = plot_data_viral.index.get_level_values(1)
ax.set_xticks(range(len(assembler_labels)))
ax.set_xticklabels(assembler_labels, rotation=45, ha='right', fontsize=11)
# B. Add the Group Labels (Dataset names) below
unique_datasets = plot_data_viral.index.get_level_values(0).unique()

start_idx = 0
for dataset in unique_datasets:
    count = len(plot_data_viral.loc[dataset])
    center_idx = start_idx + (count - 1) / 2
    
    # Get the clean short name
    clean_name = name_mapping_viral.get(dataset, dataset)
    
    # Add the text label lower down
    ax.text(
        center_idx, -0.2, clean_name, 
        ha='center', va='top', 
        transform=ax.get_xaxis_transform(),
        fontweight='normal', fontsize=12
    )
    
    start_idx += count

# Final Formatting
plt.xlabel('') # Remove the default X label
plt.ylabel('Amount', fontweight='bold', fontsize=12)
plt.title("Number of plasmids and virus", fontweight='bold', fontsize=14, loc='left')
handles, labels = ax.get_legend_handles_labels()
plt.legend(
    handles, labels, 
    bbox_to_anchor=(0.02, 0.98), loc='upper left', 
    frameon=False, fontsize=10
)

# Remove top and right spines for a cleaner scientific look (like the screenshot)
sns.despine()
plt.tight_layout()
plt.savefig(filepath_out + 'Viruses_Human.png', dpi=300, bbox_inches='tight')
plt.close()