from __future__ import division
import sys
import os
import re
from string import *
########################################################
#This method read the bin file created and store it hash
#bin file look like:
#Tax_id	Accession	Seq_Start	Seq_End	bin_number
#240016	164421336	1	1000	1
#240016	164421336	1001	2000	2
#240016	164421336	2001	3000	3
#240016	164421336	3001	4000	4
#240016	164421336	4001	5000	5
#240016	164421336	5001	6000	6
########################################################
def storeThebin(bin,binDic,taxAcc):
	f=open(bin, 'rU')
	for line in f:
		#print line
		m = re.search ('(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
		if m:
			m1=m.group(1)  
			m2= m.group(2)
			m3= m.group(3)  
			m4= m.group(4)  
			m5=m.group(5) 
			#print m1, m2, m3 , m4 #debug
			startEnd=m3+"_"+m4
			if m2 in binDic:
				binDic[m2][startEnd]=m5
			else:
				binDic[m2]={}
				binDic[m2][startEnd]=m5

			if m2 not in taxAcc:
				taxAcc[m2] = m1
#########################################################################
#output the length of the read using the Cigar String
#Ex: 98M2S, 100M, 58M1I41M
##########################################################################
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
#########################################################################
#This method take teh highst percent score hit for a given Tax ID and 
#substract 5% from it and then dicard any score below that that percent
#Ex: 
##########################################################################
def percentRule(hitsPerRead):
	highist=0
	#for key, value in sorted (hitsPerRead.iteritems(), key=lambda (k,v): (v,k)):
		#print "%s: %s" % (key, value)

	for key, value in hitsPerRead.items(): # returns the dictionary as a list of value pairs -- a tuple.
		if value>highist:
			highist=value
		highist=highist-.05
	for key, value in hitsPerRead.items(): # returns the dictionary as a list of value pairs -- a tuple
		if highist>value:
			del hitsPerRead[key]
	#print highist
	#print "hitsPerRead",hitsPerRead
	return hitsPerRead
##########################################################################
#This is just an output method
#Ex:	 Tax	   Bin	 count
#		57650036	6492	1
##########################################################################
def FinalOutput(taxAcc,binDic,hitsPerRead,o):
	#print binDic
	count=0
	taxInBin=0
	accessionNo=None
	#print hitsPerRead
	for key, value in hitsPerRead.items(): 
		m = re.search('(\d+)-(\d+)', key)
		accessionNo=m.group(1)
		hitStart=m.group(2)
		taxInBin=taxAcc[accessionNo]
		#print taxInBin, "=taxInBin"
		#print "hitStart=", hitStart
		#for key1, value1 in binDic.items(): 
		#for value1 in binDic.iterkeys():
		#for value1 in binDic.itervalues():
		for key1, value1 in binDic.items():
			if (accessionNo==key1):
				for key2 in value1.iterkeys():
					#print "key1=",key1," value1=",value1," key2=",key2
					m2= re.search('(\d+)_(\d+)', key2)
					s=m2.group(1)
					e=m2.group(2)
					#print "start= ",s,"end= ",e
					#print "hitStart=", hitStart
					if int(hitStart)>= int(s) and int(hitStart)<int(e):
						#print "start= ",s,"end= ",e
						#print "hitStart=", hitStart
						count+=1
						break
						#print count,"hit"
	print >>o, str(taxInBin)+"\t"+str(accessionNo)+"\t"+str(count)
############################################################################################################################################
#This method  Read  the sam file and call the other methods to anlyze it
#Ex: gi|57650036|ref|NC_002951.2|_571308_571841_2:0:0_2:0:0_2bb6/2	16	gi|297207379|ref|NZ_ADVP01000001.1|	1915	1	100M	*	
#0	0	TAAAAATCTACACCAGTAGCTTCTTTTACAGTATCAACAATATACAAACGAGTCCAAGCAGATTCTAAATCAATCGTTTCCCCATTGTATTGTACTTTTG	
#2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222	AS:i:190	
#XS:i:190	XN:i:0	XM:i:2	XO:i:0	XG:i:0	NM:i:2	MD:Z:31C11G56	YT:Z:UU
############################################################################################################################################
def read(taxAcc,binDic,inSAM,output):
	f=open(inSAM, 'rU')
	o=open(output,'w')
	print >> o, "Tax"+"\t"+"Bin"+"\t"+"count"
	hitsPerRead={}
	hashCount=1
	b=0
	tempTax=None
	for line in f:
		#
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


		#if not tempTax:
			#tempTax = tax2
		#print tempTax, tax, b
		if tax != tempTax and b==1:
			hitsPerRead=percentRule(hitsPerRead) 
			#print hitsPerRead
			FinalOutput(taxAcc,binDic,hitsPerRead,o)
			hitsPerRead={}
			hashCount=1
			tempTax = tax
			hitsPerRead[tax+"-"+start]=score
			hashCount+=1
			b=0
			
#keep reading the sam file untill new new accessionz
		else:
			tempTax = tax
			hitsPerRead[tax+"-"+start]=score
			hashCount+=1
			b=1
			#percentRule(hitsPerRead) 
	FinalOutput(taxAcc,binDic,hitsPerRead,o)



def main():
	if len(sys.argv) < 4 :
		print "USAGE: python sys.argv[0] 1-Input_SAM_File 2-bin_file 3-Output_file_name"
		sys.exit()
	inSAM = sys.argv[1]
	bin = sys.argv[2]
	output = sys.argv[3]
	binDic={}
	taxAcc={}
	storeThebin(bin,binDic,taxAcc)
	read(taxAcc,binDic,inSAM,output)

if __name__ == '__main__':
	main()