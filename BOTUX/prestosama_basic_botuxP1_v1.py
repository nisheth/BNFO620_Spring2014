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
	
	fastafile = open(infile)
	line = fastafile.readline().strip()
	while line != '':
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
		
	fastafile.close()

	i=1
	totalReads = 0
	
	for lenn in sorted(lenAbunD.keys(), reverse=True):
		print '------------------------------------------------------------'
		tempD = lenAbunD[lenn]			#this returns a dictionary where the keys are seq and the vales are abund
		
		items = [(v, k) for k, v in tempD.items()]
		items.sort()
		items.reverse()             # so largest is first
		items = [(k, v) for v, k in items]
		
		for x in items:
			print 'SEQ NUMB:', i, '\tLENGTH', lenn,'\tAbundance', x[1] #x[0] would give you the sequence 
			totalReads += x[1]
			i += 1
	
	print 'total reads:', totalReads
if __name__ == '__main__':
	main()		
	