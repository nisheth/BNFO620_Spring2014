import argparse
import re

# Construct ArgumentParser and add the arguments
parser = argparse.ArgumentParser(description= "Extracts information only for those taxa names that are present in profile summary file.")
parser.add_argument("file_profile", type=str, help= "Input profile summary file")
parser.add_argument("file_taxa", type=str, help= "Input taxa file")

args = parser.parse_args()

# Creating a file handle to read the information from names file.
try:
    fileHandle_1 = open(str(args.file_profile), "r")
except:
    print "File cannot be opened for reading."


# Creating a file handle to read the information from nodes file.
try:
    fileHandle_2 = open(str(args.file_taxa), "r")
except:
    print "File cannot be opened for reading."


# Creating files to write into.
try:
    fileOut_1 = open("Taxa_to_load.txt", "w")
except:
    print "File cannot be opened for writing."

header_1 = "Tax_id" + "\t" + "Unique_name" + "\t" + "Parent_tax_id" + "\t" + "Rank" + "\n" 
fileOut_1.write(header_1)

taxa_array = []
uniq_dict = {}

#Processing the files
for line in fileHandle_1:
    columns = line.split("\t")
    taxa_name = columns[3]
    taxa_array.append(taxa_name)
#print taxa_array

for line in fileHandle_2:
    #print line
    taxa = "Key"
    columns = line.split("\t")
    tax_id = columns[0]
    uniq_name = columns[1]
    #uniq_array.append(uniq_name)
    parent = columns[2]
    rank = columns[3]
    uniq_dict[taxa] = [tax_id, uniq_name, parent, rank]

    for i in taxa_array:
        if i == uniq_dict[taxa][1]:
            fileOut_1.write(str(uniq_dict[taxa][0]) + "\t" + str(uniq_dict[taxa][1]) + "\t" + str(uniq_dict[taxa][2]) + "\t" + str(uniq_dict[taxa][3]) + "\n")
        else:
            fileOut_1.write("")
        
fileHandle_1.close()
fileHandle_2.close()
fileOut_1.close()

