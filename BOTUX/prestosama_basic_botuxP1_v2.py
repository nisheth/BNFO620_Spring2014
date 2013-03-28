#Melissa Prestosa

import sys
import re
import os
import operator

def main ():
	if len(sys.argv) < 3:
		print "Please input fasta file, threshold, and trimlength if using"
		sys.exit(0)
	
	if len(sys.argv) == 4:
		infile = sys.argv[1]
		threshold = sys.argv[2]
		trimlen = sys.argv[3]
	else:
		infile = sys.argv[1]
		threshold = sys.argv[2]
		trimlen = -1
	
	outf = 'sorted_by_abundance_and_length.txt'
	trimlen = int(trimlen)
	lenAbunD = {}
	readInCounter = 0
	
	fastafile = open(infile)
	line = fastafile.readline().strip()
	while line != '':
		readInCounter += 1
		match = re.search(r'^\>.',line)
		if match:
			pass
		else:
			length = len(line)
			if trimlen != -1 and length > trimlen:
				line = line[:trimlen]
				length = len(line)
			if lenAbunD.has_key(length):
				if lenAbunD[length].has_key(line):
					lenAbunD[length][line] += 1
				else:
					lenAbunD[length][line] = 1
			else:
				lenAbunD[length] = {}
				lenAbunD[length][line] = 1				
		
		line = fastafile.readline().strip()
		if readInCounter%1000 == 0:
			print 'read %s lines from file %s' %(readInCounter, infile)
			
		
	fastafile.close()

	i=1
	totalReads = 0
	
	outfile = open(outf, 'w')
	outline ='------------------------------------------------------------\n'
	for lenn in sorted(lenAbunD.keys(), reverse=True):
		outfile.write(outline)		
		items = sorted([(v, k) for k, v in lenAbunD[lenn].items()], reverse=True) ##makes dict into tuples NOW THE TUPLES ARE IN THE ORDER (abun, seq)!!!
		
		for x in items:
			outstring = ''.join(['SEQ NUM: ', str(i), '\t\tLEN:', str(lenn),'\t\tABUNDANCE: ', str(x[0]), '\n']) #x[1] would give you the sequence 
			outfile.write(outstring)
			totalReads += x[0]
			i += 1
	
	totaltally =  ''.join(['\nTotal Reads:', str(totalReads) ,'\nTotal Distinct Sequences:', str(i-1)])
	print '\nOutput printed to file %s \n %s' % (outf ,totaltally)
	outfile.write(totaltally)
	
	outfile.close()
	
if __name__ == '__main__':
	main()		
	