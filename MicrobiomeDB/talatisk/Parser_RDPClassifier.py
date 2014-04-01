import argparse
import re
import os



parser = argparse.ArgumentParser(description="This program parses the RDP Classifier output")

##add arguments to our parser which are the two files the first is the genebank file and the second is the output file name
parser.add_argument('input_file', type=file, help='fasta_file')
parser.add_argument('path_of_classifier', type=str, help="path to RDP classifier file")
parser.add_argument('input_threshold', type=float)
args = parser.parse_args()

#print args.input_file.name
output_name = re.search('(\w+)_[ATCG]{0,6}_', args.input_file.name).group(1)
threshold = str(args.input_threshold)

os.system("java -Xmx1g -jar " + args.path_of_classifier + " classify -c 0.8 -o " + output_name + "_classified.txt" + " " + args.input_file.name)

RDP_Results_Output = open(output_name+'_read_assignment.txt', 'wb+')
RDP_Results_Summary = open(output_name+'_profile_summary.txt', 'wb+')

print >> RDP_Results_Output, 'SampleID\tMethod-id\tReadID\tTaxa-Name\tTaxa-Level\tScore'
print >> RDP_Results_Summary, 'SampleID\tMethod-id\tTaxa-Name\tTaxa-Level\t#_of_Reads\t%_of_Total\tAvg_Score'


RDP_results = open(output_name + "_classified.txt")

method_id = '2'
list = []
ReadAssignment = {}
ReadAssignment2 = {}
total_reads = 0


for line in RDP_results:
    list = line.rstrip().split("\t")
    del list[1] ## Remove the - column from the original output
    read_sample_id = re.match(".*?\|\d+\|(.*?)\|.*", list[0]).group(1)

    for i in range(1, len(list), 3):
        taxa_name = list[i]
        taxa_name = taxa_name.replace('"', '')
        taxa_level = list[i+1]
        score = float(list[i+2])

        if score >= args.input_threshold:
            print >> RDP_Results_Output, output_name, '\t',method_id, '\t', read_sample_id, '\t', taxa_name, '\t', taxa_level, '\t', score
            concatenated_line = output_name + "\t" + method_id + "\t" + taxa_name + "\t" + taxa_level
            if concatenated_line in ReadAssignment:
                ReadAssignment[concatenated_line] += 1
            else:
                ReadAssignment[concatenated_line] = 1

            if concatenated_line in ReadAssignment2:
                ReadAssignment2[concatenated_line] += score
            else:
                ReadAssignment2[concatenated_line] = score

        else:
            break

    total_reads = total_reads + 1


for taxis in ReadAssignment:
    percent_total = float(ReadAssignment[taxis])/float(total_reads)*100.00
    average_score = float(ReadAssignment2[taxis])/float(ReadAssignment[taxis])

    print >> RDP_Results_Summary, taxis, '\t', ReadAssignment[taxis], '\t' ,"%.2f" % percent_total, '\t',"%.2f" % average_score












        












