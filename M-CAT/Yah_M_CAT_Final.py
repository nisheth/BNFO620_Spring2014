from __future__ import division
import sys
import os
import re
from string import *
import math
from math import e
########################################################
#This method read the bin file created and store it hash
#bin file look like:
#Tax_id Accession   Seq_Start   Seq_End bin_number
#240016 164421336   1   1000    1
#240016 164421336   1001    2000    2
#240016 164421336   2001    3000    3
#240016 164421336   3001    4000    4
#240016 164421336   4001    5000    5
#240016 164421336   5001    6000    6
########################################################
def storeThebin(bin,binDic,taxAcc,binHit):
    f=open(bin, 'rU')
    for line in f:
        #print line
        m = re.search ('(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
        if m:
            m1=m.group(1)
            if m1 in binHit:  #to count how many bin each readID has
                binHit[m1]+=1
            else:
                binHit[m1]=1
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

            #print binHit

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
#substract 5% from it and then dicard any score below that that percent.
#After that it outputs accession number tax_id and start 
#Ex: 
##########################################################################
def percentRule(hitsPerRead,taxAcc,p):
    #o=open(percent_output, "w")
    highist=0
    #for key, value in sorted (hitsPerRead.iteritems(), key=lambda (k,v): (v,k)):
        #print "%s: %s" % (key, value)
    #print hitsPerRead

    for key, value in hitsPerRead.items(): # returns the dictionary as a list of value pairs -- a tuple.
        if value>highist:
            highist=value
        highist=highist-.05
    for key, value in hitsPerRead.items(): # returns the dictionary as a list of value pairs -- a tuple
        if highist>value:
            del hitsPerRead[key]
    for key, value in hitsPerRead.items(): 
        m = re.search('(.+)\*(\d+)\*(\d+)', key)
        readID=m.group(1)
        accessionNo=m.group(2)
        hitStart=m.group(3)
        #print accessionNo," ",hitStart
        taxInBin=taxAcc[accessionNo]
        print >>p, readID+"\t"+taxInBin+"\t"+hitStart
    #print "Tax=",taxInBin," AccessionNo=",accessionNo," hitStart=",hitStart
    
    #print "hitsPerRead",hitsPerRead
    return hitsPerRead
##########################################################################
#This is just an output method
#Ex:     Tax       Bin   count
#       57650036    6492    1
##########################################################################
def binHitCounter(taxAcc,binDic,hitsPerRead,binPerTax,tax_Bin_count):
    #print binDic
    #count=0
    
    taxInBin=0 
    accessionNo=None
    #print hitsPerRead
    for key, value in hitsPerRead.items(): 
        m = re.search('\*(\d+)\*(\d+)', key)
        accessionNo=m.group(1)
        hitStart=m.group(2)
        taxInBin=taxAcc[accessionNo]
        #print taxInBin, "=taxInBin"
        #print "hitStart=", hitStart
        #for key1, value1 in binDic.items(): 
        #for key2 in value1.iterkeys():
        #for value1 in binDic.iterkeys():
        #for value1 in binDic.itervalues():
        for key1, value1 in binDic.items():
            if (accessionNo==key1):
                for key2, value2 in value1.items(): 
                    #print "key1=",key1," value1=",value1," key2=",key2," value2=",value2
                    m2= re.search('(\d+)_(\d+)', key2)
                    s=m2.group(1)  #start
                    e=m2.group(2)  #end
                    #print "start= ",s,"end= ",e
                    #print "hitStart=", hitStart
                    if int(hitStart)>= int(s) and int(hitStart)<int(e):
                        tax_bin_key=str(taxInBin)+"_"+str(value2)
                        if tax_bin_key in tax_Bin_count:
                            tax_Bin_count[tax_bin_key]+=1
                            # count how many time the tax hit at least once
                            binPerTax[taxInBin]+=1  
                        else:
                            tax_Bin_count[tax_bin_key]=1   
                            binPerTax[taxInBin]=1
                        #print "start= ",s,"end= ",e
                        #print "hitStart=", hitStart
                        #print count,"hit"
def taxScore(taxAcc,binHit,tax_Bin_count,binPerTax):
    taxW={}
    Sw={}
    for key, value in binHit.items():
        #taxW[key]=binPerTax[key]/value
        if key in binPerTax.iterkeys():
            taxW[key]=binPerTax[key]/value

    for  key, value in tax_Bin_count.items():
        m= re.search('(\d+)_(\d+)', key)
        tax=m.group(1)  #start
        binNumber=m.group(2)  #end
        if tax in Sw:
            Sw[tax]+=taxW[tax]*value*logN(taxW[tax]*value)
        else:
            Sw[tax]=taxW[tax]*value*logN(taxW[tax]*value)
    return Sw

def logN(X, base=math.e, epsilon=1e-12):
  # logN is logarithm function with the default base of e
  integer = 0
  if X < 1 and base < 1:
    raise ValueError, "logarithm cannot compute"
  while X < 1:
    integer -= 1
    X *= base
  while X >= base:
    integer += 1
    X /= base
  partial = 0.5               # partial = 1/2 
  # list = []                   # Prepare an empty list, it seems useless
  X *= X                      # We perform a squaring
  decimal = 0.0
  while partial > epsilon:
    if X >= base:             # If X >= base then a_k is 1 
      decimal += partial      # Insert partial to the front of the list
      X = X / base            # Since a_k is 1, we divide the number by the base
    partial *= 0.5            # partial = partial / 2
    X *= X                    # We perform the squaring again
  return (integer + decimal)



def taxBinCountOutput(tax_Bin_count,output):
    o=open(output,'w')
    print >> o, "Tax"+"\t"+"Bin"+"\t"+"count"
    for key, value1 in tax_Bin_count.items():
        m2= re.search('(\d+)_(\d+)', key)
        readID=m2.group(1)
        bin=m2.group(2)
        print >>o,  str(readID)+"\t"+str(bin)+"\t"+str(value1)
#def deleteExtraTax():


def updateReadIdTaxStart(percent_output,Sw,finalOutput):
    f=open(percent_output, 'rU')
    outputHash={}
    b=0
    for line in f:
        #print line
        m= re.search('(.+)\s+(\d+)\s+(\d+)', line)
        readID=m.group(1)
        tax=m.group(2)
        start=m.group(3)

        if readID in outputHash:
            for key1 in outputHash.iterkeys():
                for key2 in key1.iterkeys():
                    if Sw(tax)>Sw(key2):
                        outputHash[key1][tax]=start

        else:
            outputHash[readID]={}
            outputHash[readID][tax]=start
            #print outputHash
     
    return outputHash

def finalOutputReadIdTaxStart(outputHash,finalOutput):
    #print outputHash
    out=open(finalOutput, "w")
    for key1 ,value1 in outputHash.iteritems():
        for key2 , value2 in value1.iteritems():
            print >> out,  str(key1)+"\t"+str(key2)+"\t"+str(value2)

############################################################################################################################################
#This method  Read  the sam file and call the other methods to anlyze it
#Ex: gi|57650036|ref|NC_002951.2|_571308_571841_2:0:0_2:0:0_2bb6/2  16  gi|297207379|ref|NZ_ADVP01000001.1| 1915    1   100M    *   
#0  0   TAAAAATCTACACCAGTAGCTTCTTTTACAGTATCAACAATATACAAACGAGTCCAAGCAGATTCTAAATCAATCGTTTCCCCATTGTATTGTACTTTTG    
#2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222   AS:i:190    
#XS:i:190   XN:i:0  XM:i:2  XO:i:0  XG:i:0  NM:i:2  MD:Z:31C11G56   YT:Z:UU
############################################################################################################################################
def read(taxAcc,binDic,inSAM,tax_Bin_count,binPerTax,percent_output):
    f=open(inSAM, 'rU')
    p=open(percent_output, "w")
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
        #gi|164421336|ref|NC_002951.2|_570583_571003_2:0:0_1:0:0_c66/2  16  gi|297207379|ref|NZ_ADVP01000001.1| 2640
        #gi|57650036|ref|NC_002951.2|_567950_568502_2:0:0_4:0:0_b10/2   0   gi|258453812|
        m = re.search('(gi\S\d+.+)\s\d+\s+gi\S(\d+).+\s+(\d+)\s+\d+\s+(\w+)\s+[*].+MD:Z:([0-9]+(([A-Z]|\^[A-Z]+)[0-9]+)*)', line)
        readID=m.group(1) 
        gi= (m.group(2)) 
        start = (m.group(3)) 
        cigar= (m.group(4))  
        MD= m.group(5)  
        #print readID,gi,start,cigar,MD
        cigarCount=countCigar(cigar)
        #print cigarCount
        MDcount=countMD(MD)
        #print MDcount
        score=(cigarCount-MDcount)/cigarCount
        #print score

        #if not tempTax:
            #tempTax = gi
        #print tempTax, readID, b
        if readID != tempTax and b==1:
            hitsPerRead=percentRule(hitsPerRead,taxAcc,p) #Appling 5% rule
            #print hitsPerRead
            binHitCounter(taxAcc,binDic,hitsPerRead,binPerTax,tax_Bin_count)
            hitsPerRead={}
            hashCount=1
            tempTax = readID
            hitsPerRead[readID+"*"+gi+"*"+start]=score
            #print readID+"-"+gi+"-"+start
            hashCount+=1
            b=0
            
#keep reading the sam file untill new new accessionz
        else:
            tempTax = readID
            hitsPerRead[readID+"*"+gi+"*"+start]=score
            #print readID+"-"+gi+"-"+start
            hashCount+=1
            b=1
            #percentRule(hitsPerRead) 
    binHitCounter(taxAcc,binDic,hitsPerRead,binPerTax,tax_Bin_count)

def main():
    if len(sys.argv) < 4 :
        print "USAGE: python sys.argv[0] 1-Input_SAM_File 2-bin_file  4- 5%_output 5-finalOutput"
        sys.exit()
    inSAM = sys.argv[1]
    bin = sys.argv[2]
    finalOutput=sys.argv[3]
    output = "Bin_Output"
    percent_output= "fivePercentRuleTable"
    binHit={}
    binDic={}
    taxAcc={}
    tax_Bin_count={}
    binPerTax={}
    Sw={}
    outputHash={}

    taxScore(taxAcc,binHit,tax_Bin_count,binPerTax)
    storeThebin(bin,binDic,taxAcc,binHit)
    read(taxAcc,binDic,inSAM,tax_Bin_count,binPerTax,percent_output)
    taxBinCountOutput(tax_Bin_count,output)
    Sw=taxScore(taxAcc,binHit,tax_Bin_count,binPerTax)
    outputHash=updateReadIdTaxStart(percent_output,Sw,finalOutput)
    finalOutputReadIdTaxStart(outputHash,finalOutput)

if __name__ == '__main__':
    main()