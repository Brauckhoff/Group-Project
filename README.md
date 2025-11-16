# Task

Reproduce analysis of the paper and compare to original paper.


# Initial notes

- Comparison of 3 state-of-the-art assemblers:
- [ ] metaMDBG
- [ ] metaFlye (v.2.9-b1768)
- [ ] hifiasm-meta (v.0.2-r058)
- used two mock communities and three samples\
(File: data/41587_2023_1983_MOESM2_ESM.xlsx\
 see overview: TableS1\
 see commands: TableS2\
 see results: Table S3)
- all data sets used in this study were downloaded from the [NCBI Sequence Read Archive](https://www.ncbi.nlm.nih.gov/); accession numbers are given in Supplementary Table S1.


- [ ] Report 4-8 Pages


# Questions

- should we perform all analysis (some take > 30 days)?
- only analyze PacBio or also OxfordNanopore?
- repeat whole benchmark or only analysis with metaMDBG?
- task: apply metaMDBG to all 5 data sets, check if we get same result?
-


# Timeline (in weeks)

**17th nov**
- [ ] get access to the cluster (server)!
- [ ] in case of benchmark: implement thing that takes 40 days

**24th nov**
- [ ] lay low and learn :)

**01st dec**
- [ ] code should be good to go for server

**08th dec**
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
- [ ] write report
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
