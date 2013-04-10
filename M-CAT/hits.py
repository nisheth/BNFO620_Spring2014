from __future__ import division
import sys
import os
import re
from string import *

def storeThebin(bin,binDic,taxAcc):
	f=open(bin, 'rU')
	for line in f:
		m = re.search ('(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
		if m:
			m1=m.group(1)  
			m2= m.group(2)
			m3= m.group(3)  
			m4= m.group(4)  
			m5=m.group(5) 
			#print m1, m2, m3 , m4 #debug
			startEnd=m3+"_"+m4
			if m1 in binDic:
				binDic[m1]={startEnd:m5}
			else:
				binDic[m1]={}

			if m2 not in taxAcc:
				taxAcc[m2] = m1
def countCigar(cigar):
	count=0
	tuples1 =re.findall(r'([0-9]+)([A-Z]+)',cigar) # puting the pattern in tuple
	#print tuples1
	for tuple in tuples1:
		count+=int(tuple[0])
	return count
def countMD(MD):
	count=0
	gap=0
	tuples2 =re.findall(r'([0-9]+)([A-Z]|\^[A-Z]+)',MD)  # puting the pattern in tupe
	#print tuples2
	for tuple in tuples2:
		count+=1

		de=re.search('\^(.+)',tuple[1])  #check if we have deletion
		if de:
			count-=1
			gap=len(de.group())-1
			#print len(de.group())-1
	count=count+gap

	return count 

def percentRule(hitsPerRead):
	highist=0
	#for key, value in sorted (hitsPerRead.iteritems(), key=lambda (k,v): (v,k)):
		#print "%s: %s" % (key, value)

	for key, value in hitsPerRead.items(): # returns the dictionary as a list of value pairs -- a tuple.
		if value>highist:
			highist=value
		highist=highist-.05
	for key, value in hitsPerRead.items(): # returns the dictionary as a list of value pairs -- a tupl
		if highist>value:
			del hitsPerRead[key]

	#print highist
	return hitsPerRead
def Foutput(binDic,hitsPerRead,output):
	count=0
	o=open(output,'w')
	print >> o, "Tax"+"\t"+"Bin"+"\t"+"count"
	for key, value in hitsPerRead.items(): 
		m = re.search('-(\d+)', key)
		hitStart=m.group(1)
		#print hitStart
		for key1, value1 in binDic.items(): 
			for key2, value2 in value1.items():
				#print key2
				m2= re.search('(\d+)-(\d+)', key)
				if hitStart> m2.group(1) and hitStart<m2.group(2):
					count+=1
	print >>o, key+"\t"+value2+"\t"+str(count)

def read(binDic,inSAM,output):
	f=open(inSAM, 'rU')
	#open(output,'w')
	hitsPerRead={}
	hashCount=1
	tempTax=None 
	for line in f:
		cigarCount=0
		MDcount=0
		score=0
		#print line
		m = re.search('gi\S(\d+).+gi\S(\d+).+\s+(\d+)\s+\d+\s+(\w+)\s+[*].+MD:Z:([0-9]+(([A-Z]|\^[A-Z]+)[0-9]+)*)', line)
		tax=m.group(1) 
		tax2= (m.group(2))  
		start = (m.group(3)) 
		cigar= (m.group(4))  
		MD= m.group(5)  
		#print tax,tax2,start,cigar,MD
		cigarCount=countCigar(cigar)
		#print cigarCount
		MDcount=countMD(MD)
		#print MDcount
		score=(cigarCount-MDcount)/cigarCount
		#print score


		if not tempTax:
			tempTax = tax
		if tax != tempTax:
			hitsPerRead=percentRule(hitsPerRead) 
			Foutput(binDic,hitsPerRead,output)
			hitsPerRead={}

		else:
			#tax=tax+"-"+str(hashCount)
			tax=tax+"-"+start
			hitsPerRead[tax]=score
			hashCount+=1
			#percentRule(hitsPerRead) 


def main():
	if len(sys.argv) < 4 :
		print "USAGE: python sys.argv[0] 1-Input_SAM_File 2-bin_file 3-Output"
		sys.exit()
	inSAM = sys.argv[1]
	bin = sys.argv[2]
	output = sys.argv[3]
	binDic={}
	taxAcc={}
	storeThebin(bin,binDic,taxAcc)
	read(binDic,inSAM,output)

if __name__ == '__main__':
	main()