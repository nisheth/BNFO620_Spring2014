#__author__ = 'Marco Abreu'
from __future__ import division
import subprocess
import sys
import os
import re
from MCATpipline import B2_PLAN
#import argparse


Source = '/home/bnfo620/M-CAT/sampledata/simulatddata/'
Source_Index1 = '/home/bnfo620/M-CAT/All_Bacteria_1'
Source_Index2 = '/home/bnfo620/M-CAT/All_Bacteria_2'
Results_to = os.getcwd()+"/"
samtools = '/home/bnfo620/bin/samtools'
Bin_Size = 1000
#GenSource = "/home/bnfo620/M-CAT"
#Source = ""
#Results_to = os.getcwd()
### program as arguments accepts the directory with flagstat files and a filename to be written to
try:
    if len(sys.argv)<2:
        print "USAGE: python sys.argv[0] directory/RefGenome directory/Dump_file \n",
        print "Attempting default value test parameters...."
        #GenSource = 'C:/Users/Owner/PycharmProjects/Homework/mcattest.txt'
        #Dump = 'C:/Users/Owner/PycharmProjects/Homework/dump.txt'
        #GenSource = 'C:/Users/bccl_user/Desktop/Bnfo691_602/testgenome.txt'
        #Dump = 'C:/Users/bccl_user/Desktop/Bnfo691_602/dump.txt'
        #Results_to = ''
        GenSource = "/home/bnfo620/M-CAT/All_Bacteria_Drafts+.fna"
        Dump = "/home/bnfo620/M-CAT/gi_taxid_nucl.dmp"
    else:
        GenSource = sys.argv[1]
        Dump = sys.argv[2]
        #Results_to = sys.argv[2]
except IOError:
    print "Error in input"
print "Source: ",GenSource, "\n", Dump

#Takein arguments from commandline, and run script which runs 3 programs

def TaxID_to_GI(Dump):
    print "TaxIN to gi...START",
    f =open(Dump)
    dump_hash = {}
    for line in f:
        gi, tax_id = line.split()
        #print gi,tax_id
        if int(tax_id) not in dump_hash.keys():
            dump_hash[int(tax_id)] = {}
            dump_hash[int(tax_id)][int(gi)]={}
        else:
            dump_hash[int(tax_id)][int(gi)]={}
    print "TaxID_to_GI...END\n"
    return dump_hash

def Genome_Binner(dump_hash,GenSource, Bin_Size = 1000):
    print "Genome_Binner... START",
    f =open(GenSource)
    Gen_Bin_Array = []
    sequence_count = 0
    Genome_name = ""
    for line in f:
        if line[0] == ">":
            #print sequence_count
            if sequence_count != 0:
                bin = Scount_bin(sequence_count,Bin_Size)
                #Gen_Bin_Array.append([Genome_name,sequence_count])
                for key in dump_hash.keys():
                    #print "Key",key,dump_hash[key],":",Genome_name
                    if Genome_name in dump_hash[key]:
                        #print "test:",key, Genome_name,bin
                        dump_hash[key][Genome_name]=bin
                    else:
                        pass
            sequence_count = 0
            temp = line.split("|")
            Genome_name = int(temp[1])
        else:
            Gen_Bin_Array=[] #reset to 0
            sequence_count += len(line)
            #Gen_Bin_Array.append([Genome_name,sequence_count])
        #print Gen_Bin_Array
    print "Genome_Binner...END\n"
    return dump_hash

def Scount_bin(counts, size):
    bin={}
    bin_number = float(float(counts)/float(size))
    bin_flag=0
    #print "Sbin",bin_number
    if bin_number >= 1:
        remainder = bin_number-int(bin_number)
        if remainder >= .5:
            bin_number=int(bin_number)+1
            bin_flag = 1
        else:
            bin_number=int(bin_number)
        for i in xrange(bin_number):
            if i==bin_number-1 and bin_flag == 0:
                bin[i]=[0,str(str(i*size)+"-"+str(((i+1)*size)-1))]
                bin[i]=[0,str(str((i)*size)+"-"+str(((i+1)*size)+int(remainder*size)))]

            elif i==bin_number-1 and bin_flag == 1:
                bin[i]=[0,str(str(i*size)+"-"+str(((i+1)*size)-1))]
                bin[i+1]=[0,str(str((i+1)*size)+"-"+str(((i+1)*size)+int(remainder*size)))]
            elif i == 0:
                bin[i]=[0,str(str(i*size)+"-"+str((size)-1))]
            else:
                bin[i]=[0,str(str(i*size)+"-"+str(((i+1)*size)-1))]
    else:
        bin[0]=[0,str("0-"+str(counts)),counts]
        #print bin
    return bin



def TaxID_gi_bin_hasher(Dump,GenSource, Bin_Size=1000):
    print "TaxID_gi_bin_Hasher... START\n",
    Hash = TaxID_to_GI(Dump) #hash[gi]=tax id
    Array = Genome_Binner(GenSource,Bin_Size) #gi_num, sequence length
    taxID_bins = {}
    for i,index in enumerate(Array):
        if i%Bin_Size == 0:
            #print "Count: ",i
            #print "0",Array[0],"1", Array[1],index
            gi_num = index[0]
            bin_num = int(index[1])/int(Bin_Size)
        if gi_num in Hash.keys():
            tax_num = Hash[gi_num]
            if tax_num not in taxID_bins.keys():
                taxID_bins[tax_num] = {}
            if gi_num not in taxID_bins[tax_num].keys():
                taxID_bins[tax_num][gi_num]={}
                for i in xrange(bin_num):
                    taxID_bins[tax_num][gi_num][i] = 0
        else:
            pass
    print "TAXID gi bin hasher....END\n"
    return taxID_bins

def fileProcess(Source):
    for filename in os.listdir(Source):
        print "filename:", filename

def fileParse(file):
    pass

def outfileprint(hash): #Test by printing created outfile
    #f =open(str(os.getcwd()+"/MarcoAbreuResult.txt"))
    outFile = open('MarcoAbreuResult.txt','w')
    toString = "TaxID\tGiNumber\tBin\tBin Range\tCount\n"
    for key in sorted(hash.keys()):
        for key1 in sorted(hash[key].keys()):
            for key2 in sorted(hash[key][key1].keys()):
                toString += str(key)+"\t"+str(key1)+"\t"+str(key2)+"\t"+str(hash[key][key1][key2][1])+"\t"+str(hash[key][key1][key2][0])+"\n"
    print "Write...",
    outFile.write(toString)
    print "Close", outFile
    outFile.close()
    return "Write Complete"

def SAMREADER(hash,thresh=3):
    for filename in os.listdir(Results_to):
        name_end = filename[len(filename)-8:]
        list = []
        if name_end == 'CSAM.sam':
            f = open(os.getcwd()+"\\"+filename)
            i = 0
            cline = ""
            for line in f:
                if line[:2] == 'gi':
                    cline=line+cline
                    if len(cline) > 250:
                        ginum,taxnum,score,start_pos = giRead(cline)
                        for key in hash.keys():
                            if ginum in hash[key].keys():
                                bins=int(start_pos/Bin_Size)
                                hash[key][ginum][bins].append([score,taxnum])





                    cline = ""
                else:
                    cline+=line
                i+=1

def giRead(line):
    raw = line.split(" ")
    #print "X",line
    info = []
    for part in raw:
        lok = part.strip('\n')
        if len(lok)>1:
            #print len(lok),lok
            info.append(lok)
    #print "info",info[0],info[1],info[2],info[3],info[4],info[len(info)-2] #,info
    raw_mdz = str(info[len(info)-2]).split(':')
    mdz = raw_mdz[2]
    gi = str(info[0]).split("|")
    ginum = gi[1]
    if len(info[1])>5:
        cigar = info[3]
        tax = str(info[1]).split("|")
        taxnum = tax[1]
        start_pos = info[2]
    else:
        start_pos = info[3]
        cigar = info[4]
        tax = str(info[2]).split("|")
        taxnum = tax[1]
    #print "raw",ginum,taxnum,cigar,mdz,start_pos
    mz = int(mdz_score(mdz))
    cig = int(cigar_score(cigar))
    score = float(mz/float(cig))*100
    return ginum,taxnum,score,start_pos

def mdz_score(score):
    code = re.findall(r'(\D+|\d+)',score)
    score = 0
    #print code
    for i in xrange(len(code)-1):
        try:
            score += int(code[i])
        except ValueError:
            score+=len(str(code[i]))
    return int(score)

def cigar_score(score):
    code = re.findall(r'(\D+|\d+)',score)
    score = 0
    #print code
    for i in xrange(len(code)-1):
        if i < len(code)-1:
            if code[i+1]=='M':
                #print i,code[i]
                score+=int(code[i])
    #print "Score",score
    return int(score)




print "START"
hashX= Genome_Binner(TaxID_to_GI(Dump),GenSource)


Genetics = B2_PLAN(Source,Results_to,Source_Index1,Source_Index2)
Genetics.bowtie_OPS(Source_Index1)
Genetics.SAM_OPS()
Genetics.BAMMERGE_OPS()
Genetics.B2S_OPS()

#outfileprint(hashX)

SAMREADER(hashX)
#print TaxID_gi_bin_hasher(Dump,GenSource)
print "END"

