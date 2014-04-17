__author__ = 'BUNTY'
import argparse
from os import listdir
from os.path import isfile, join, basename
import re

parser = argparse.ArgumentParser(description = "Pipline to call ParseRDP script Snehal K. Talati")
parser.add_argument("inputdir", type = str, help="Input Fasta Directory")

args = parser.parse_args()

fasta_files = [ join(args.inputdir,f) for f in listdir(args.inputdir) if isfile(join(args.inputdir,f)) and f.endswith(".fa")]
Sample_Barcode_Output = open('sample_barcode.txt', 'w')
SampleTableOutput = open('SampleTable.txt' , 'w')

print "Parsing Fasta Files for breaking up filenames"
print >> SampleTableOutput, "Project\tSampleName"
print >> Sample_Barcode_Output, "SampleFullName\tSampleName\tSampleID\tSampleDate\tSampleRegion\tSampleBarcode"
for fa_file in fasta_files:
    filename =  basename(fa_file)
    sampleFull = re.search('(.*)_reads\.fa', filename).group(1)
    sample_name = re.search('(\w+)_[ATCG]{0,6}_', filename).group(1)
    SampleID = re.search('(.*)_\d{4}', filename).group(1)
    SampleDate = re.search('(\d{4}_\d+_\d+)', filename).group(1)
    SampleRegion = re.search('\d{4}_\d+_\d+_(\d+)', filename).group(1)
    barcode = re.search('\_([ATCG]*)_', filename).group(1)

    print >> Sample_Barcode_Output,  sampleFull + "\t" + sample_name + "\t" + SampleID + "\t" + SampleDate + "\t" + SampleRegion + "\t" + barcode
    print >> SampleTableOutput, "Microbiome" + "\t" + sample_name



