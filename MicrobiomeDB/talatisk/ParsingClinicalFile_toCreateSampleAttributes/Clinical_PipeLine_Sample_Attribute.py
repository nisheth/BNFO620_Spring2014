__author__ = 'BUNTY'
import argparse
import os


parser = argparse.ArgumentParser(description = "Pipline to call all Clinical Files and Fasta Directory to Create Sample Attributes")
parser.add_argument("fasta_files_path", type = str, help="Path Fasta_Files")
parser.add_argument("clinical_file1", type = str, help="clinical_file_1")
parser.add_argument("clinical_mapping_file", type=str, help="clinical_mapping_file")

args = parser.parse_args()

fasta_file_path = args.fasta_files_path
clinical_file1_path = args.clinical_file1
clinical_mapping_path = args.clinical_mapping_file

print "Parsing Started............."

parse_fasta_file = ("python fasta_file_name_processing.py " + fasta_file_path )
os.system(parse_fasta_file)
print "Created from fasta file names --> sample_barcode.txt"
parse_clinical1 = ("python parsing_clinical.py " + clinical_file1_path)
os.system(parse_clinical1)
print "Created from clincical file one --> Final_Clinical_Parsed.txt"
parse_clinical_merge = ("python parsing_clinical2.py " + "Final_Clinical_Parsed.txt sample_barcode.txt " + clinical_mapping_path)
os.system(parse_clinical_merge)
print "Created Unflattened Version merging all files --> Sample_Attributes_Unflattened.txt"
parse_clinical_map = ("python parsing_clinical3.py " + "Sample_Attributes_Unflattened.txt")
os.system(parse_clinical_map)
print "Finally Created Sample Attributes Table --> Sample_Attributes_Flattened_Table.txt"

print "Parsing Complete :)"
