import argparse
import re

# Construct ArgumentParser and add the arguments
parser = argparse.ArgumentParser(description= "Extracts informations from the names and nodes")
parser.add_argument("file_names", type=str, help= "Input names file")
parser.add_argument("file_nodes", type=str, help= "Input nodes file")

args = parser.parse_args()

# Creating a file handle to read the information from names file.
try:
    fileHandle_1 = open(str(args.file_names), "r")
except:
    print "File cannot be opened for reading."


# Creating a file handle to read the information from nodes file.
try:
    fileHandle_2 = open(str(args.file_nodes), "r")
except:
    print "File cannot be opened for reading."


# Creating files to write into.
try:
    fileOut_1 = open("names_out.txt", "w")
except:
    print "File cannot be opened for writing."

header_1 = "Tax_id" + "\t" + "Unique_name" + "\n"
fileOut_1.write(header_1)

try:
    fileOut_2 = open("nodes_out.txt", "w")
except:
    print "File cannot be opened for writing."

header_2 = "Tax_id" + "\t" + "Parent_tax_id" + "\t" + "rank" + "\n"
fileOut_2.write(header_2)

unique_name_array = []

# Processing the files
for line in fileHandle_1:
    if re.search(r"scientific name", line):
        #print line
        columns = line.split("|")
        tax_id = columns[0]
        unique_name = columns[1]
        fileOut_1.write(tax_id + "\t" + unique_name + "\n")


for line in fileHandle_2:
    #print line
    columns = line.split("|")
    tax_id = columns[0]
    parent = columns[1]
    rank = columns[2]
    fileOut_2.write(tax_id + "\t" + parent + "\t" + rank + "\n")
    
fileHandle_1.close()
fileHandle_2.close()
fileOut_1.close()
fileOut_2.close()
    
    

