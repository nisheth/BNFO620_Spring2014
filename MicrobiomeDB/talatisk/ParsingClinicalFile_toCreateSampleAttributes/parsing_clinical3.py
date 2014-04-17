import argparse

parser = argparse.ArgumentParser(description="This program parses the Clinical Excel File")

##add arguments to our parser which are the two files the first is the genebank file and the second is the output file name
parser.add_argument('sample_attributes', type=file, help="sample_attributes_file")
args = parser.parse_args()

flattened_sample_attributes = open("Sample_Attributes_Flattened_Table.txt", "w")
unflattened_sample_attributes = args.sample_attributes
unflattened_sample_attributes_header = next(unflattened_sample_attributes).split("\t")
dictionary = {}

unflattened_sample_attributes_header.pop(0)

print >> flattened_sample_attributes, "SampleName\tAttribute\tValue"
for line in unflattened_sample_attributes:
    line_list = line.rstrip().split("\t")
    dictionary[line_list[0]] = line_list
    line_list.pop(0)


for key in dictionary:
    for i in range(33):
        print >> flattened_sample_attributes, key + "\t" + unflattened_sample_attributes_header[i] + "\t" + dictionary[key][i]


