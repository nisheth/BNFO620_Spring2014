import sys
import re

input_1 = open("OralMicrobiome_Clinical_Variables_Data.txt", "r")
input_2 = open("Patient_sample_info.txt", "r")
output = open("Merged_file.xls", "w")

patient_dict = {}
sample_dict = {}

header_1 = input_1.readline()
header_1_list = header_1.strip().split("\t")
for line in input_1:
    line_list = line.strip().split("\t")
    patient_id = line_list[0]
    patient_dict[patient_id] = line_list


header_2 = input_2.readline()
header_2_list = header_2.strip().split("\t")
for line in input_2:
    line_list = line.strip().split("\t")
    sample_id = line_list[1]
    sample_dict[sample_id] = line_list


output_header = header_2_list
output_header.extend(header_1_list) 
output_header_string = "\t".join(output_header)
output.write(output_header_string + "\n")

for (sample_id, values) in sample_dict.iteritems():
	patient_id = sample_dict[sample_id][6]
	print "Sample ID -", sample_id, "\tPatient ID -", patient_id
	print_list = sample_dict[sample_id]
	print_list.extend(patient_dict[patient_id])
	print_string = "\t".join(print_list)
	output.write(print_string + "\n")


input_1.close()
input_2.close()
output.close()

print "Done."
