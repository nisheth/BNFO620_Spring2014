import argparse


parser = argparse.ArgumentParser(description = "Pipline to call ParseRDP script Snehal K. Talati")
parser.add_argument("nodes_dump", type = file, help="nodes.dmp")
parser.add_argument("names_dump", type = file, help="names.dmp")
parser.add_argument("profile_summary", type = file, help="profile_summary")
args = parser.parse_args()

nodes_file = args.nodes_dump
names_file = args.names_dump
profile_summary = args.profile_summary
header_line = next(profile_summary)

taxa_Table_File = open("Taxa_Final_File.txt", "w")

dictionary = {}

print "Making Dictionary..."
for line in profile_summary:
    line = line.rstrip().split('\t')
    line[3] = line[3].replace("Root", "root")
    dictionary[line[3]] = ['Not Mapped','','']

print "Checking Names File..."
for line2 in names_file:
    line2 = line2.rstrip().split('\t')
    #print line2[2]
    for key in dictionary:
        if line2[2] == key:
            dictionary[key][0] = line2[0]
print "Checking Nodes File..."
for line3 in nodes_file:
    line3 = line3.rstrip().split('\t')
    for key in dictionary:
    #print line3[0]
         if line3[0] == dictionary[key][0]:
             dictionary[key][1] = line3[4]
             dictionary[key][2] = line3[2]

print >> taxa_Table_File, 'TAXAID\tNAME\tTAXALEVEL\tPARENT_TAXA_ID'
print "Preparing to print from dictionary..."
for key in dictionary:
    print  >> taxa_Table_File, dictionary[key][0] + "\t" + key + "\t" + dictionary[key][1] + "\t" + dictionary[key][2]





