from __future__ import division
import re
import os
import sys
import math
import profile
import pickle
import numpy as np

def read_Bin(filename):
    """
    This module will open the tax_id reference file and create a hash with the gi number as
    the key and the tax_id as the value.
    :param filename: string, filename of the tax_id reference file specified by user
    :return: dict, containing the information for the gi => tax_id values
    """
    bins = {}                  #create taxId hash
    taxid = {}
    try:
        f = file(filename)
    except IOError:
        print "The file, %s, does not exist" % filename

    print "creating gi => tax_id hash..."

    last = None
    for line in f:
        line = line.rstrip()
        if line.startswith("TaxID"):
            continue
        #tax,gi,start,end,bin = line.split()             #get the gi number and tax_id
        try:
            tax,gi,start,end,bin = line.split()
        except ValueError:
            continue
        bins[tax+"_"+bin]= [tax,int(start),int(end),bin]  #create the hash
        last = tax+"_"+bin
        if gi not in taxid:
            taxid[gi] = tax
            #print gi, tax
    #print "Finished"
    f.close()
    print bins[last]
    #pickle.dump(bins,open("tmpBins.p","wb"))
    #pickle.dump(taxid,open("tmpTax.p","wb"))
    print "Finished"
        
    return bins,taxid

def parseCigar(cigar):
    cigarParsed = []
    part = ""
    for position, chr in enumerate(cigar):
        if chr == "*":
            cigarParsed.append(chr)
            break
        if chr == "M" or chr == "I" or chr == "D":
            if part != "":
                cigarParsed.append(int(part))
                part = ""
            cigarParsed.append(chr)
        else:
            part += chr

    if part != "":
        cigarParsed.append(int(part))
    #print cigarParsed, "cigar"
    return cigarParsed

def parseMD(md):
    mdParsed = []
    part = ""
    for position, chr in enumerate(md):
        if chr == "A" or chr == "C" or chr == "T" or chr == "G" or chr == "^":
            if part != "":
                mdParsed.append(int(part))
                part = ""
            mdParsed.append(chr)
        else:
            part += chr
    if part != "":
        mdParsed.append(int(part))
    #print mdParsed, "MD"
    return mdParsed

def getReadInfo(tax,record,readInfo):
    info = []
    read = record[0]
    cigar = record[5]
    md = None
    #print cigar, "cigar"
    begin = int(record[3])
    length = len(record)-1
    for each in record:
        #print each
        if each.startswith("MD"):
            md = each.strip("MD:Z:")
            break
    #if record[length].startswith("MD"):
        #md = record[length].strip("MD:Z:")
    #else:
        #length = len(record) -2
        #if record[length].startswith("MD"):
            #md = record[length].strip("MD:Z:")


    cigar = parseCigar(cigar)
    if md:
        md = parseMD(md)
    else:
        md = '*'
    info.append(tax)
    info .append(begin)
    info.append(cigar)
    info.append(md)
    info.append(read)
    readInfo.append(info)

    return readInfo

def score(cigar,md):
    if cigar[0] != '*':
        den = 0
        lenC = len(cigar)
        count = 0

        while count < lenC:
            if cigar[count] == 'D':
                den = den -cigar[count]
            else:
                den = den + cigar[count]
            count += 2

        misAndGap = 0
        match = 0

        for position,value in enumerate(md):
            if isinstance(value,int):
                match += value
                continue
            elif value == '^':
                continue
            else:
                misAndGap += 1

        num = match - misAndGap
        score = (num / den) * 100
    else:
        score =0
    return score

def processReads(readInfo,mout,binHash,binCount):
    scores = []
    max = 0
    readScore = []
    for each in readInfo:
        print each
        readScore = [each[0],each[1],score(each[2],each[3]),each[4]]
        scores.append(readScore)
        if readScore[2] > max:
            max = readScore[2]

    max -= 5

    for each in scores:
        print each, "each"
        if each[2] >= max:
            mapped = each[3] + "\t" + each[0]
            print each[3],"3"
            print >> mout,mapped
            for every in binHash:
                #print every,"every"
                if each[0] in binHash[every][0]:
                    #print "every[0]", binHash[every][0]
                    if each[1] >= binHash[every][1] or each[1] <= binHash[every][2]:
                        if each[0] in binCount:
                            #print each[3],"each 3"
                            binCount[each[3]] += 1
                        else:
                            binCount[each[3]] = 1
                            #print each[3],"each 3"

    return binCount


def read_sam(sam,bins,taxid):
    try:
        f = file(sam)      #cast as a file object if not valid throw exception
    except IOError:
        print "The file, %s, does not exist" % sam     #print error if no file found

    printout = open("mappedReads.txt",'w')
    printout1 = open("binCount.txt",'w')

    currTax = None
    readInfo = []
    binCount= {}
    for line in f:                                 #go line by line through the file until the end of the file
        if line == "":                              #if there is a space between sequences this will catch it and continue the loop
            continue

        record = line.split()
        if int(record[1]) == 4:
            continue
        else:
            read = record[2]
            read = read.split('|')
            if read[0] == '*':
                continue
            tax = taxid[read[1]]
            if not currTax:
                currTax = tax
            if tax != currTax:
                processReads(readInfo,printout,bins,binCount)
                readInfo = []
                readInfo = getReadInfo(tax,record,readInfo)
            else:
                readInfo = getReadInfo(tax,record,readInfo)

    for each in binCount:
        binInfo = each[0] + "\t" + each[1]
        print >> printout1,binInfo

    '''
    finalHash = {}
    K = 0
    N = 0
    for each in binCount:
        if each[1] != 0:
            K += 1
        N += 1


    #log in numpy is ln()
    Sw = 0
    prev = None
    for each in binCount:
        if not prev:
            prev = each[0]
            continue
        if gene[0] = prev:
           finalHash[each[0]] = (-W*np.log(W)+W*sum) / np.log(K)

    '''

    printout.close()
    printout1.close()


def main():
    #the following will be changed, I realized i could just write a command that will find all the sam files. For now it does the analysis on one sam file
    if len(sys.argv) < 3:
        print "USAGE: python sys.argv[0] 1- Bin File 2- SamMergedFile1 \n"
        sys.exit()
    binFile = sys.argv[1]
    samFile = sys.argv[2]
    binHash,taxHash = read_Bin(binFile)
    #binHash = pickle.load(open("tmpBins.p","rb"))
    #taxHash = pickle.load(open("tmpTax.p","rb"))
    read_sam(samFile,binHash,taxHash)

if __name__ == '__main__':
    profile.run("main()","filterSam.tmp")
