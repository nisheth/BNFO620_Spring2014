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

def read(dic,binSize,filename, mapFile,output):
	f=open(filename, 'rU')
	mp=open(mapFile, 'rU')
	o=open(output,'w')
	start=1
	binCounter=1
	header="Tax_id"+"\t"+"Accession"+"\t"+"Seq_Start"+"\t"+"Seq_End"+"\t"+"bin_number"
	print >> o,header
	

	for line in f:
		#print line
		m = re.search('[>]\w+[|](\w+)', line)
		if m:
			print m.group(1)
			myAccession=m.group(1)
		else:
			length=len(line)
			iterate=length/binSize
			leftOver=iterate-int(iterate)
			leftOver=int(leftOver*binSize)
			iterate=int(iterate)
			print leftOver
			print iterate
			print length
			for l in  mp:
				m = re.search('(\w+)\s(\w+)', l)
				#print m.group(1)
				#print m.group(2)
				accession= m.group(1)
				tax=m.group(2)
				if myAccession==accession:
					break
			for i in range (0,iterate):
				end=start+binSize-1
				Dic(dic,tax,myAccession,start,end,binCounter)
				#print dic[tax][myAccession][binCounter]
				start+=binSize
				binCounter+=1

			if leftOver>binSize/2:
				end=end+leftOver
				Dic(dic,tax,myAccession,start,end,binCounter)
				#print dic[tax][myAccession][binCounter]
				binCounter+=1
				
				
			else :
				start=start-binSize
				end =end+leftOver
				binCounter=binCounter-1
				#print tax,myAccession,start,end,binCounter		
				dic[tax][myAccession][binCounter]=str(start)+".."+str(end)
				#print dic[tax][myAccession][binCounter]
			#print dic
			for k in range (1,binCounter):
				sToE=dic[tax][myAccession][k]
				m = re.search('(\w+)\.\.(\w+)', sToE)
				#print m.group(1)
				#print m.group(2)
				start= m.group(1)
				end=m.group(2)

				#print k
				if dic.has_key(tax):
					if dic[tax].has_key(myAccession):
						if dic[tax][myAccession].has_key(k):
							myStr=str(tax)+"\t"+str(myAccession)+"\t"+str(start)+"\t"+str(end)+"\t"+str(k)
							print >> o,myStr



def main():
	if len(sys.argv) < 5:
		print "USAGE: python sys.argv[0] 1- Input fna File 2- bin Size 3- gi maping tax file 4- outputfile \n"
		sys.exit()
	inFna = sys.argv[1]
	binSize =int( sys.argv[2])
	inMap = sys.argv[3]
	output = sys.argv[4]
	dic={}
	
	read(dic,binSize,inFna,inMap,output)

if __name__ == '__main__':
	main()