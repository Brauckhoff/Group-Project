# Task

Reproduce analysis of the paper and compare to original paper.

# To Do's

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
- [Zymo-HiFi mock reference genomes](https://s3.amazonaws.com/zymo-files/BioPool/D6331.refseq.zip) https://s3.amazonaws.com/zymo-files/BioPool/D6331.refseq.zip. 
- [ATCC mock reference genomes](https://www.atcc.org/products/msa-1003)



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
