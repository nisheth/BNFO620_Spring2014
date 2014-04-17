import argparse
import re
from os import listdir
from os.path import isfile, join

# Construct ArgumentParser and add the arguments
parser = argparse.ArgumentParser(description= "Extracts the read informations")
parser.add_argument("path_of_fasta_files", type=str, help= "path to input fasta file")

args = parser.parse_args()

# Creating a file to write the read information and writing the required information into it.
try:
    fileOut_read = open("read_info.txt", "w")
except:
    print "File cannot be opened for writing."

header_read = "SampleID" + "\t" + "ReadID" + "\t" + "Read_length" + "\t" + "Quality_score" + "\n"
fileOut_read.write(header_read)


# Generate a list of all fasta files within the input directory
fasta_file_lst = [ join(args.path_of_fasta_files,f) for f in listdir(args.path_of_fasta_files) if isfile(join(args.path_of_fasta_files,f)) and f.endswith(".fa")]
#fasta_file_lst = os.listdir(args.path_of_fasta_files)


# Looping through all the files in the directory
for file in fasta_file_lst:
    # To let us know when which file is getting processed
    print "File: " + file

    # Opening the file 
    try:
        fileHandle = open(str(file), "r")
    except:
        print "File cannot be opened for reading."

    
    # Obtaining the sample id.
    samp = file.split("\\")
    #print samp
    expression_search = re.search("(.*?)_([ATCG]+?).*", str(samp[6]))
    sample = expression_search.group(1)
    barcode = expression_search.group(2)
    #print sample

    
    # Looping through each line in the file. 
    for line in fileHandle:
        #print line
        if re.search(r">", line):
            #print line
            line = re.sub(r">", "", line)
            read = line.split("|")
            read_id = read[2]
            read_len = read[3]
            score = read[4]
            
        # Printing into the read file
        fileOut_read.write(sample + "\t" + read_id + "\t" + read_len + "\t" + score + "\n")
        

# Closing the files
fileHandle.close()
fileOut_read.close()
            

    
