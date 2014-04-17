import argparse
import sys
import re
import os
from os import listdir
from os.path import isfile, join

# Construct ArgumentParser and add the arguments
parser = argparse.ArgumentParser(description= "Extracts the sample informations.")
parser.add_argument("path_of_fasta_files", type=str, help= "path to input fasta file")

args = parser.parse_args()

# Creating a file to write the sample information and writing the required information into it.
try:
    fileOut_samp_1 = open("samp_info.txt", "w")
except:
    print "File cannot be opened for writing."

header_samp_1 = "Sample_Name" + "\t" + "Sample_ID" + "\t" + "Date" + "\t" + "Region" + "\t" + "Barcode" + "\n" 
fileOut_samp_1.write(header_samp_1)

# Creating a file to write the sample information and writing the required information into it.
try:
    fileOut_samp_2 = open("samp_name.txt", "w")
except:
    print "File cannot be opened for writing."

header_samp_2 = "Sample_Name" + "\n" 
fileOut_samp_2.write(header_samp_2)

# Generate a list of all fasta files within the input directory
fasta_file_lst = os.listdir(args.path_of_fasta_files)
#print fasta_file_lst 

# Looping through all the files in the directory
for file in fasta_file_lst:
    # To let us know when which file is getting processed
    print "File: " + file
    #fileOut_samp.write(file + "\n")

    sample_id = re.search("(\w+)_(20[0-9][0-9].*)_(\d+)_([ATCG]+).*", file).group(1)
    sample_date = re.search("(\w+)_(20[0-9][0-9].*)_(\d+)_([ATCG]+).*", file).group(2)
    sample_region = re.search("(\w+)_(20[0-9][0-9].*)_(\d+)_([ATCG]+).*", file).group(3)
    sample_name = sample_id + "_" + sample_date + "_" + sample_region
    sample_barcode = re.search("(\w+)_(20[0-9][0-9].*)_(\d+)_([ATCG]+).*", file).group(4)
    fileOut_samp_1.write(sample_name + "\t" + sample_id + "\t" + sample_date + "\t" + sample_region + "\t" + sample_barcode + "\n")
    fileOut_samp_2.write(sample_name + "\n")
    #print sample_name
    #print sample_id
    #print sample_date
    #print sample_region
    #print sample_barcode
    #print barcode
    
fileOut_samp_1.close()
fileOut_samp_2.close()
            
