#Yahya Bokhari 03-22-2013
#!/usr/bin/python -tt
#program to 
#Input:
#OUTPUT:

from __future__ import division
import sys
import os
import re
from string import *

def Dic(dic,tax,myAccession,start,end,binCounter):
	#print tax,myAccession,start,end,binCounter
	startEnd=str(start)+".."+str(end)
	#print startEnd
	if dic.has_key(tax):
		if dic[tax].has_key(myAccession):
			print tax,myAccession,start,end,binCounter
			dic[tax][myAccession][binCounter]=startEnd
	else:
		dic[tax]={}
		dic[tax][myAccession]={}
		dic[tax][myAccession][binCounter]=startEnd
def read1(myMap,mapFile):
	mp=open(mapFile, 'rU')
	for l in  mp:
		m = re.search('(\w+)\s(\w+)', l)
		#print m.group(1)
		#print m.group(2)
		accession= m.group(1)
		tax=m.group(2)
		myMap[accession]=tax
	#print myMap


def read2(dic,binSize,filename,myMap,output):
	f=open(filename, 'rU')
	o=open(output,'w')
	start=1 # where the first bin starts
	binCounter=1
	myTax=0
	t=0
	header="Tax_id"+"\t"+"Accession"+"\t"+"Seq_Start"+"\t"+"Seq_End"+"\t"+"bin_number"
	print >> o,header

	for line in f:
		#print line
		m = re.search('[>]\w+[|](\w+)', line)
		if m:
			binCounter=1
			print m.group(1)
			myAccession=m.group(1)
			myTax=t
			t=myMap[myAccession]
			if myTax!=t:
				binCounter=1
		else:
			length=len(line)  # length of the sequence
			iterate=length/binSize   #the loop depends on the bin size
			leftOver=iterate-int(iterate)  # reminder of length/binSize
			leftOver=int(leftOver*binSize)
			iterate=int(iterate)  # the float part will be taking care off later.
			print "length:",length,", BinSize:", binSize,", iterate", iterate,", leftOver", leftOver
				
			for i in range (0,iterate):
				end=start+binSize-1  #where the bin ends
				
				myStr=str(t)+"\t"+str(myAccession)+"\t"+str(start)+"\t"+str(end)+"\t"+str(binCounter)
				print >> o,myStr
				start+=binSize
				binCounter+=1

			if leftOver>binSize/2:
				end=end+leftOver
				myStr=str(t)+"\t"+str(myAccession)+"\t"+str(start)+"\t"+str(end)+"\t"+str(binCounter)
				print >> o,myStr
				binCounter+=1		
				
			else :
				start=start-binSize
				end =end+leftOver
				binCounter=binCounter-1
				myStr=str(t)+"\t"+str(myAccession)+"\t"+str(start)+"\t"+str(end)+"\t"+str(binCounter)
				print >> o,myStr
				#print tax,myAccession,start,end,binCounter		
			#print dic
		


def main():
	if len(sys.argv) < 5:
		print "USAGE: python sys.argv[0] 1- Input fna File 2- bin Size 3- gi maping tax file 4- outputfile \n"
		sys.exit()
	inFna = sys.argv[1]
	binSize =int( sys.argv[2])
	inMap = sys.argv[3]
	output = sys.argv[4]
	dic={}
	myMap={}
	read1(myMap,inMap)
	read2(dic,binSize,inFna,myMap,output)


if __name__ == '__main__':
	main()