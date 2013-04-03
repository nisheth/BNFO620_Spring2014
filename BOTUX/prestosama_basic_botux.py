#Melissa Prestosa

import sys
import re
import os
import operator
import argparse

otuList = [] #global variable
screenSplit = '---------------------------------------------------'

def makeWordList(sequence, wordLen):
	#assuming word size 8
	list = []
	for pos in xrange(len(sequence) - (wordLen + 1)):
		#print pos , len(sequence)
		word = sequence[pos:pos + wordLen]
		list.append(word)	
	return list

def makeNewOtu(sequence, wordList):
	list = [] #I want element 0 to be the seed sequence and element 1 to be a dict of words element 2 to be number of sequences in that OTU
	list.append(sequence)
	wordDict = {}
	for word in wordList:
		if word in wordDict:
			#print 'word exists:' , word
			wordDict[word] += 1
		else: 
			wordDict[word] = 1
	list.append(wordDict)
	list.append(1)
	otuList.append(list)

def updateExistingOtu(posOfOTUtoUpdate, wordList):
	for word in wordList:
		if word in otuList[posOfOTUtoUpdate][1]:
			otuList[posOfOTUtoUpdate][1][word] += 1
		else:
			otuList[posOfOTUtoUpdate][1][word] = 1
	otuList[posOfOTUtoUpdate][2] +=1
	
def scoreOTUs(seqSequence, wordList):
	bestScore = [-999,-999] #bestScore[0] = position of OTU; bestScore[1] = score
	
	for index, otu in enumerate(otuList):
		sumScoreforOTU = 0
		
		totalWordsinCurrentOTU = sum(otu[1].itervalues()) 
		#print totalWordsinCurrentOTU		
		
		for seqWord in wordList:
			if seqWord in otu[1]:
				freqofWi = otu[1][seqWord]
				currentScoreforWi = ((float(freqofWi)/float(totalWordsinCurrentOTU)) * (float(len(otu[0]))/float(len(seqSequence))))
				#print currentScoreforWi
				
				sumScoreforOTU += currentScoreforWi				
			else:
				#word does not exist in OTU
				pass

		#print screenSplit
		#print 'OTU', index, 'Score', sumScoreforOTU , 'seed', len(otu[0]),'currSeq', len(seqSequence)

		if sumScoreforOTU >= bestScore[1]:
			#print 'replacing best score', bestScore[1], 'with new score', sumScoreforOTU
			bestScore[0] = index
			bestScore[1] = sumScoreforOTU
			
	return bestScore				
	
def main ():
#	if len(sys.argv) < 3:
#		print "Please input fasta file, threshold (as a percentage), and trimlength if using"
#		sys.exit(0)
	
#	if len(sys.argv) == 4:
#		infile = sys.argv[1]
#		threshold = float(sys.argv[2])
#		trimlen = int(sys.argv[3])
#		wordLen = 8
#	else:
#		infile = sys.argv[1]
#		threshold = float(sys.argv[2])
#		trimlen = -1
#		wordLen = 8
	
	parser = argparse.ArgumentParser(description = 'BOTUX - write better description later')
	parser.add_argument('-l','--trimlen', help='Specify trim length', required = False, type = int, default = -1)
	parser.add_argument('-t','--threshold', help='Minimum threshold score (as a percentage - ie. for 80% enter .8) for assigning sequence for OTU', required = False, type = float, default = 0.65)
	parser.add_argument('-i','--infile', help='full path to fasta file -- right now only takes fasta', required = True)
	parser.add_argument('-w','--wordLen', help='word size', required = False, type = int, default = 8) 
	
	args = parser.parse_args()
	
	infile = args.infile
	threshold = args.threshold
	wordLen = args.wordLen
	trimlen = args.trimlen
	
	
	outf = 'sorted_by_abundance_and_length.txt'
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
			if length in lenAbunD: #if seqWord in otu[1]:
				if line in lenAbunD[length]: #if seqWord in otu[1]:
					lenAbunD[length][line] += 1
				else:
					lenAbunD[length][line] = 1
			else:
				lenAbunD[length] = {}
				lenAbunD[length][line] = 1				
		
		line = fastafile.readline().strip()
		#if readInCounter%1000 == 0:
			#print 'read %s lines from file %s' %(readInCounter, infile)
			
		
	fastafile.close()

	totalSeq=1
	totalReads = 0
	
	
	for lenn in sorted(lenAbunD.keys(), reverse=True):
		#outfile.write(outline)		
		items = sorted([(v, k) for k, v in lenAbunD[lenn].items()], reverse=True) ##makes dict into tuples NOW THE TUPLES ARE IN THE ORDER (abun, seq)!!!
		
		for x in items:
			#outstring = ''.join(['SEQ NUM: ', str(i), '\t\tLEN:', str(lenn),'\t\tABUNDANCE: ', str(x[0]), '\n']) #x[1] would give you the sequence 
			currSeqWordL = makeWordList(x[1],wordLen)
							
			if otuList == []:
				#print 'yes otuList is empty'
				#first seq
				makeNewOtu(x[1],currSeqWordL)				
			
			else:				
				#print '\n\nSeq #', totalSeq
				best = scoreOTUs(x[1], currSeqWordL) 
				#print "best =", best
				#print best[1]
				#print threshold
				#scoreOTUs returns a list of length two with x[0] being pos of best otu x[1] being best score
				if best[1] >= threshold:
					#print "updating"
					updateExistingOtu(best[0],currSeqWordL)
				else:
					makeNewOtu(x[1],currSeqWordL)	

			totalReads += x[0]
			totalSeq += 1
				
				
	print '\n\nOTU\tFirst 8 nt\t Last 8 nt \t Number of Seq in OTU'
	for index, otu in enumerate(otuList):
		seq = otu[0]
		print index,'\t', seq[:8],'\t', seq[-8:], '\t', otu[2]		

	
if __name__ == '__main__':
	main()		
	
