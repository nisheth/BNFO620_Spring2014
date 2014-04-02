# Filename: parse_RDPClassified.py
# Description: Reads the RDP Classifier classified-output file and generates the ReadAssignment and ProfileSummary files 
# Author: Hardik I. Parikh
# Date: 03/26/2014

import sys
import argparse
import re
import math


# ArgParser module to get input from command line
parser = argparse.ArgumentParser(description="This script parses RDP Classifier output file and generates ReadAssigntment and ProfileSummary files.")
parser.add_argument("infile", type=argparse.FileType("r"), help="RDP Classifier Ouput File")
parser.add_argument("threshold_score", type=float, help="Threshold Score")
parser.add_argument("methodid", type=str, help="Sample ID")
parser.add_argument("sampleid", type=str, help="Sample ID")
parser.add_argument("ra_outputfile", type=str, help="ReadAssignment Output File")
parser.add_argument("ps_outputfile", type=str, help="ProfileSummary Output File")
args = parser.parse_args()


# Define variables and data structures
method_id = args.methodid
sample_id = args.sampleid
read_id = ""
RA_Dict = {}
PS_Dict = {}
level, name, score = ("", "", 0.0)
ps_count, ps_tot_score, ps_perc_read, ps_avg_score = (0, 0.0, 0.0, 0.0)
tot_read = 0


# Read the input file, store data in dictionary

for line in args.infile:
	line = line.strip()
	line = re.sub(r"\"", "", line)
	
	# convert line string into a list
	line_lst = line.split("\t")

	# get read id
	description_lst = line_lst[0].split("|")
	read_id = description_lst[2]
	tot_read += 1		# counter for total reads

	# iterate within the list to get Taxa-Level, Taxa-Name and Taxa-Score
	level_ct = 0		# variable to assign num to Taxa-level. Used later to sort the dictionaries
	for i in range(3, len(line_lst), 3):
		level = line_lst[i]
		level_ct += 1
		name = line_lst[i-1]
		score = float(line_lst[i+1])		

		# compare score to threshold cutoff and proceed
		if score >= args.threshold_score:

			# store data for read assignment dictionary	
			RA_Dict.setdefault(read_id,{}).setdefault(level,{})
			RA_Dict[read_id][level]['level_ct'] = level_ct
			RA_Dict[read_id][level]['name'] = name
			RA_Dict[read_id][level]['score'] = score
		
			# store data for profile summary dictionary
			PS_Dict.setdefault(level,{}).setdefault(level_ct,{})
			if name in PS_Dict.get(level,{}).get(level_ct,{}):
				new_ps_count = PS_Dict[level][level_ct][name]['count'] + 1
				PS_Dict[level][level_ct][name]['count'] = new_ps_count
				new_ps_tot_score = PS_Dict[level][level_ct][name]['tot_score'] + score
				PS_Dict[level][level_ct][name]['tot_score'] = new_ps_tot_score
			else:
				PS_Dict.setdefault(level,{}).setdefault(level_ct,{}).setdefault(name,{})
				ps_count = 1
				PS_Dict[level][level_ct][name]['count'] = ps_count
				ps_tot_score = score
				PS_Dict[level][level_ct][name]['tot_score'] = ps_tot_score
		
		else:
			break	



# Open Output files to write

ra_outfile = open(args.ra_outputfile, 'w')
ps_outfile = open(args.ps_outputfile, 'w')

ra_headerlst = ["Sample ID", "Method ID", "Read ID", "Taxa-Name", "Taxa-Level", "Taxa-Score"]
ra_header = "\t".join(ra_headerlst)
print >> ra_outfile, ra_header
ps_headerlst = ["Sample ID", "Method ID", "Taxa-Level", "Taxa-Name", "# of Reads", "% of Total", "Avg-Score"]
ps_header = "\t".join(ps_headerlst)
print >> ps_outfile, ps_header


# write ReadAssignment Output File
for (read_id, levels) in RA_Dict.iteritems():
	for (level, attrs) in sorted(levels.iteritems(), key=lambda x: x[1]['level_ct']):
		ra_printlst = [str(sample_id), str(method_id), str(read_id), str(RA_Dict[read_id][level]['name']), str(level), str(RA_Dict[read_id][level]['score'])]
		ra_printstr = "\t".join(ra_printlst)
		print >> ra_outfile, ra_printstr
		

# write ProfileSummary Output File
for (level, level_cts) in sorted(PS_Dict.iteritems(), key=lambda x:x[1]):
	for(level_ct, names) in level_cts.iteritems():
		for (name, attrs) in names.iteritems():
			ps_perc_read = ( PS_Dict[level][level_ct][name]['count'] / float(tot_read) ) * 100.00
			ps_avg_score = PS_Dict[level][level_ct][name]['tot_score'] / PS_Dict[level][level_ct][name]['count']
			ps_printlst = [str(sample_id), str(method_id), str(level), str(name), str(PS_Dict[level][level_ct][name]['count']), str("%.2f" % ps_perc_read), str("%.2f" % ps_avg_score)]	
			ps_printstr = "\t".join(ps_printlst)
			print >> ps_outfile, ps_printstr



# Close files
ra_outfile.close()
ps_outfile.close()

