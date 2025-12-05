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
> fastq for all accession numbers are in shared folder ready to use

take a look at [screen](https://www.geeksforgeeks.org/linux-unix/screen-command-in-linux-with-examples/) to run things in background

## Set up environment

Installation should be done in your directory (root `cd ~`). 

<details>
  
<summary>1. <b>miniconda</b> (takes ~30min)</summary>

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ~/Miniconda3-latest-Linux-x86_64.sh
```
[miniconda docs](https://www.anaconda.com/docs/getting-started/miniconda/install#macos-linux-installation) \
[manage env](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) 

In case the init is also missing, (no (base) at beginning of line), after restart run:
```
source miniconda3/bin/activate
conda init --all
source ~/.bashrc 
```

</details>

<details>

<summary>2. <b>Tool</b> - 
<a href="https://github.com/GaetanBenoitDev/metaMDBG">metaMDBG</a></summary>

```
conda install -c conda-forge -c bioconda metamdbg
```

</details>

<details>

<summary>3. <b>most other packages</b> </summary>

[minimap2](https://github.com/lh3/minimap2)
```
conda install bioconda::minimap2
```
[metabat2](https://bioconda.github.io/recipes/metabat2/README.html)
```
conda install bioconda::metabat2
```
CheckM got a newer version with differing methods, its recommended to try both so we'll do :) (took a while) \
[old CheckM](https://github.com/Ecogenomics/CheckM) \
[new CheckM2](https://github.com/chklovski/CheckM2)
```
conda install bioconda::checkm-genome bioconda::checkm2
```
[viralverify](https://github.com/ablab/viralVerify)
```
conda install bioconda::viralverify
```
[checkv](https://pypi.org/project/checkv/)
```
conda install -c conda-forge -c bioconda checkv
```
[barrnap](https://github.com/tseemann/barrnap)
```
conda install -c bioconda -c conda-forge barrnap
```
[infernal](https://github.com/EddyRivasLab/infernal)
```
conda install -c bioconda infernal 
```
[wfmash](https://anaconda.org/channels/bioconda/packages/wfmash/overview)
```
conda install -c bioconda -c conda-forge wfmash
```

</details>

## Next steps

<details>

<summary>1. <b>avengers assemble</b></summary>

do assemble for all metagenomes + co-assemblies \
command they used:
```
metaMDBG asm outputDir reads -t 16 -l 13 -d 0.005
```

**current version adaptation**:
> adapt [threads](https://orinoco.cs.uni-tuebingen.de/what-we-do.html) (nog has max 96 ; collins has max 48) \
> -l might be string mimial size \
> -d might be string density \
> -l flag is deprecated couldnt really find anything based on the allowed options:
```
 Basic options:
    --out-dir               Output dir for contigs and temporary files
    --in-hifi               PacBio HiFi read filename(s) (separated by space)
    --in-ont                Nanopore R10.4+ read filename(s) (separated by space)
    --threads               Number of cores [1]

  Assembly options:
    --kmer-size             k-mer size [15]
    --density-assembly      Fraction of total k-mers used for assembly [0.005]
    --max-k                 Stop assembly after k iterations [0]
    --min-abundance         Minimum abundance for k-min-mers (default = rescue mode) [0]
    --all-assembly-graph    Generate assembly graph at each multi-k iteration (higher disk usage)

  Correction options:
    --min-read-quality      Minimum read average quality [0]
    --density-correction    Fraction of total k-mers used for correction [0.025]
    --min-read-identity     Min read identity [0.96]
    --min-read-overlap      Min read overlap length [1000]
    --skip-correction       Skip read correction

```
I would guess -l is kmer size and -d might be density assembly, but as they used 0.005 and its the default lets leave it here:
```
metaMDBG asm --out-dir ./<SRR-ID>/ --in-hifi <path-to-fastq.gz> --threads 32 --kmer-size 13
```
build test:
```
metaMDBG asm --out-dir ./SRR13128014/ --in-hifi /teachstor/share/groupprojectWS25/groupC/data/fastq/SRR13128014.fastq.gz --threads 50 --kmer-size 13
```
- [x] does run? yes, it does \
note: starts immediately start screen! \
Output for SRR13128014 (can be accessed vie log file)
```
        Run time:                   2h 12min 22sec
        Peak memory:                2.47982 GB
        Assembly length:            72004130
        Contigs N50:                1894056
        Nb contigs:                 580
        Nb Contigs (>1Mb):          12
        Nb circular contigs (>1Mb): 10

```
wrote a script that could run all (small modification needed)

for co-assembly just write the fastq.gz after one another: `<fastq1> <fastq2> <...>`

</details>

*coming soon*

useful insight into further steps of [analysis](https://github.com/GaetanBenoitDev/MetaMDBG_Manuscript)

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
- [x] get tool installed on server
- [x] script for data download
- [x] get data
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
