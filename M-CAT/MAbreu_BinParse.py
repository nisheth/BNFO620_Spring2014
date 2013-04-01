
__author__ = 'Marco Abreu'

import subprocess
import sys
import os
#import argparse

Bin_Size = 100
#GenSource = "/home/bnfo620/M-CAT"
#Source = ""
#Results_to = ''
### program as arguments accepts the directory with flagstat files and a filename to be written to
try:
    if len(sys.argv)<2:
        print "USAGE: python sys.argv[0] input-dir output-dir index \n",
        print "Attempting default value test parameters...."
        #GenSource = 'C:/Users/Owner/PycharmProjects/Homework/mcattest.txt'
        #Dump = 'C:/Users/Owner/PycharmProjects/Homework/dump.txt'
        GenSource = 'C:/Users/bccl_user/Desktop/Bnfo691_602/testgenome.txt'
        Dump = 'C:/Users/bccl_user/Desktop/Bnfo691_602/dump.txt'
        #Results_to = ''
        #GenSource = "/home/bnfo620/M-CAT/All_Bacteria_Drafts+.fna"
        #Dump = "/home/bnfo620/M-CAT/gi_taxid_nucl.dmp"
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
    #print "Sbin",bin_number
    if bin_number >= 1:
        remainder = bin_number-int(bin_number)
        if remainder >= .5:
            bin_number=int(bin_number)+1
        else:
            bin_number=int(bin_number)
        for i in xrange(bin_number):
            bin[str(str(i)+"_bin")]=0
    else:
        bin["0_bin"]=0
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
    toString = ""
    for key in hash.keys():
        for key1 in hash[key].keys():
            for key2 in hash[key][key1].keys():
                toString += str(key1)+"\t"+str(key2)+"\t"+str(key)+"\t"+str(hash[key][key1][key2])+"\n"
    print "Write...",
    outFile.write(toString)
    print "Close", outFile
    outFile.close()
    return "Write Complete"
print "START"

hashX= Genome_Binner(TaxID_to_GI(Dump),GenSource)
outfileprint(hashX)
#print TaxID_gi_bin_hasher(Dump,GenSource)
print "END"

