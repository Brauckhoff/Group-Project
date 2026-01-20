# Task

Reproduce analysis of the paper and compare to original paper.

# Guide

## Data

Lets focus on PacBio and if we get bored then add some OxfordNanopore...\
I would focus on the larger samples but mock is also an option - *to discuss*

| Sample    | Accessions  | Estimated time | Run time for us| used threads | peak memory |
| --------- | ----------- | -------------- |----------------|--------------|-------------|
| [Zymo](https://s3.amazonaws.com/zymo-files/BioPool/D6331.refseq.zip)?     | SRR13128014 | ? | 2h12min   | 50 | 2.5GB|
| [ATCC](https://www.atcc.org/products/msa-1003)?     | SRR11606871 | ?              |6h45min| 20 | 3.6GB |
| [human gut](https://downloads.pacbcloud.com/public/dataset/Sequel-IIe-202104/metagenomics/) | SRR15275213 | 7h   | 6h2min | 16 | 11.8GB |
|           | SRR15275212 | 7h           | 4h55min | 16 | 11.6GB |
|           | SRR15275211 | 6h           | 5h45min | 16 | 11.3GB |
|           | SRR15275210 | 6h           | 5h20min | 16 | 11.3GB |
|           | *co-assembly* | 36h        | 14h33min | 32 | 14.3GB |
| [AD-HiFi](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SAMEA8949998&o=acc_s%3Aa&s=ERR10905741)   | ERR10905741 | 12h        | 11h14min | 16 | 10.9GB |
|           | ERR10905742 | 13h        | 11h20min | 16 | 11GB |
|           | ERR10905743 | 13h        | 13h47min | 16 | 12.6GB |
|           | *co-assembly* | 77h      | 27h31min | 32 | 13.4GB |
| Sheep rumen | SRR14289618 | 108h     | 39h27min | 32 | 13.7GB |

Here is a tutorial for the [download](https://erilu.github.io/python-fastq-downloader/)... also with possible python integration :D
> we need fastq.gz file format 

Downloaded sra-toolkit (v3.2.1-ubuntu64) and created a script to download SRR codes like described under the 'download'-link (Removed all additional options). Can be found in the data folder. Usage:\
`python3 fetch_sra_multi.py <SRR-ID1> <SRR-ID2> <...>`
> fastq for all accession numbers are in shared folder ready to use

take a look at [screen](https://www.geeksforgeeks.org/linux-unix/screen-command-in-linux-with-examples/) to run things in background \
[server docs](https://orinoco.cs.uni-tuebingen.de/what-we-do.html)

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
[CheckM](https://github.com/Ecogenomics/CheckM) \
```
conda install bioconda::checkm-genome
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

For the binning after the assembly also samtools is needed, I had problem installing it and created a new enviroment like this
```
conda create -n gp \
  -c conda-forge \
  -c bioconda \
  python=3.10 \
  samtools \
  pysam \
  metamdbg
```

</details>

## Next steps

<details>

<summary>1. <b>avengers assemble</b></summary>

# MetaMDBG - v1.2

do assemble for all metagenomes + co-assemblies \
command they used:
```
metaMDBG asm outputDir reads -t 16 -l 13 -d 0.005
```

**current version adaptation**:
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
metaMDBG asm --out-dir ./<SRR-ID>/ --in-hifi <path-to-fastq.gz> --threads 16 --kmer-size 13
```
build test:
```
metaMDBG asm --out-dir ./SRR13128014/ --in-hifi /teachstor/share/groupprojectWS25/groupC/data/fastq/SRR13128014.fastq.gz --threads 16 --kmer-size 13
```
- [x] does run? yes, it does \

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
> created `assembly.sh` ; and needed to rerun for SRR14289618 cause of path issues (`assembly2.sh`)

for co-assembly just write the fastq.gz after one another: `<fastq1> <fastq2> <...>`


# MetaFlye

command used: 
```
/usr/bin/time -v -o ./assembled_flye/times/SRR15275212.log flye --pacbio-hifi ./data/fastq/SRR15275212.fastq.gz --out-dir ./assembled_flye/SRR15275212/ --threads 16 --plasmids --meta
```
- --plasmid not available anymore


# hifiasm-meta

Create enviroment: I let run one command after the other
```
conda create -n hifiasm-meta-new -c bioconda -c conda-forge   samtools   minimap2   pigz   -y
conda activate hifiasm-meta-new
conda install bioconda::hifiasm_meta
```

In case we are interested in the version: ha base version: 0.13-r308  
hamt version: 0.3-r079

Command used: 
```
/usr/bin/time -v hifiasm_meta -t 16 -o assembled_hifi/SRR15275210/asm data/fastq/SRR15275210.fastq.gz
```
For the co-assembly we just gave the command multiple files. 

```
/usr/bin/time -v hifiasm_meta -t 32 -o assembled_hifi/co-assembly_human/asm data/fastq/SRR15275210.fastq.gz data/fastq/SRR15275211.fastq.gz data/fastq/SRR15275212.fastq.gz data/fastq/SRR15275213.fastq.gz
```

</details>

<details>

<summary>2. <b>analysis</b></summary>

# Analysis with MetaMDBG_Manuscript

python script that combines mapping, binning and checkM of assembled data

clone git repository:
```
git clone https://github.com/GaetanBenoitDev/MetaMDBG_Manuscript.git
```

create conda environment with necessary tools:
- python v3.8
- minimap v2.21 / v.2.24
- samtools v1.16.1
- metabat2 v2
- checkm v1.2.1 (data for checkm is actually installed with checkm so it should be fine by default)

```
conda create -n manuscript \
  -c conda-forge -c bioconda \
  python=3.8 \
  metabat2=2 \
  checkm-genome=1.2.1 \
  minimap2=2.21 \
  samtools=1.16.1 \
  wfmash=0.10.0 \
  biopython \
  pyani
```

useful insight into further steps of [analysis](https://github.com/GaetanBenoitDev/MetaMDBG_Manuscript)

### Step 1

<details>
<summary> <b>Assess circular contigs</b></summary>

  ```
  MetaMDBG:
  python3 ./run_singleContigs.py outputDir contigs.fasta.gz contigs.fasta.gz mdbg nbCores

  Hifiasm_meta:
  python3 ./run_singleContigs.py outputDir contigs.fasta.gz contigs.fasta.gz hifiasm nbCores

  Metaflye:
  python3 ./run_singleContigs.py outputDir contigs.fasta.gz assembly_info.txt metaflye nbCores
  ```
bash script of our used version - `circularity.sh` 

> fixed wrong referencing of circularity for mdbg in their scripts: \
> countCircularContigs.py & computeMAG_singleContigs.py \
> changed the included countHicanu() function into countMDBG()

<br>

extract the fasta from the produced graph in [hiafiams](https://hifiasm.readthedocs.io/en/latest/faq.html) (*see script getFasta.sh*)

```
awk '/^S/{print ">"$2;print $3}' SRR15275213/asm.p_ctg.gfa | gzip > SRR15275213/contigs.p_ctg.fasta.gz
```

</details>

### Step 2

<details>
<summary> <b>Assess non-circular MAGs (binning)</b></summary>

```
MetaMDBG:
python3 ./computeMAG_binning.py outputDir contigs.fasta.gz contigs.fasta.gz mdbg minCircularContigLength nbCores reads_1.fastq.gz reads_2.fastq.gz... --circ

Hifiasm_meta:
python3 ./computeMAG_binning.py outputDir contigs.fasta.gz contigs.fasta.gz hifiasm minCircularContigLength nbCores reads_1.fastq.gz reads_2.fastq.gz... --circ

Metaflye:
python3 ./computeMAG_binning.py outputDir contigs.fasta.gz assembly_info.txt metaflye minCircularContigLength nbCores reads_1.fastq.gz reads_2.fastq.gz... --circ
```

bash script used is `antiCircularity.sh` and `antiCircularity-CA.sh` \
(note multiple fastq can be targeted with e.g. $fastq/SRR15*)

<br>

> `_computeMAG_binning_extractCircularBin.py` was updated for mdbg in the same manner as mentioned before to extract circularity characteristic; \
> needed to command out deletion of temp files for adhifi co-assembly on mdbg

</details>

### Step 3

<details>
<summary> <b>Assess assembly completeness</b></summary>

```
python3 ./computeReferenceCompleteness.py referenceFile contigs.fasta.gz contigs.fasta.gz mdbg tmpDir 0.99 nbCores
```

needed to update several aspects and functional script used is called `debugCompleteness.py` 

- removed 'conda -n pyani' as this specifies the environment 
- skipped files added to reference that are of size 0 from wfmash
- changed openAni function to correct if statement that takes only first element of header and compares it to mapped contigs
- note: metaflye assembly.fasta needs to be compressed with gzip

<br>

referenceFile creation after downloading mock reference from [X](https://s3.amazonaws.com/zymo-files/BioPool/D6331.refseq.zip)
```
find references/mock_genomes/zymo/D6331.refseq -type f -iname "*.fasta" > ./references/mock_genomes/zymo/referenceFile.txt
```
- needed to change some filenames as they contained space, which caused errors
- corrected fasta format in: ssrRNAs/Bifidobacterium_adolescentis_16S.fasta
- rename ssrRNA of Prevotella_corporis to Prevotella_corporis_16S otherwise overwrite with genome seq


</details>

</details>

## Identify plasmids and viruses

<details>
<summary> <b>ViralVerify and checkV</b></summary>

To identify plasmids and viruses viralVerify and checkV was used. 
For both tools the versions from the paper were used.  
For viralVerify the basic enviroment of metaMDBG was just extended by using: 
```
conda install bioconda::viralverify
```
This automatically installed the version 1.1 which is the one required from the paper. 

Create enviroment with the correct versions for checkV (here a separate enviroment was necessary to adapt the python version): 
```
conda create -n checkv_env python=3.10
conda activate checkv_env
conda install -c conda-forge -c bioconda checkv=1.0.1
```

Download the necessary databases: 

```
viralverify download-db /teachstor/share/groupprojectWS25/groupC/references/viralV
```
```
checkv download_database /teachstor/share/groupprojectWS25/groupC/references/checkv_db
```

Unfortunately it is not very clear from the paper on which files the identification of viruses and plasmids were run. We first used the binned files, which were the outputs of metaBat2 form the metaMDBG manuscripts (to assess all binned files a script was used), but the results were far away from the results of the paper. Thus, we decided to use the assembled fasta files. 
For metaMDBG and hifiasm-meta the fasta files were unzipped and than used. Here is a list of the files used from each assembler:

```
/teachstor/share/groupprojectWS25/groupC/assembled/<SAMPLE_ID>/contigs.fasta
/teachstor/share/groupprojectWS25/groupC/assembled_flye/<SAMPLE_ID>/assembly.fasta
/teachstor/share/groupprojectWS25/groupC/assembled_hifi/<SAMPLE_ID>/contigs.p_ctg.fasta
```

The command of viralVerify was further used as stated in the paper: 
```
viralverify -f <INPUT_FILE> -o <OUTPUT_FOLDER> --hmm references/viralV/nbc_hmms.hmm -t 16 --thr 5
```
For example: 
```
viralverify -f /teachstor/share/groupprojectWS25/groupC/assembled_flye/ERR10905741/assembly.fasta -o viralverify/flye/ERR10905741_flye --hmm references/viralV/nbc_hmms.hmm -t 16 --thr 5
```

After running these files we used checkV to asses the quality. 
Here we used a small script attached to this GitHub repository. 
```
 ./checkV_analysis.sh <SAMPLE_ID> <ASSEMBLER>
```
For example
```
 ./checkV_analysis.sh ERR10905741 flye
```



</details>

## RNA analysis with Barrnap and Infernal

<details>
<summary> <b>Barrnap and Infernal</b></summary>
  
environment with correct versions:
```
conda create -n envRNAnalysis infernal=1.1.4 barrnap=0.9 -c bioconda -c conda-forge
```

rna_analysis.sh: *work in progress*
- runs both infernal and barrnap for all mag files and all tools

### Infernal
- tRNA

Database Rfam:
```
wget ftp://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.cm.gz
gunzip Rfam.cm.gz
wget ftp://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.clanin
mcpress Rfam.cm
```

code from paper:
```
cmscan --cpu 16 --cut_ga --rfam --nohmmonly --fmt 2 --tblout outputFilename --clanin Rfam.clanin Rfam.cm magFilename
```
-`--cpu <n>`: number of parallel CPU workers to use for multithreads
- `--cut_ga`: use CM's GA gathering cutoffs as reporting thresholds
- `--rfam`: set heuristic filters at Rfam-level (fast)
- `--nohmmonly`: never run HMM-only mode, not even for models with 0 basepairs
- `--fmt <n>`: set hit table format to \<n\>  (1\<=n\<=2)
- `--tblout <f>`: save parseable table of hits to file \<s\>
- `--clanin <f>`: read clan information from file \<f\>

### Barrnap
- rRNA

code from paper:
```
barrnap --threads 16 --evalue 0.01 magFilename > outputFilename
```
- `--threads [N]`: Number of threads/cores/CPUs to use (default '1')
- `--evalue [n.n]`: Similarity e-value cut-off (default '1e-06')

</details>


# Questions/Meetings

*17th Nov*:
- should we perform all analysis (some take > 30 days)? // repeat whole benchmark or only analysis with metaMDBG?\
*Answer* - no metaMDBG is fine
- only analyze PacBio or also OxfordNanopore?\
*Answer* - start with PacBio and if time left do ONT
- task: apply metaMDBG to all 5 data sets, check if we get same result?\
*Answer* - yes we do that :), but start small with 2-3 datasets if time continue

*08th Dec*:
- Update what we have done: assembly for all data sets are running, one run interrupted with out an error message (run again)
- Plan to check first parts of analysis for next week

*15th Dec*:
- Confirm how do we analyse the sample, check if we are on the right track?
- ask, if we have to "determine the fraction of reads" and "estimate contig coverage across samples before binning" (p.10/1387, last paragraph)
- Ask about single and co-assembly anaysis


# Timeline (in weeks)

**17th nov**
- [x] get access to the cluster (server)!

**24th nov**
- [x] lay low and learn :)

**01st dec**
- [x] get tool installed on server
- [x] script for data download
- [x] get data
- [x] code should be good to go for server

**08th dec**
- [x] NEXT MEETING :)
- [x] do analyses and debug

**15th dec**
- [x] post processing and analysis

**22th dec**
- [x] continue analysis

**29th dec**
- [x] ...

**05th jan**
- [ ] debug and run analysis (*ongoing*)

**12th jan**
- [ ] finish practical tasks
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

<details>
<summary>Old stuff</summary>

# Binning of the assembled data

Run minimap 2 in combination with samtools

The original command from the paper with minimap version v2.21-r1071
```
‘minimap2 -ak19 -w10 -I10G -g5k -r2k –lj-min-ratio 0.5 -A2 -B5 -O5,56 -E4,1 -z400,50 ∣ samtools sort -o outut.bam’
```

We have version 2.28-r1209
<details>
<summary> <b>Usage of minimap2</b></summary>

```
Usage: minimap2 [options] <target.fa>|<target.idx> [query.fa] [...]
Options:
  Indexing:
    -H           use homopolymer-compressed k-mer (preferrable for PacBio)
    -k INT       k-mer size (no larger than 28) [15]
    -w INT       minimizer window size [10]
    -I NUM       split index for every ~NUM input bases [8G]
    -d FILE      dump index to FILE []
  Mapping:
    -f FLOAT     filter out top FLOAT fraction of repetitive minimizers [0.0002]
    -g NUM       stop chain enlongation if there are no minimizers in INT-bp [5000]
    -G NUM       max intron length (effective with -xsplice; changing -r) [200k]
    -F NUM       max fragment length (effective with -xsr or in the fragment mode) [800]
    -r NUM[,NUM] chaining/alignment bandwidth and long-join bandwidth [500,20000]
    -n INT       minimal number of minimizers on a chain [3]
    -m INT       minimal chaining score (matching bases minus log gap penalty) [40]
    -X           skip self and dual mappings (for the all-vs-all mode)
    -p FLOAT     min secondary-to-primary score ratio [0.8]
    -N INT       retain at most INT secondary alignments [5]
  Alignment:
    -A INT       matching score [2]
    -B INT       mismatch penalty (larger value for lower divergence) [4]
    -O INT[,INT] gap open penalty [4,24]
    -E INT[,INT] gap extension penalty; a k-long gap costs min{O1+k*E1,O2+k*E2} [2,1]
    -z INT[,INT] Z-drop score and inversion Z-drop score [400,200]
    -s INT       minimal peak DP alignment score [80]
    -u CHAR      how to find GT-AG. f:transcript strand, b:both strands, n:don't match GT-AG [n]
    -J INT       splice mode. 0: original minimap2 model; 1: miniprot model [1]
  Input/Output:
    -a           output in the SAM format (PAF by default)
    -o FILE      output alignments to FILE [stdout]
    -L           write CIGAR with >65535 ops at the CG tag
    -R STR       SAM read group line in a format like '@RG\tID:foo\tSM:bar' []
    -c           output CIGAR in PAF
    --cs[=STR]   output the cs tag; STR is 'short' (if absent) or 'long' [none]
    --ds         output the ds tag, which is an extension to cs
    --MD         output the MD tag
    --eqx        write =/X CIGAR operators
    -Y           use soft clipping for supplementary alignments
    -t INT       number of threads [3]
    -K NUM       minibatch size for mapping [500M]
    --version    show version number
  Preset:
    -x STR       preset (always applied before other options; see minimap2.1 for details) []
                 - lr:hq - accurate long reads (error rate <1%) against a reference genome
                 - splice/splice:hq - spliced alignment for long reads/accurate long reads
                 - asm5/asm10/asm20 - asm-to-ref mapping, for ~0.1/1/5% sequence divergence
                 - sr - short reads against a reference
                 - map-pb/map-hifi/map-ont/map-iclr - CLR/HiFi/Nanopore/ICLR vs reference mapping
                 - ava-pb/ava-ont - PacBio CLR/Nanopore read overlap

See `man ./minimap2.1' for detailed description of these and other advanced command-line options.  
```
</details>

As some options do not exist anymore or do not work, sofar this command was used to run it:

```
minimap2 -t 16   -a -k 19 -w 10 -I 10G -g 5000  -A 2 -B 5 -O 5,56 -E 4,1 -z 400,50   assembled/ERR10905741/contigs.fasta.gz data/fastq/ERR10905741.fastq.gz | samtools sort -@ 16 -o metaBat2/ERR10905741/ERR10905741.bam
```

This was the print out: 
```
[M::main] Version: 2.28-r1209
[M::main] CMD: minimap2 -t 16 -a -k 19 -w 10 -I 10G -g 5000 -A 2 -B 5 -O 5,56 -E 4,1 -z 400,50 assembled/ERR10905741/contigs.fasta.gz data/fastq/ERR10905741.fastq.gz
[M::main] Real time: 3259.649 sec; CPU: 49281.376 sec; Peak RSS: 15.327 GB
[bam_sort_core] merging from 5 files and 16 in-memory blocks...
```

environment with minimap2 v2.21-r1071 + samtools v1.16.1
```
conda create -n envMinimap --no-channel-priority -c bioconda -c conda-forge minimap2=2.21 samtools=1.16.1
```
- `--no-channel-priority`: ensures the right dependencies can be installed after setting `conda config --set channel_priority strict` (maybe not necessary if this wasn't done)
- `minimap2=2.21` results in v2.21-r1071

running minimap2 and samtools with older versions:
```
minimap2 -t 16 -ak19 -w10 -I10G -g5k -r2k --lj-min-ratio 0.5 -A2 -B5 -O5,56 -E4,1 -z400,50 contigs reads | samtools sort -@ 16 -o align.bam
```
- `--lj-min-ratio` has been deprecated

environment with metaBAT2 v2
```
conda create -n envMetaBat2 -c bioconda -c conda-forge metabat2=2
```
- results in version 2.15

Coninued with generating the depth file with ``` jgi_summarize_bam_contig_depths ``` from metaBat2
<details>
<summary> <b>Usage of jgi_summarize_bam_contig_depths</b></summary>

```
Usage: jgi_summarize_bam_contig_depths <options> sortedBam1 [ sortedBam2 ...]
where options include:
        --outputDepth       arg  The file to put the contig by bam depth matrix (default: STDOUT)
        --percentIdentity   arg  The minimum end-to-end % identity of qualifying reads (default: 97)
        --pairedContigs     arg  The file to output the sparse matrix of contigs which paired reads span (default: none)
        --unmappedFastq     arg  The prefix to output unmapped reads from each bam file suffixed by 'bamfile.bam.fastq.gz'
        --noIntraDepthVariance   Do not include variance from mean depth along the contig
        --showDepth              Output a .depth file per bam for each contig base
        --minMapQual        arg  The minimum mapping quality necessary to count the read as mapped (default: 0)
        --weightMapQual     arg  Weight per-base depth based on the MQ of the read (i.e uniqueness) (default: 0.0 (disabled))
        --includeEdgeBases       When calculating depth & variance, include the 1-readlength edges (off by default)
        --maxEdgeBases           When calculating depth & variance, and not --includeEdgeBases, the maximum length (default:75)
        --referenceFasta    arg  The reference file.  (It must be the same fasta that bams used)

Options that require a --referenceFasta
        --outputGC          arg  The file to print the gc coverage histogram
        --gcWindow          arg  The sliding window size for GC calculations
        --outputReadStats   arg  The file to print the per read statistics
        --outputKmers       arg  The file to print the perfect kmer counts

Options to control shredding contigs that are under represented by the reads
        --shredLength       arg  The maximum length of the shreds
        --shredDepth        arg  The depth to generate overlapping shreds
        --minContigLength   arg  The mimimum length of contig to include for mapping and shredding
        --minContigDepth    arg  The minimum depth along contig at which to break the contig
```
</details>

This is the command I used: 
```
jgi_summarize_bam_contig_depths --outputDepth metaBat2/depth.txt metaBat2/ERR10905741.bam
```

The print out after it was done: (took around 5-10 minutes)

```
Output depth matrix to metaBat2/depth.txt
Output matrix to metaBat2/depth.txt
Opening 1 bams
Consolidating headers
Processing bam files
Thread 0 finished: ERR10905741.bam with 8568576 reads and 4746235 readsWellMapped
Creating depth matrix file: metaBat2/depth.txt
Closing most bam files
Closing last bam file
Finished
```

If this is run how to continue?:  
"We performed contig binning using MetaBAT2 (ref. 32), with
default parameters and a fixed seed (–seed 42) for reproducibility.
As MetaBAT2 may bin strains from the same species, creating a single
apparently contaminated MAG, we separated all circular contigs of
1 Mb or longer before binning the remaining contigs, as suggested in
the hifiasm-meta study." 
Here they cite the paper: https://www.nature.com/articles/s41592-022-01478-3, 
In here I understand it as they do the script sorting afterwards. 
"We used MetaBAT2 for initial binning and then post-process MetaBAT2 results to get final MAGs. We aligned raw reads to an assembly with ‘minimap2 -ak19 -w10 -I10G -g5k -r2k --lj-min-ratio 0.5 -A2 -B5 -O5,56 -E4,1 -z400,50 contigs.fa reads.fa’ 22, calculated the depth with ‘jgi_summa_rsize_bam_contig_depths --outputDepth depth.txt input.bam’ and ran MetaBAT2 with ‘metabat2 --seed 1 -i contigs.fa -a depth.txt’. We tried different random seeds or ‘-s 500000’, and got similar results. We only applied MetaBAT2 to the primary hifiasm-meta and HiCanu assemblies, as including alternative assemblies led to worse binning. After MetaBAT2 binning, we separate circular contigs of 1 Mb or longer into a separate MAG if it is binned together with other contigs."



As it was easier to continue with out the sorting I started a metaBat2
<details>
<summary> <b>Usage of metabat2</b></summary>
  
```
MetaBAT: Metagenome Binning based on Abundance and Tetranucleotide frequency (version 2.12.1; Aug 31 2017 21:02:54)
by Don Kang (ddkang@lbl.gov), Feng Li, Jeff Froula, Rob Egan, and Zhong Wang (zhongwang@lbl.gov)

Allowed options:
  -h [ --help ]                     produce help message
  -i [ --inFile ] arg               Contigs in (gzipped) fasta file format [Mandatory]
  -o [ --outFile ] arg              Base file name and path for each bin. The default output is fasta format.
                                    Use -l option to output only contig names [Mandatory].
  -a [ --abdFile ] arg              A file having mean and variance of base coverage depth (tab delimited;
                                    the first column should be contig names, and the first row will be
                                    considered as the header and be skipped) [Optional].
  -m [ --minContig ] arg (=2500)    Minimum size of a contig for binning (should be >=1500).
  --maxP arg (=95)                  Percentage of 'good' contigs considered for binning decided by connection
                                    among contigs. The greater, the more sensitive.
  --minS arg (=60)                  Minimum score of a edge for binning (should be between 1 and 99). The
                                    greater, the more specific.
  --maxEdges arg (=200)             Maximum number of edges per node. The greater, the more sensitive.
  --pTNF arg (=0)                   TNF probability cutoff for building TNF graph. Use it to skip the
                                    preparation step. (0: auto).
  --noAdd                           Turning off additional binning for lost or small contigs.
  --cvExt                           When a coverage file without variance (from third party tools) is used
                                    instead of abdFile from jgi_summarize_bam_contig_depths.
  -x [ --minCV ] arg (=1)           Minimum mean coverage of a contig in each library for binning.
  --minCVSum arg (=1)               Minimum total effective mean coverage of a contig (sum of depth over
                                    minCV) for binning.
  -s [ --minClsSize ] arg (=200000) Minimum size of a bin as the output.
  -t [ --numThreads ] arg (=0)      Number of threads to use (0: use all cores).
  -l [ --onlyLabel ]                Output only sequence labels as a list in a column without sequences.
  --saveCls                         Save cluster memberships as a matrix format
  --unbinned                        Generate [outFile].unbinned.fa file for unbinned contigs
  --noBinOut                        No bin output. Usually combined with --saveCls to check only contig
                                    memberships
  --seed arg (=0)                   For exact reproducibility. (0: use random seed)
  -d [ --debug ]                    Debug output
  -v [ --verbose ]                  Verbose output
```

</details>

```
metabat2 --seed 42 -i assembled/ERR10905741/contigs.fasta.gz -o metaBat2/binERR10905741 -a metaBat2/depth.txt -t 16
```
This was printed in the console afterwards: 
```
MetaBAT 2 (v2.12.1) using minContig 2500, minCV 1.0, minCVSum 1.0, maxP 95%, minS 60, and maxEdges 200. 
791 bins (1055104432 bases in total) formed.
```
And we have 791 binned files which when I undersatnd it correctly are our MAGs

</details>
