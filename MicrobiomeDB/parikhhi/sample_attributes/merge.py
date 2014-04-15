import sys
import re

patientDict = {}
sampleDict = {}

infile1 = open("PatientInfo.tsv", "r")
infile2 = open("Sample-Patient.tsv", "r")
outfile = open("Sample_Attributes.tsv", "w")

header_infile1 = infile1.readline()
header_infile1_lst = header_infile1.strip().split("\t")
for line in infile1:
	line_lst = line.strip().split("\t")
	patient_id = line_lst[0]
	patientDict[patient_id] = line_lst


header_infile2 = infile2.readline()
header_infile2_lst = header_infile2.strip().split("\t")
for line in infile2:
	line_lst = line.strip().split("\t")
	sample_id = line_lst[1]
	sampleDict[sample_id] = line_lst


outfile_header = header_infile2_lst
outfile_header.extend(header_infile1_lst) 
outfile_header_string = "\t".join(outfile_header)
print >> outfile, outfile_header_string

for (sample_id, values) in sampleDict.iteritems():
	patient_id = sampleDict[sample_id][6]
	print "Sample ID -", sample_id, "\tPatient ID -", patient_id
	print_lst = sampleDict[sample_id]
	print_lst.extend(patientDict[patient_id])
	print_string = "\t".join(print_lst)
	print >> outfile, print_string


infile1.close()
infile2.close()
outfile.close()

print "Done."
