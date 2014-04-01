import argparse
import re
import os
from os import listdir
from os.path import isfile, join


# Construct ArgumentParser and add the arguments
parser = argparse.ArgumentParser(description= "Extracts taxa classification information of all .fa files in a folder and parses the extracted file.")
parser.add_argument("path_of_classifierjar", type=str, help= "path to RDP classifier.jar file")
parser.add_argument("path_of_fasta_files", type=str, help= "path to input fasta file")

args = parser.parse_args()


# Generate a list of all fasta files within the input directory
fasta_file_lst = [ join(args.path_of_fasta_files,f) for f in listdir(args.path_of_fasta_files) if isfile(join(args.path_of_fasta_files,f)) and f.endswith(".fa")]
#fasta_file_lst = os.listdir(args.path_of_fasta_files)


# Looping through all the files in the directory
for file in fasta_file_lst:
    # To let us know when which file is getting processed
    print "File: " + file

    
    # Obtaining the sample id.
    samp = file.split("\\")
    #print samp
    sample_id1 = samp[5] 
    #print sample_id1
    samp2 = sample_id1.split("_")
    sample_id = samp2[0]+"_"+samp2[1]+"_"+samp2[2]+"_"+samp2[3]+"_"+samp2[4]+"_"+samp2[5]
    #print sample_id
    

    # Creating files for writing, writing the header into it.
    try:
        fileOut_1 = open(sample_id+"_read_assignment.txt", "w")
    except:
        print "File cannot be opened for writing."

    header_1 = "SampleID" + "\t" + "Method-id" + "\t" + "ReadID" + "\t" + "Taxa-level" + "\t" + "Taxa-name" + "\t" + "Score" + "\n"
    fileOut_1.write(header_1)    

    try:
        fileOut_2 = open(sample_id+"_profile_summary.txt", "w")
    except:
        print "File cannot be opened for writing."

    header_2 = "SampleID" + "\t" + "Method-id" + "\t" + "Taxa-name" + "\t" + "Taxa-level" + "\t" + "#_of_reads" + "\t" + "%_of_total" + "\t" + "Avg_Score" + "\n"
    fileOut_2.write(header_2)


    # Running the command for rdp classifier
    command = "java -Xmx1g -jar " + args.path_of_classifierjar + " classify -c 0.5 -o " + sample_id + "_classified.txt" + " " + file
    #print type(file_name)
    #print command
    os.system(command)


    # Opening the output file from rdp classifier
    try:
        fileHandle_2 = open(sample_id+"_classified.txt", "r")
    except:
        print "File cannot be opened for reading."
        

    #Declaring all variables  
    method_id = "1"
    read_id = ""
    taxa_name = ""
    taxa_level = ""
    score = ""
    percent = ""
    avg = ""
    threshold = 0.5
    taxa_dict = {}
    num_of_reads = 0
    

    #Looping through all the lines in the output file which was obtained from rdp classifier.
    while True:
        line = fileHandle_2.readline().strip()
        if line == "":
            break

        line = re.sub(r"\"", "", line)

        # Count for the number of reads
        num_of_reads += 1

        # Splitting the line based on tabs
        columns = line.split("\t")

        # Obtaining the read id 
        description = columns[0].split("|")
        read_id = description[2]

        #print sample_id + "\t" + read_id + "\t"
        #print columns[3]

        # Iterate in the list "columns" to get the taxa name, taxa level and score.
        for i in range(2, len(columns), 3):
            taxa_name = columns[i]
            taxa_level = columns[i + 1]
            score = columns[i + 2]
            # Checking whether the scores are above the threshold value.
            if (float(score) >= threshold):
                # If it is, then writing into the read assignment file.
                fileOut_1.write(sample_id + "\t" + method_id + "\t" + read_id + "\t" + taxa_name + "\t" + taxa_level + "\t" + score + "\n")

                # If that taxa name exists, adding the count and the scores.
                if taxa_name in taxa_dict:
                    taxa_dict[taxa_name][4] += 1
                    taxa_dict[taxa_name][5] += float(score)
                # If not, creating the default dictionary with the respective key and values.    
                else:
                    taxa_dict[taxa_name] = [sample_id, method_id, taxa_name, taxa_level, 1, float(score)]
                    

    # Writing into the profile summary file                
    for taxa_name in taxa_dict:
        percent_val = (float(taxa_dict[taxa_name][4])/float(num_of_reads))*100
        percent = format(percent_val, ".2f")
        avg_val = taxa_dict[taxa_name][5]/(float(taxa_dict[taxa_name][4]))
        avg = format(avg_val, ".2f")
        fileOut_2.write(str(taxa_dict[taxa_name][0]) + "\t" + str(taxa_dict[taxa_name][1]) + "\t" + str(taxa_dict[taxa_name][2]) + "\t" + str(taxa_dict[taxa_name][3]) + "\t" + str(taxa_dict[taxa_name][4]) + "\t" + str(percent) + "\t" + str(avg) + "\n")
        

# Closing all the files
fileHandle_2.close()
fileOut_1.close()
fileOut_2.close()
                


    




    
