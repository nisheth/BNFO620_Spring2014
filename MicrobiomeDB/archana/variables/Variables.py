# Reads the myTrinh_Rename and Patients tab from the OralMicrobiome_Clinical_Mapping_Data.xls file as different tab delimeted text files.
# Parses the required information. 

import argparse
import re
import csv

# Construct ArgumentParser and add the arguments
parser = argparse.ArgumentParser(description= "Extracts informations from clinical data.")
parser.add_argument("file_variables", type=str, help= "Input variables file")

args = parser.parse_args()

# Creating a file handle to read the information from clinics file, myTrinh_Rename tab.
try:
    fileHandle_1 = open(str(args.file_variables), "r")
except:
    print "File cannot be opened for reading."


# Creating files to write into.
try:
    fileOut = open("clinic_out.txt", "w")
except:
    print "File cannot be opened for writing."

header = "Sample_id" + "\t" + "Variable" + "\t" + "Value" + "\n"
fileOut.write(header)
            

# Parsing data from the variables file
reader = csv.reader(fileHandle_1, delimiter = "\t", skipinitialspace = True)
line_data = list()
columns = next(reader)
#print(columns)

for col in columns:
    # Create a list in lineData for each column of data.
    line_data.append(list())
#print lineData


for line in reader:
    for i in xrange(0, len(line_data)):
        # Copy the data from the line into the correct columns.
        line_data[i].append(line[i])
#print line_data
        
data = dict()

for i in xrange(0, len(columns)):
    # Create each key in the dict with the data in its column.
    data[columns[i]] = line_data[i]

# For printing into the file
for i, n in enumerate(data[columns[0]]):
    #print i
    for j, m in enumerate(columns):
        fileOut.write(str(data[columns[0]][i]) + "\t" + str(columns[j]) + "\t")
        if str(data[columns[j]][i]) == "":
            fileOut.write("NA" + "\n")
        else:    
            fileOut.write(str(data[columns[j]][i]) + "\n")


fileHandle_1.close()
fileOut.close()
