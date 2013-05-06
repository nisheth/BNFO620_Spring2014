from __future__ import division
import re
import os
import sys
import math
import profile

def swScore(samFile):
    ### samfile contains filtered reads
    ### we will score these based on sw formula and write out again
    ### read in binCount file
    ### calculate sw by looping through the binCOunts of all the bins in a taxID and store  as a dictionary
    ### with key of taxID and value of sw score
    
    ### next loop through reads in filtered sam file
    ### those with one taxID write out to assigned file
    ### those with more, compared SW scores of the taxIDs
    ### assign read to highest sw score and write out
    pass


def main():
    ###main function that runs everything
    if len(sys.argv) < 3:
        print "USAGE: python sys.argv[0] 1- Bin File 2- SamMergedFile1 \n"
        sys.exit()
        ### grab what we need
    binFile = sys.argv[1]

if __name__ == '__main__':
    profile.run("main()","filterSam.tmp")
