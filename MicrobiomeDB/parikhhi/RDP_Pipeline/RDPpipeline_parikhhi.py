# Filename: RDPpipeline_parikhhi.py
# Description: This pipleine accepts Input-Dir-fastafiles, runs RDPClassifier for each file, parses the classified output and generates the read assignment and profile summary files
# Author: Hardik I Parikh
# Date: 03/28/2014

import argparse
import os
import re
from os import listdir
from os.path import isfile, join


# ArgParser module to get input from command line
parser = argparse.ArgumentParser(description="RDP Classifier Pipeline - parikhhi.")
parser.add_argument("RDPclassifier_jar", type=str, help="Path to RDP classifier.jar file")
parser.add_argument("inputdir", type=str, help="Input FASTA files directory")

args = parser.parse_args()


# Generate a list of all fasta files within the input directory
fasta_file_lst = [ join(args.inputdir,f) for f in listdir(args.inputdir) if isfile(join(args.inputdir,f)) and f.endswith(".fa")]

# Make Appropriate Output Directories 
rdp_outputdir = "./Output_RDPClassifier_files/"
ra_outputdir = "./Output_ReadAssignment_files/"
ps_outputdir = "./Output_ProfileSummary_files/"

if not os.path.exists(rdp_outputdir):
	os.makedirs(rdp_outputdir)
if not os.path.exists(ra_outputdir):
	os.makedirs(ra_outputdir)
if not os.path.exists(ps_outputdir):
	os.makedirs(ps_outputdir)

# Run the pipeline for each file
file_ctr = 0
for fasta_file in fasta_file_lst:

	file_ctr += 1
	print file_ctr	
	print os.path.basename(fasta_file)	

	# Create output file names
	rdp_outputfile = re.sub(args.inputdir, rdp_outputdir, fasta_file)
	rdp_outputfile = re.sub(r'_[ATGC]+_reads.fa', 'classified.tsv', rdp_outputfile)
	ra_outputfile = re.sub(args.inputdir, ra_outputdir, fasta_file)
	ra_outputfile = re.sub(r'_[ATGC]+_reads.fa', 'ra.tsv', ra_outputfile)
	ps_outputfile = re.sub(args.inputdir, ps_outputdir, fasta_file)
	ps_outputfile = re.sub(r'_[ATGC]+_reads.fa', 'ps.tsv', ps_outputfile)

		
	# Run RDP classifier on the input file
	rdp_classifier_command = "java -Xmx1g -jar " + args.RDPclassifier_jar + " classify -c 0.5 -o " + rdp_outputfile + " " + fasta_file
	print ""	
	print "Running the RDP Classifier ..."
	print rdp_classifier_command
	os.system(rdp_classifier_command)
	print "Done."

	# Run the parsing program
	sampleid = os.path.basename(fasta_file)
	sampleid = re.sub(r'_[ATGC]+_reads.fa', '', sampleid)
	threshold_value = "0.5"
	method_id = "1"

	parse_command = "python parse_RDPClassified_parikhhi.py " + rdp_outputfile + " " + threshold_value + " " + method_id + " " + sampleid + " " + ra_outputfile + " " + ps_outputfile
	print ""	
	print "Parsing the RDP Classifier Output File ..."
	print parse_command
	os.system(parse_command)
	print "Done."
	print ""	
	print ""	


