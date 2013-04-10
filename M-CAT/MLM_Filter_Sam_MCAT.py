from __future__ import division
import re
import os
import sys
import math
import profile

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
        tax,gi,start,end,bin = line.split()             #get the gi number and tax_id
        bins[tax+"_"+bin]= [tax,int(start),int(end),bin]  #create the hash
        last = tax+"_"+bin
        if gi not in taxid:
            taxid[gi] = tax
            print gi, tax
    print "Finished"
    f.close()
    print bins[last]
    return bins,taxid

def parseCigar(cigar):
    cigarParsed = []
    part = ""
    for position, chr in enumerate(cigar):
        if chr == "M" or chr == "I" or chr == "D":
            if part != "":
                cigarParsed.append(int(part))
                part = ""
            cigarParsed.append(chr)
        else:
            part += chr

    if part != "":
        cigarParsed.append(int(part))
    print cigarParsed, "cigar"

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
    print mdParsed, "MD"

def getReadInfo(tax,record,readInfo):
    info = []
    read = record[0]
    cigar = record[5]
    begin = int(record[3])
    length = len(record)-1
    if record[length].startswith("MD"):
        md = record[length].strip("MD:Z:")
    else:
        length = len(record) -2
        if record[length].startswith("MD"):
            md = record[length].strip("MD:Z:")


    cigar = parseCigar(cigar)
    md = parseMD(md)
    info.append(tax)
    info .append(begin)
    info.append(cigar)
    info.append(md)
    info.append(read)
    readInfo.append(info)

    return readInfo

def score(cigar,md):
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
    return score

def processReads(readInfo,mout,binHash,binCount):
    scores = []
    max = 0
    for each in readInfo:
        score = [each[0],each[1],score(each[2],each[3]),each[4]]
        scores.append(score)
        if score[2] > max:
            max = score[2]

    max -= 5

    for each in scores:
        if each[2] >= max:
            mapped = each[4] + "\t" + each[0]
            print >> mout,mapped
            for every in binHash:
                if each[0] in binHash[every][0]:
                    if each[1] >= binHash[every][1] or each[1] <= binHash[every][2]:
                        if each[0] in binCount:
                            binCount[each[3]] += 1
                        else:
                            binCount[each[3]] = 1

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
    read_sam(samFile,binHash,taxHash)

if __name__ == '__main__':
    profile.run("main()","filterSam.tmp")
