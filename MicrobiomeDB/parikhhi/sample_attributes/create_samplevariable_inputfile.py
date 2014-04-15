import sys
import re

infile = open("Sample_Attributes.tsv", "r")
outfile = open("SampleVariables.tsv", "w")

header_lst = ["Sample Name", "Sample Variable", "Variable Value"]
header_str = "\t".join(header_lst)
print >> outfile, header_str

header_infile = infile.readline()
header_infile_lst = header_infile.strip().split("\t")

for line in infile:
	line_lst = line.strip().split("\t")
	site_depth = line_lst[8]
	print site_depth
	samplecollectiondate = line_lst[3].split("_")
	yyyy = samplecollectiondate[0]
	mm = samplecollectiondate[1]
	dd = samplecollectiondate[2]
	date_newformat = [mm, dd, yyyy]	
	line_lst[3] = "/".join(date_newformat)
	print line_lst[3]

	if site_depth == "Deep":
		for i in range(3, len(line_lst), 1):
			print header_infile_lst[i]
			if re.search("-S", header_infile_lst[i]):
				print "TRUE"
			else:
				header_infile_lst[i] = re.sub("-D", "", header_infile_lst[i])
				print_lst = [str(line_lst[1]), str(header_infile_lst[i]), str(line_lst[i])]
				print_str = "\t".join(print_lst)
				print print_str
				print >> outfile, print_str
	elif site_depth == "Shallow":
		for i in range(3, len(line_lst), 1):
			print header_infile_lst[i]
			if re.search("-D", header_infile_lst[i]):
				print "TRUE"
			else:
				header_infile_lst[i] = re.sub("-S", "", header_infile_lst[i])
				print_lst = [str(line_lst[1]), str(header_infile_lst[i]), str(line_lst[i])]
				print_str = "\t".join(print_lst)
				print print_str
				print >> outfile, print_str

infile.close()

