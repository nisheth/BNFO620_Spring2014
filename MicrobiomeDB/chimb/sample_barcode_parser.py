__author__ = 'Bryan'
import re
import argparse
import os

#construct ArgumentParser and add arguments for file in and file out
parser = argparse.ArgumentParser(description='Get sample and sample barcode')
parser.add_argument('dir_of_fasta_files', type=str, help="directory to input fasta file")
parser.add_argument('output_file', type=argparse.FileType('w'), help="output file name")


args = parser.parse_args()
fasta_files = os.listdir(args.dir_of_fasta_files)

for file in fasta_files:


    sample_id_barcodeC = re.search("(.*?)_([ATCG]+?)_(?:read|test).*", file)
    sample = sample_id_barcodeC.group(1)
    barcode = sample_id_barcodeC.group(2)

    print >> args.output_file, sample,'\t',barcode


