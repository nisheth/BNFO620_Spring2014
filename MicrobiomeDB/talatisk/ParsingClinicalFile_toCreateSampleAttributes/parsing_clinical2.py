import argparse

parser = argparse.ArgumentParser(description="This program parses the Clinical Excel File")

##add arguments to our parser which are the two files the first is the genebank file and the second is the output file name
parser.add_argument('standardized_file', type=file, help="standardized file")
parser.add_argument('barcode_file', type=file, help="barcode file")
parser.add_argument('mapping_clinical', type=file, help="mapping_clinical")
args = parser.parse_args()

Sample_Attributes_Unflattened = open('Sample_Attributes_Unflattened.txt', 'w')

clinical_file = args.standardized_file
clinical_header = next(clinical_file).rstrip()
barcode_file1 = args.barcode_file
clinical_map = args.mapping_clinical
clinical_map_line_header = next(clinical_map).rstrip().split('\t')
clinical_map_line_header.pop(0)
barcode_line_header = next(barcode_file1)

dict = {}
clinical = {}
clinical_variables = {}

print >> Sample_Attributes_Unflattened, clinical_header + "\t" + "Barcode" + "\t" + ("\t".join(clinical_map_line_header))
## Clinical File1
for line in clinical_file:
    clinical_line = line.rstrip().split('\t')
    line = line.rstrip()
    dict[clinical_line[0]] = line




for line3 in clinical_map:
    #line4 = line4.rstrip()
    line3 = line3.rstrip().split("\t")
    patientid = line3[0]
    line3.pop(0)
    clinical_variables[patientid] = line3




## FASTA FILE BREAKDOWN

for line2 in barcode_file1:
    #print line2
    barcode_line = line2.rstrip().split('\t')
    #print barcode_line[1]
    final_line = dict[barcode_line[1]] + "\t" + barcode_line[5]
    final_line = final_line.rstrip()
    final_line2 = final_line.split('\t')
    clinical[final_line2[3]] = final_line
    print >> Sample_Attributes_Unflattened, final_line + "\t" + ('\t'.join(clinical_variables[final_line2[3]]))
    #print clinical[final_line2[3]]






















