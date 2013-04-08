M-CAT : Metagenomics Coverage and Assignment Tool


Refernece Genome Data
--------------------
newbler.csbc.vcu.edu : /home/bnfo620/M-CAT


All_Bacteria_Drafts+.fna - Reference genome fasta file

(I found some 100000+ sequences were duplicated in this file. I created cleaned version.)

All_Bacteria_clean.fna - Clear Reference genome fasta file

gi_taxid_nucl.dmp -  gi id to tax-id mapping


Bowtie2 Index 
-------------
(Bowtie2 index has limitation of ~4 GB of nueleotides as reference genome. Thus, I need to partition reference file into two.)
All_Bacteria_1  - Index 1
All_Bacteria_2  - Index 2


Your samples need to be aligned separated to each of above two indices and then merge two sam files into one before your program reads it.

Sample Data
-----------
/home/bnfo620/M-CAT/sampledata/hmp
There are Five Samples from Human Genome Project's Health patients. These samples are from Vaginal site. 

Simulated Data
--------------
/home/bnfo620/M-CAT/sampledata/simulatddata/Staphylococcus_aureus_epidermidis*.fastq

Two Staphylococcus species mixed in one sample at 1x coverage. 


