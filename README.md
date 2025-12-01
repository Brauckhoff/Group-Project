# Task

Reproduce analysis of the paper and compare to original paper.

# Guide

## Data

Lets focus on PacBio and if we get bored then add some OxfordNanopore...\
I would focus on the larger samples but mock is also an option - *to discuss*

| Sample    | Accessions  | Estimated time |
| --------- | ----------- | -------------- |
| [Zymo](https://s3.amazonaws.com/zymo-files/BioPool/D6331.refseq.zip)?     | SRR13128014 | ?              |
| [ATCC](https://www.atcc.org/products/msa-1003)?     | SRR11606871 | ?              |
| [human gut](https://downloads.pacbcloud.com/public/dataset/Sequel-IIe-202104/metagenomics/) | SRR15275213 | 7h   |
|           | SRR15275212 | 7h           |
|           | SRR15275211 | 6h           |
|           | SRR15275210 | 6h           |
|           | *co-assembly* | 36h        |
| [AD-HiFi](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SAMEA8949998&o=acc_s%3Aa&s=ERR10905741)   | ERR10905741 | 12h        |
|           | ERR10905742 | 13h        |
|           | ERR10905743 | 13h        |
|           | *co-assembly* | 77h      |
| Sheep rumen | SRR14289618 | 108h     |

Here is a tutorial for the [download](https://erilu.github.io/python-fastq-downloader/)... also with possible python integration :D
> we need fastq.gz file format 

Downloaded sra-toolkit and created a script to download SRR codes like described under the 'download'-link (Removed all additional options). Can be found in the data folder. Usage:\
`python3 fetch_sra_multi.py <SRR-ID1> <SRR-ID2> <...>`
> download is currently running for all mentioned accession numbers (started 01.dec 18:00)
> will be in shared folder in the next days ready to use


## Set up environment

Installation should be done in your directory (root `cd ~`). 

1. miniconda (takes ~30min)
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ~/Miniconda3-latest-Linux-x86_64.sh
```
[miniconda docs](https://www.anaconda.com/docs/getting-started/miniconda/install#macos-linux-installation) \
[manage env](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

2. Tool - [metaMDBG](https://github.com/GaetanBenoitDev/metaMDBG) 
```
conda install -c conda-forge -c bioconda metamdbg
```


# Questions

*17th Nov*:
- should we perform all analysis (some take > 30 days)? // repeat whole benchmark or only analysis with metaMDBG?\
*Answer* - no metaMDBG is fine
- only analyze PacBio or also OxfordNanopore?\
*Answer* - start with PacBio and if time left do ONT
- task: apply metaMDBG to all 5 data sets, check if we get same result?\
*Answer* - yes we do that :), but start small with 2-3 datasets if time continue

*08th Dec*:


# Timeline (in weeks)

**17th nov**
- [x] get access to the cluster (server)!

**24th nov**
- [x] lay low and learn :)

**01st dec**
- [ ] get tool installed on server
- [x] script for data download
- [ ] get data
- [ ] code should be good to go for server

**08th dec**
- [ ] NEXT MEETING :)
- [ ] do analyses and debug

**15th dec**
- [ ] post processing and analysis

**22th dec**
- [ ] continue analysis

**29th dec**
- [ ] be ready to visualize

**05th jan**
- [ ] finish practical tasks

**12th jan**
- [ ] write report 4-8 pages
- [ ] prepare presentation

**19th jan**
- [ ] finish report
- [ ] finish presentation


# Sources

Paper - https://doi.org/10.1038/s41587-023-01983-6

# Software 

- metaMDBG v0.3
- hifiasm-meta v0.2-r058
- metaflye v2.9-b1768
- minimap2 v2.21-r1071
- samtools v1.16.1
- jgi_summarize_bam_contig_depths v2
- metabat2 v2
- CheckM v1.2.1
- CheckV v1.0.1
- dRep v3.2.2
- Infernal v1.1.4
- Barrnap v0.9
- Viralverify v1.1
- wfmash v0.10.0
- R package fasttree v2.16
- R package gtdbtk v2.1.0
- R package Castor v1.7.3
- R package ggtree v2.4.1
- R package treeio v1.14.3
- R package ggtreeExtra v1.0.2\
costum Scripts:
- https://github.com/GaetanBenoitDev/metaMDBG
- https://github.com/GaetanBenoitDev/MetaMDBG_Manuscript

https://static-content.springer.com/esm/art%3A10.1038%2Fs41587-023-01983-6/MediaObjects/41587_2023_1983_MOESM1_ESM.pdf
