from __future__ import division
import re
import os
import sys
import math
import profile
import pickle

def load_Tax_id(filename):
    """
    This module will open the tax_id reference file and create a hash with the gi number as
    the key and the tax_id as the value.
    :param filename: string, filename of the tax_id reference file specified by user
    :return: dict, containing the information for the gi => tax_id values
    """
    taxId = {}                  #create taxId hash
    try:
        f = file(filename)
    except IOError:
        print "The file, %s, does not exist" % filename

    print "creating gi => tax_id hash..."
    for line in f:
        line = line.rstrip()
        gi,tax = line.split()             #get the gi number and tax_id
        taxId[gi]= tax                          #create the hash
    pickle.dump(taxId,open("taxIdHash.p","wb"))
    print "Finished"
    return taxId

def load_sequences(reference,taxIDRef,binSize,output):
    """
    This module will call load_Tax_id to get a hash of the gi => tax_id values, it will then open the
    reference file and parse it, if the current line is a header it will obtain the gi number and tax_id
    and if it is a sequence it will call bin_genome. It will print the results out to a file
    :param reference: string, filename for reference file specified by user
    :param taxIDRef: string, filename for tax_id reference file specified by user
    :param binSize: int, bin size specified by user
    :param output: string, filename for output file
    """

    Bin = 1                             #initialize bin to 1
    previous = None                     #initialize previous to None
    taxID = load_Tax_id(taxIDRef)       #get taxId hash
    tax_id = None                       #initialize tax_id to None
    out = open(output, 'w')             #open the outfile
    header = "TaxID \t\t GI \t\t Start of Seq \t\t End of Seq \t\t Bin"                 #create the header
    print >> out,header                 #print header to outfile

    try:
        f = file(reference)      #cast as a file object if not valid throw exception
    except IOError:
        print "The file, %s, does not exist" % reference     #print error if no file found

    print "Loading sequences and creating bin hash file..."

    count = 0                           #initialize a counter, every 1000 sequences I will print something
    seq = None
    for line in f:                                 #go line by line through the file until the end of the file
        if line == "":
            continue
        if re.match("^>",line):                 #see if it starts with '>' if so store the header
            line = line.rstrip()                #remove whitespace at end of line
            line = line.strip(">")              #remove the > from the header
            line = line.split('|')               #retrieve the gi number

            if seq:
                print len(seq)
                Bin = bin_genome(seq,binSize,Bin,tax_id,giNumber,out)           #get binHash for current sequence
                count += 1

            giNumber = line[1]
            seq = None
            try:
                tax_id = taxID[giNumber]                          #retrieve the tax_id from the taxId hash
            except KeyError:
                if len(line) > 3:
                    tax_id = line[3]
                else:
                    tax_id = line[2]
                    
            if not previous:                                              #if there was no previous seq
                previous = tax_id                                         #set previous to current tax_id
            else:
                if previous != tax_id:                                    #if previous is not equal to the current tax_id
                    Bin = 1                                               #reset bin to equal to 1
                    previous = tax_id                                     #set previous to the current tax_id
        else:
            if seq:
                seq += line.rstrip()
            else:
                seq = line.rstrip()
            #Bin = bin_genome(line.rstrip(),binSize,Bin,tax_id,giNumber,out)           #get binHash for current sequence
            #for each in binHash:                                          #for each in the bin hash
                #start,end = binHash[each].split("...")                    #get the start and end positions
                #string = tax_id+"\t\t"+giNumber+"\t\t"+start+"\t\t"+end+"\t\t"+str(each)                #create a string with the bin information
                #print >> out,string                                       #print string to the out file
            #count += 1
            #tax_id = None
        if count % 1000 == 0:
            print count+1 , "Sequences have been processed..."
    if seq:
        print len(seq)
        Bin = bin_genome(seq,binSize,Bin,tax_id,giNumber,out)           #get binHash for current sequence
    print "Finished!"
    print "Your output was printed to "+output

def bin_genome(sequence,binSize,Bin,tax_id,giNumber,out):
    """
    This method will create a hash that will give the sequence end and start positions for each bin created for a
    specific genome
    :param sequence: string, the current sequence
    :param binSize: int, bin size user specified
    :param Bin:  int, current bin
    :return: a dict containing the bin information and an integer reflecting the new bin number
    """
    binNumber = ""
    startPos = ""
    endPos = ""
    last = ""
    end = None                                                      #initialize end to None
    length = len(sequence)                                          #get the length of the sequence
    newbins = int(math.floor(length / binSize))                   #get the number of bins (only the ones that equal binSize)
    if newbins == 0:                                               #if the length of the sequence is less than binSize newbins will = 0
        newbins = 1                                                #set it to 1 bin
        excess = 0                                                  #set excess to 0
        end = length                                                #set end to the length of the sequence
    else:
        excess = length - (newbins * binSize)                         #get what is leftover and set as ecess
    newbins = Bin + newbins                                           #if bins are continuing from the prev seq then we need to correct for that
    start = 1                                                  #initialize start to 1
    if not end:
        end = binSize                                             #initialize end to binSize if it was net previously set
    previous = ""                                                 #initialzie previous

    for binNumber in range(Bin, newbins):
        binNumber = str(Bin)                                                  #set key to Bin
        startPos = str(start)
        endPos = str(end)                   #create hash for specific key
        Bin += 1                                                    #increase bin by 1
        start += binSize                                            #update start position
        end += binSize                                              #update end position
        if Bin == newbins:                                          #check to see if the last Bin was created if so handle excess  
            if excess < (binSize / 2)and excess > 0:                            #if excess is less than binSize / 2
                endPos = str(excess + int(endPos))                             #add excess and previous end position and make it current end position
            elif excess >= (binSize / 2):                           #if excess is greater than or equal to binSize /2
                last += tax_id+"\t\t"+giNumber+"\t\t"+str(start)+"\t\t"+str(excess-1+start)+"\t\t"+str(int(binNumber) + 1)                                  #make the key previous + 1 (creating another bin)
        string = tax_id+"\t\t"+giNumber+"\t\t"+startPos+"\t\t"+endPos+"\t\t"+binNumber                #create a string with the bin information
        print >> out,string                                       #print string to the out file
        if last != "":
            print >> out,last
    return Bin

def main():
    if len(sys.argv) < 5:
        print "USAGE: python sys.argv[0] 1- reference fasta File 2- tax_id reference File 3- bin size 4- output file \n"
        sys.exit()
    reference = sys.argv[1]
    taxIdRef = sys.argv[2]
    binSize = int(sys.argv[3])
    output = sys.argv[4]

    #reference = "MLMTestRef.fna"
    #taxIdRef = "MLMTestTax.fna"
    #binSize = 5
    #output = "MLMTestOut.txt"

    load_sequences(reference,taxIdRef,binSize,output)

if __name__ == '__main__':
    profile.run("main()","genomebinprofile.tmp")


















