from __future__ import division
import re
import os
import sys
import math
import profile

def readBins(binFile):
    ### reads in bin file and stores it to be used

    ### variables
    bins ={}
    tax = {}

    ### nwo read in the files
    try:
        f = file(binFile)
    except IOError:
        print "The file, %s, does not exist" % binFile

     ### status ipdate
    print "loading bin file"

    previousKey = None
    for line in f:
        line = line.rstrip()
        if line.startswith("TaxID"):
            continue
        info = line.split()
        taxID = info[0]
        giID = info[1]
        start = info[2]
        end = info[3]
        binNum = info[4]

        ### now use that line info in dict as an array
        ### have key of the taxID and binNum
        ### have to do int() as otherwise start and end are treated as str
        key = taxID+"_"+binNum
        bins[key]= [taxID,int(start),int(end),binNum]

        previousKey = key
        ### if the giID to taxID does not exist, store it
        if giID not in tax:
            tax[giID] = taxID

        f.close()

        ### return the data
        return bins,tax


def readSam(sam,bins,taxa):
    ### open sam file
    try:
        f = file(sam)
    except IOError:
        print "The file, %s, does not exist" % sam

    current = None
    readInfo = []
    binCount= {}

    ### go through line by line (each line is a sam record)
    for line in f:
        ### skip empty lines
        if line == "":
            continue

        ### store each line info in a list
        samRecord = line.split()

        ### ignore the reads that do not map back
        if int(samRecord[1]) == 4:
            continue
        else:
            ### get the taxID from the list
            read = samRecord[2]
            read = read.split('|')
            taxID = taxa[read[1]]
            ### make a current for the first record
            if not current:
                current = taxID

            ### for the next records, run the functions
            if taxID != current:
                filterReads(readInfo,bins,binCount)
                readInfo = []
                readInfo = readInformation(taxID,samRecord,readInfo)
            else:
                readInfo = readInformation(taxID,samRecord,readInfo)


def readInformation(taxID,samRecord,readInfo):
    ### takes the
    info = []
    readID = samRecord[0]
    cigarString = samRecord[5]
    start = int(samRecord[3])

    ### since mdz can be at different locations in the sam record, it must be checked to see if it is there.
    ### the length is the adjusted to index positions
    samLength = len(samRecord)-1
    ### if it is at the last position
    if samRecord[samLength].startswith("MD"):
        mdString = samRecord[samLength].strip("MD:Z:")
    ### check to see if it is at the second to last
    else:
        samLength = len(samRecord) -2
        if samRecord[samLength].startswith("MD"):
            mdString = samRecord[samLength].strip("MD:Z:")


    cigarString = cigarParser(cigarString)
    mdString = mdParser(mdString)

    ### now take this information and append it to a list. readInfo ends up being a list of a list
    info.append(taxID)
    info.append(start)
    info.append(cigarString)
    info.append(mdString)
    info.append(readID)

    ### now append list to another list
    readInfo.append(info)

    return readInfo

def score(cigar, mdz):
    ### this generates a score using the cigar and mdz lists
    cigarNum = 0
    cigarLength = len(cigar)
    count = 0

    ### walk through cigar list and generate number if chars
    while count < cigarLength:
        if cigar[count] == 'D':
            ### removes the number of deletions
            cigarNum = cigarNum - cigar[count]
        else:
            cigarNum = cigarNum + cigar[count]
        count += 2

    misNum = 0
    matchNum = 0

    for i,value in enumerate(mdz):
        ### if it is a number, add it to the match number
        if isinstance(value,int):
            matchNum += value
            continue
        ### if insert, skip
        elif value == '^':
            continue
        ### if mismatch, add to mismatch number
        else:
            misNum += 1

    ### take the number of matches without the mismatches and divide by the cigar matches.
    ### to get the percentage, multiple by 100
    numerator = matchNum - misNum
    score = (numerator / cigarNum) * 100

    return score
def cigarParser(cigarString):
    ### this takes a cigar string and adds each piece to an array
    cigarParsed = []
    piece = ""
    for position, character in enumerate(cigarString):
        if character == "M" or character == "I" or character == "D":
            if piece != "":
                cigarParsed.append(int(piece))
                piece = ""
            cigarParsed.append(character)
        else:
            piece += character

    if piece != "":
        cigarParsed.append(int(piece))

    return cigarParsed

def mdParser(mdString):
    ### does the same thing as the cigarParser
    mdParsed = []
    piece = ""
    for position, character in enumerate(mdString):
        if character == "A" or character == "C" or character == "T" or character == "G" or character == "^":
            if piece != "":
                mdParsed.append(int(piece))
                piece = ""
            mdParsed.append(character)
        else:
            piece += character
    if piece != "":
        mdParsed.append(int(piece))

    return mdParsed

def filterReads(readInfo,bins ,binCounts):
    scores = []
    max = 0
    outFile = "filtered.sam"
    binOut = "binCounts.txt"

    ### go through all the reads
    for each in readInfo:
        tmp =score(each[2], each[3])
        ### store read information and scores as a list
        score = [each[0], each[1], tmp ,each[4]]
        ### have list of list of all scores
        scores.append(score)
        if score[2] > max:
            max = score[2]

    cutOff = max - 5

    ### open file to write out to
    out = open(outFile, 'w')
    ot =  open(binOut, 'w')

    ### walk though all the scores and check to see if above cut off
    for each in scores:
        if each[2] >= cutOff:

            mapped = each[4] + "\t" + each[0]
            out.write(mapped)

            for every in bins:
                if each[0] in bins[every][0]:
                    if each[1] >= bins[every][1] or each[1] <= bins[every][2]:
                        if each[0] in binCounts:
                            binCounts[each[3]] += 1
                        else:
                            binCounts[each[3]] = 1

    for each in binCounts:
        ot.write(each)

    return binCounts





def main():
    ###main function that runs everything
    if len(sys.argv) < 3:
        print "USAGE: python sys.argv[0] 1- Bin File 2- SamMergedFile1 \n"
        sys.exit()
    ### grab what we need
    binFile = sys.argv[1]
    samFile = sys.argv[2]
    ### send binFile to read bins to generate data structures we need
    bins,taxHash = readBins(binFile)
    ### send thos structures to readSame which filters by score
    readSam(samFile,bins,taxHash)

if __name__ == '__main__':
    profile.run("main()","filterSam.tmp")

