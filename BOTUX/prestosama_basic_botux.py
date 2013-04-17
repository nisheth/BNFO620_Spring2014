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
	#assuming word size 8
	list = []
	for pos in xrange(len(sequence) - (wordLen + 1)):
		#print pos , len(sequence)
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
			#print 'word exists:' , word
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
		#print totalWordsinCurrentOTU		
		
		for seqWord in wordList:
			if seqWord in otu[1]:
				freqofWi = otu[1][seqWord]
				currentScoreforWi = (float(freqofWi)/float(totalWordsinCurrentOTU)) 
				#print currentScoreforWi				
				sumScoreforOTU += currentScoreforWi			
				
			else:
				#word does not exist in OTU
				pass

		#print screenSplit
		#print 'OTU', index, 'Score', sumScoreforOTU , 'seed', len(otu[0]),'currSeq', len(seqSequence)

		sumScoreforOTU = sumScoreforOTU * (float(len(otu[0]))/float(len(seqSequence)))
		if sumScoreforOTU >= bestScore[1]:
			#print 'replacing best score', bestScore[1], 'with new score', sumScoreforOTU
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
	
	fastafile = open(infile)	
	header = ''
	subseqList = []
	wholeSeq = ''
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
		
		
		#if readInCounter%1000 == 0:
			#print 'read %s lines from file %s' %(readInCounter, infile)
			
		
	fastafile.close()

	totalSeq=0
	totalReads = 0
	
	
	for lenn in sorted(lenAbunD.keys(), reverse=True):
		#outfile.write(outline)		
		items = sorted([(v, k) for k, v in lenAbunD[lenn].items()], reverse=True)
		##makes dict into tuples NOW THE TUPLES ARE IN THE ORDER (abun, seq)!!!
		
		for x in items:
			#outstring = ''.join(['SEQ NUM: ', str(i), '\t\tLEN:', str(lenn),'\t\tABUNDANCE: ', str(x[0]), '\n']) #x[1] would give you the sequence 
			#x[0] give you abund
			#x[1] gives you the seq
			currSeqWordL = makeWordList(x[1],wordLen)
							
			if otuList == []:
				#print 'yes otuList is empty'
				#first seq
				makeNewOtu(x[1], x[0], currSeqWordL)				
			
			else:				
				#print '\n\nSeq #', totalSeq
				best = scoreOTUs(x[1], currSeqWordL) 
				#scoreOTUs returns a list of length two with best[0] being pos of best otu best[1] being best score
				#print "best =", best
				#print best[1]
				#print threshold

				if best[1] >= threshold:
					#print "updating"
					updateExistingOtu(best[0], best[1], x[0], x[1], currSeqWordL)
				else:
					makeNewOtu(x[1], x[0], currSeqWordL)	

			totalReads += x[0]
			totalSeq += 1
				
				
	otusum = 0
	
	outS = open(outSeed, 'w')
	outF = open(outFreq, 'w')
	outA = open(outAssign, 'w')
	outW = open(outWord, 'w')
	#print '\n\nOTU\tFirst 8 nt \t Number of Reads in OTU'
	#outfile.write('OTU\tFirst 8 nt \t Number of Reads in OTU\n\n')
	
	for index, otu in enumerate(otuList):		
		
		sumOfScores = 0
		seedSeq = otu[0]		
		outS.write(''.join(['OTU', str(index+1),'\t', seedSeq, '\n'])) #for OTU_seed.txt
				
		for read in otu[3]:
			#print read , otu[3][read]
			sumOfScores += otu[3][read]
			outA.write(''.join([read, '\t', 'OTU', str(index+1),'\t', str(otu[3][read]),'\n'])) #for OTU_assignment.txt
		
		#print 'sum ', sumOfScores
		avgScore = sumOfScores / otu[2]
		outF.write(''.join(['OTU', str(index+1),'\t', str(otu[2]), '\t', str(avgScore), '\n'])) #for OTU_frequency.txt
	
		for word in otu[1]:
			outW.write(''.join(['OTU', str(index+1), '\t', word, '\t', str(otu[1][word]), '\n']))
	
		
		totalWordsinCurrentOTU = sum(otu[1].itervalues()) 
		outW.write(''.join(['OTU', str(index+1),' total\t', str(totalWordsinCurrentOTU), '\n']))
	
	outS.close()
	outA.close()
	outF.close()
	outW.close()
	#print 'totalReads', totalReads, '\ttotalSeq', totalSeq, '\tsum of OTUs', otusum
	#outfile.write(''.join(['\n','totalReads  ', str(totalReads), '\ttotalSeq  ', str(totalSeq), '\tSum of reads in OTUs  ', str(otusum)]))
	# print '\n\n'
	# for seq in seqNames:
		# print seqNames[seq]
		# print '\n'
	
	
if __name__ == '__main__':
	main()		
	
