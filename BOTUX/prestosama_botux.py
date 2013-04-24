#Melissa Prestosa
	
#BOTUX - write better discription later!

import sys
import re
import os
import operator
import argparse
import collections

seqDict = {}
otuList = []

def sortDictByValue(dict):
	return collections.OrderedDict(sorted(seqDict.items(), key = lambda t: t[1], reverse=True))
#end of def sortDictByValue

def setUpParser():
	"""
	Parse in user input
	"""
	parser = argparse.ArgumentParser(description = 'BOTUX - write better description later')
	parser.add_argument('-l','--trimLen', help = 'Specify trim length', required = False, type = int, default = -1)
	parser.add_argument('-t','--threshold', help = 'Minimum threshold score (as a percentage - ie. for 80% enter .8) for assigning sequence for OTU', required = False, type = float, default = 0.65)
	parser.add_argument('-i','--infile', help = 'full path to fasta file -if you want fastq file use flag -fq', required = True)
	parser.add_argument('-fq','--fastq', help = 'use this flag if the input file is a fastq file', required = False, action = 'store_true', default = False) 
	parser.add_argument('-w','--wordLen', help = 'word size', required = False, type = int, default = 8) 
		
	parsed = parser.parse_args()	
	return parsed
#end of def setUpParser

def readFastaFile(iFH, trimLen):
	readID = ''	
	line = iFH.readline().strip()
		
	while line != '':
		match = re.search(r'^\>.', line)
		if match: 							#defline
			if readID == '': 				#first time 
				readID = line[1:]
			else:							#process previous sequence							
				"""start of seq processing"""
				wholeSeq = ''.join(subSeqList)							
				if trimLen != -1 and len(wholeSeq) > trimLen:
					wholeSeq = wholeSeq[:trimLen]
				
				if wholeSeq in seqDict:
					seqDict[wholeSeq].update(readID)
				else:
					seqObj = Sequence(wholeSeq,readID)
					seqDict[wholeSeq] = seqObj
				
				""" end of seq processing """
				readID = line[1:]			#replace previous read ID with new read ID				
			subSeqList = []
		#end if match	
		
		else:
			subSeqList.append(line)			#add line to subSeqList 
		line = iFH.readline().strip()
	#end while line != ''
	
	"""start of seq processing"""
	wholeSeq = ''.join(subSeqList)							
	if trimLen != -1 and len(wholeSeq) > trimLen:
		wholeSeq = wholeSeq[:trimLen]
				
	if wholeSeq in seqDict:
		seqDict[wholeSeq].update(readID)
	else:
		seqObj = Sequence(wholeSeq,readID)
		seqDict[wholeSeq] = seqObj
	""" end of seq processing """
		
#end of def readFastaFile
	
def readFastqFile(iFH, trimLen):
	counter = 0 
	line = iFH.readline().strip()
	
	while line != '':
		counter += 1
		if counter%4 == 1: 					#defline
			readID = line[1:]
		if counter%4 == 2:					#seqline
			wholeSeq = line
			if trimLen != -1 and len(wholeSeq) > trimLen:
				wholeSeq = wholeSeq[:trimLen]
			
			"""start of seq processing"""		
			if trimLen != -1 and len(wholeSeq) > trimLen:
				wholeSeq = wholeSeq[:trimLen]
				
			if wholeSeq in seqDict:
				seqDict[wholeSeq].update(readID)
			else:
				seqObj = Sequence(wholeSeq,readID)
				seqDict[wholeSeq] = seqObj
			""" end of seq processing """	
				
		line = iFH.readline().strip()
	#end of while != ''
#end of def readFastqFile	

def checkThreshold(thresh):
	if thresh > 1 or thresh < 0:
		print 'Please enter threshold as a percentage (between 0 and 1)'
		sys.exit()
#end of def checkThreshold

def makeWordList(seqObj, wordLen):
	list = []
	for pos in xrange(len(seqObj) -(wordLen +1)):
		word = seqObj.sequence[pos : pos + wordLen]
		list.append(word)
	return list
#end of def makeWordList

def scoreSeq(seqWordList, seqObj):
	bestScore = [-1,-1] #bestScore[0] = position of OTU, bestScore[1] = score
	
	for index, otu in enumerate(otuList):
		sumScoreForOTU = 0
		#totalWordsinCurrentOTU = sum(otu[1].itervalues())				#no longer necessary 
		for seqWord in seqWordList:
			if seqWord in otu.wordDict:
				freqofWi = otu.wordDict[seqWord]
				scoreforWi = (float(freqofWi)/float(otu.totalWords)) 
				sumScoreForOTU += scoreforWi		
			else:
				#word does not exist in OTU
				pass
	
		sumScoreForOTU = sumScoreForOTU * (float(len(otu.seedSeq))/float(len(seqObj.sequence)))
		
		if sumScoreForOTU >= bestScore[1]:
			bestScore[0] = index
			bestScore[1] = sumScoreForOTU
	
	return bestScore
#end of def scoreSeq

class Sequence:
	def __init__(self, seq, readID):
		self.sequence = seq
		self.abundance = 1
		self.length = len(seq)
		self.readIDList = [readID]		
	
	def update(self, readID):
		self.abundance += 1
		(self.readIDList).append(readID)
	
	def __len__(self):
		return self.length
	
	def __lt__(self, other):
		if self.length == other.length:
			return self.abundance < other.abundance
		else:
			return self.length < other.length
	
	def __gt__(self, other):
		if self.length == other.length:
			return self.abundance > other.abundance
		else:
			return self.length > other.length
	
	def __eq__(self, other):
		if self.length == other.length:
			return self.abundance == other.abundance
		else:
			return self.length == other.length
#end class Sequence

class OTU:
	def __init__(self, seedSeq, abund, readIDList, wordList):
		self.seedSeq = seedSeq
		self.noOfReads = abund
		self.wordDict = {}
		self.totalWords = 0
		self.ReadIDScoreDict = {}
		
		for word in wordList:
			if word in self.wordDict:
				self.wordDict[word] += abund
				self.totalWords += 1
			else:
				self.wordDict[word] = abund
				self.totalWords += 1
		
		for readID in readIDList:
			self.ReadIDScoreDict[readID] = 1				
		
	def update(self, wordList, seqObj, score):
		for word in wordList:
			if word in self.wordDict:
				self.wordDict[word] += seqObj.abundance
				self.totalWords += 1
			else:
				self.wordDict[word] = seqObj.abundance
				self.totalWords += 1
		
		self.noOfReads += seqObj.abundance
		
		for readID in seqObj.readIDList:
			self.ReadIDScoreDict[readID] = score
		
	
	
def main ():	
	args = setUpParser()	
	infile = args.infile
	threshold = args.threshold
	wordLen = args.wordLen
	trimLen = args.trimLen
	fastq = args.fastq
	
	checkThreshold(threshold)
	
	"""
	Outfiles	
	"""
	outTest = 'outTest.txt'
	outT2 = 'outT2.txt'
	outSeed = 'MAP_OTU_seed.txt'
	outFreq = 'MAP_OTU_frequency.txt'
	outAssign = 'MAP_OTU_assignment.txt'
	outWord = 'MAP_OTU_word.txt'
	
	iFH = open(infile)
	if fastq: #if fastq flag is true send to fastq parser
		readFastqFile(iFH, trimLen)
	
	else: #if fastq flag is false (thus a fasta file) send to fasta parser
		readFastaFile(iFH, trimLen)

	iFH.close()
	
	outTestFH = open(outTest,'w')
	outT2FH = open(outT2, 'w')
	
	sortedSeqDict = sortDictByValue(seqDict)
	
	counter = 0

	totalReads = 0
	totalSeq = 0
	
	for seq in sortedSeqDict:
		currSeqWordL = makeWordList(sortedSeqDict[seq], wordLen)
		
		if otuList == []:
			otuObj = OTU(sortedSeqDict[seq].sequence,sortedSeqDict[seq].abundance,sortedSeqDict[seq].readIDList,currSeqWordL)
			otuList.append(otuObj)
		else:
			best = scoreSeq(currSeqWordL, sortedSeqDict[seq])
			if best[1] >= threshold:
				otuList[best[0]].update(currSeqWordL, sortedSeqDict[seq], best[1])
			else:
				otuObj = OTU(sortedSeqDict[seq].sequence , sortedSeqDict[seq].abundance , sortedSeqDict[seq].readIDList , currSeqWordL)
				otuList.append(otuObj)
				
	#print otuList[0].wordDict
	outSeedFH = open(outSeed, 'w')
	outFreqFH = open(outFreq, 'w')
	outAssignFH = open(outAssign, 'w')
	outWordFH = open(outWord, 'w')

	for index, otu in enumerate(otuList):	
		
		sumOfScores = 0

		outSeedFH.write(''.join(['OTU', str(index+1),'\t', otu.seedSeq, '\n'])) #for OTU_seed.txt
				
		for read in otu.ReadIDScoreDict:
			sumOfScores += otu.ReadIDScoreDict[read]
			outAssignFH.write(''.join([read, '\t', 'OTU', str(index+1),'\t', str(otu.ReadIDScoreDict[read]),'\n'])) #for OTU_assignment.txt
		
		avgScore = sumOfScores / otu.noOfReads
		outFreqFH.write(''.join(['OTU', str(index+1),'\t', str(otu.noOfReads), '\t', str(avgScore), '\n'])) #for OTU_frequency.txt
	
		words = sorted([(v, k) for k, v in otu.wordDict.items()], reverse=True)
		for word in words:
			outWordFH.write(''.join(['OTU', str(index+1), '\t', word[1], '\t', str(word[0]), '\n']))	
		
		totalWordsinCurrentOTU = sum(otu.wordDict.itervalues()) 
		outWordFH.write(''.join(['OTU', str(index+1),' total\t', str(totalWordsinCurrentOTU), '\n']))
	
	outSeedFH.close()
	outAssignFH.close()
	outFreqFH.close()
	outWordFH.close()	
		
		
	""" test output code"""	
		# length = 0	
			# counter += 1
		# if counter < 10:
			# print '_________________________'
			#  print currSeqWordL
		
		# counter += 1
		# if len(sortedSeq[seq]) != length:
			# outTestFH.write('-----------------------------------------------------------\n')
		# outTestFH.write(''.join([str(counter),'\t',str(len(sortedSeq[seq])), '\t', str(sortedSeq[seq].abundance), '\n']))
		# length = len(sortedSeq[seq])
			
		
		# counter += 1
		# if len(s[0]) != length:
			# outTestFH.write('-----------------------------------------------------------\n')
		# # s[0] should be seqObj
		# outTestFH.write(''.join([str(counter),'\t',str(len(s[0])), '\t', str(s[0].abundance), '\n']))
		# outT2FH.write(' '.join(s[0].readIDList))
		# outT2FH.write('\n')
		# length = len(s[0])
	# # for seq in seqDict:
		# # print seqDict[seq].sequence, '\t', seqDict[seq].abundance, '\n', seqDict[seq].readIDList, '\n'
	""" test output code"""
	
	
if __name__ == '__main__':
    main()
