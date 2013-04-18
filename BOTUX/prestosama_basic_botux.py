#Melissa Prestosa

import sys
import re
import os
import operator
import argparse

otuList = [] #global variable
seqNames = {}
screenSplit = '---------------------------------------------------\n'

def makeWordList(sequence, wordLen):
	list = []
	for pos in xrange(len(sequence) - (wordLen + 1)):
		word = sequence[pos:pos + wordLen]
		list.append(word)	
	return list

def makeNewOtu(sequence, abund, wordList):
	list = [] 
	nameScoreDict = {}
	#list[0] = the seed sequence 
	#list[1] = dict of words
	#list[2] = number of READS in that OTU
	#list[3] = dict where header line = read name and value = score of seq when added(as a float) (which will be assigned later. if = 1 then it was seed sequence)
	list.append(sequence)
	wordDict = {}
	for word in wordList:
		if word in wordDict:
			wordDict[word] += abund
		else: 
			wordDict[word] = abund
	list.append(wordDict)
	list.append(abund)
	
	for header in seqNames[sequence]:
		nameScoreDict[header] = 1		
	
	list.append(nameScoreDict)
	otuList.append(list)

def updateExistingOtu(posOfOTUtoUpdate, score, abund, seq, wordList):
	for word in wordList:
		if word in otuList[posOfOTUtoUpdate][1]:
			otuList[posOfOTUtoUpdate][1][word] += abund
		else:
			otuList[posOfOTUtoUpdate][1][word] = abund
	
	otuList[posOfOTUtoUpdate][2] +=abund
	
	for header in seqNames[seq]:
		otuList[posOfOTUtoUpdate][3][header] = score	
	
def scoreOTUs(seqSequence, wordList):
	bestScore = [-999,-999] #bestScore[0] = position of OTU; bestScore[1] = score
	
	for index, otu in enumerate(otuList):
		sumScoreforOTU = float(0)
		
		totalWordsinCurrentOTU = sum(otu[1].itervalues()) 
		
		for seqWord in wordList:
			if seqWord in otu[1]:
				freqofWi = otu[1][seqWord]
				currentScoreforWi = (float(freqofWi)/float(totalWordsinCurrentOTU)) 
				sumScoreforOTU += currentScoreforWi			
				
			else:
				#word does not exist in OTU
				pass


		sumScoreforOTU = sumScoreforOTU * (float(len(otu[0]))/float(len(seqSequence)))
		if sumScoreforOTU >= bestScore[1]:
			bestScore[0] = index
			bestScore[1] = sumScoreforOTU
			
	return bestScore				
	
def main ():

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
		
	outSeed = 'MAP_OTU_seed.txt'
	outFreq = 'MAP_OTU_frequency.txt'
	outAssign = 'MAP_OTU_assignment.txt'
	outWord = 'MAP_OTU_word.txt'
	
	lenAbunD = {}
	readInCounter = 0
	header = ''
	subseqList = []
	wholeSeq = ''	
	
	fastafile = open(infile)	
	line = fastafile.readline().strip()
	
	while line != '':
		readInCounter += 1
		match = re.search(r'^\>.',line)
		if match:
			if header != '':
				wholeSeq = ''.join(subseqList)
				length = len(wholeSeq)
				
				if trimlen != -1 and length > trimlen: 
					wholeSeq = wholeSeq[:trimlen]
					length = len(wholeSeq)							
			
				if wholeSeq in seqNames:
					seqNames[wholeSeq].append(header)
				else:
					seqNames[wholeSeq] = [header]				
				
				if length in lenAbunD: #if seqWord in otu[1]:
					if wholeSeq in lenAbunD[length]: #if seqWord in otu[1]:
						lenAbunD[length][wholeSeq] += 1
					else:
						lenAbunD[length][wholeSeq] = 1
				else:
					lenAbunD[length] = {}
					lenAbunD[length][wholeSeq] = 1	
			
			header = line[1:]
			subseqList = []
		else:
			subseqList.append(line)		
		
		line = fastafile.readline().strip()
	
	wholeSeq = ''.join(subseqList)
	length = len(wholeSeq)
	
	if trimlen != -1 and length > trimlen: 
		wholeSeq = wholeSeq[:trimlen]
		length = len(wholeSeq)
	
	if length in lenAbunD: #if seqWord in otu[1]:
		if wholeSeq in lenAbunD[length]: #if seqWord in otu[1]:
			lenAbunD[length][wholeSeq] += 1
		else:
			lenAbunD[length][wholeSeq] = 1
	else:
		lenAbunD[length] = {}
		lenAbunD[length][wholeSeq] = 1	
		
	if wholeSeq in seqNames:
		seqNames[wholeSeq].append(header)
	else:
		seqNames[wholeSeq] = [header]
		
		
	fastafile.close()
	
	

	totalReads = 0
	totalSeq = 0	
	
	for lenn in sorted(lenAbunD.keys(), reverse=True):
		items = sorted([(v, k) for k, v in lenAbunD[lenn].items()], reverse=True)
		##makes dict into tuples NOW THE TUPLES ARE IN THE ORDER (abun, seq)!!!
		
		for x in items:
			#x[0] give you abund
			#x[1] gives you the seq
			currSeqWordL = makeWordList(x[1],wordLen)
							
			if otuList == []:
				#first seq
				makeNewOtu(x[1], x[0], currSeqWordL)				
			
			else:	
				best = scoreOTUs(x[1], currSeqWordL) 
				#scoreOTUs returns a list of length two with best[0] being pos of best otu best[1] being best score
				#print "best =", best
				#print best[1]
				#print threshold

				if best[1] >= threshold:
					updateExistingOtu(best[0], best[1], x[0], x[1], currSeqWordL)
				else:
					makeNewOtu(x[1], x[0], currSeqWordL)	

			totalReads += x[0]
			totalSeq += 1
				
				
	
	outSeedFH = open(outSeed, 'w')
	outFreqFH = open(outFreq, 'w')
	outAssignFH = open(outAssign, 'w')
	outWordFH = open(outWord, 'w')

	
	for index, otu in enumerate(otuList):		
		
		sumOfScores = 0
		seedSeq = otu[0]		
		outSeedFH.write(''.join(['OTU', str(index+1),'\t', seedSeq, '\n'])) #for OTU_seed.txt
				
		for read in otu[3]:
			sumOfScores += otu[3][read]
			outAssignFH.write(''.join([read, '\t', 'OTU', str(index+1),'\t', str(otu[3][read]),'\n'])) #for OTU_assignment.txt
		
		avgScore = sumOfScores / otu[2]
		outFreqFH.write(''.join(['OTU', str(index+1),'\t', str(otu[2]), '\t', str(avgScore), '\n'])) #for OTU_frequency.txt
	
		words = sorted([(v, k) for k, v in otu[1].items()], reverse=True)
		for word in words:
			outWordFH.write(''.join(['OTU', str(index+1), '\t', word[1], '\t', str(word[0]), '\n']))	
		
		totalWordsinCurrentOTU = sum(otu[1].itervalues()) 
		outWordFH.write(''.join(['OTU', str(index+1),' total\t', str(totalWordsinCurrentOTU), '\n']))
	
	outSeedFH.close()
	outAssignFH.close()
	outFreqFH.close()
	outWordFH.close()

if __name__ == '__main__':
	main()		
	
