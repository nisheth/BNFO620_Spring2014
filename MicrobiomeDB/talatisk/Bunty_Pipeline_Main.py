__author__ = 'BUNTY'
import argparse
import os
from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser(description = "Pipline to call ParseRDP script Snehal K. Talati")
parser.add_argument("RDPClassifier_Jar", type = str, help="Path to RDP Classifier")
parser.add_argument("inputdir", type = str, help="Input Fasta Directory")

args = parser.parse_args()

fasta_files = [ join(args.inputdir,f) for f in listdir(args.inputdir) if isfile(join(args.inputdir,f)) and f.endswith(".fa")]


num_files = 0
print "Parser Program is Running DO NOT CLOSE THIS OR ELSE ........."
for fa_file in fasta_files:
		num_files += 1
		parse_command = ("python Parser_RDPClassifier.py " + fa_file + " " + args.RDPClassifier_Jar + " 0.8")
		print "Processing File" + " " + str(num_files)
		os.system(parse_command)

print "Parser Program is Complete you have processed" + str(num_files) + " files"
