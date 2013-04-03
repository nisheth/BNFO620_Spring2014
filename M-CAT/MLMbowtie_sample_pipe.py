import subprocess
import sys
import os

def runSystemCMD(cmd):
    print cmd
    subprocess.call([cmd],shell=True)

def isFileThere(file):
    if os.path.isfile(file) :
        print "File exists : " , file
        return True
    else:
        return False


def runBowtiePair(infile1,infile2,index,samfile):
    if not isFileThere(samfile) :
        cmd = "/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -1 " + infile1 + " -2 " + infile2 + " -x " + index + " -S " + samfile
        runSystemCMD(cmd)

def runBowtieSingle(infile1,index,samfile):
    if not isFileThere(samfile) :
        cmd = "/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -U " + infile1 + " -x " + index + " -S " + samfile
        runSystemCMD(cmd)

def convertSamToBam(samfile, bamfile):
    if not isFileThere(bamfile) :
        cmd = "/home/bnfo620/bin/samtools view -bS " + samfile + " > " + bamfile
        runSystemCMD(cmd)
        
def sortBam(bamfile,sorted):
    if not isFileThere(sorted):
        cmd = "/home/bnfo620/bin/samtools sort -no " + bamfile + " " + sorted
        runSystemCMD(cmd)

def generateSamFlagstat(bamfile,flagstatfile):
    if not isFileThere(flagstatfile) :
        cmd = "/home/bnfo620/bin/samtools flagstat " + bamfile + " > " + flagstatfile
        runSystemCMD(cmd)

def main():

    if len(sys.argv) < 6 :
        print "USAGE: python sys.argv[0] infile1 infile2 index project-name outdir\n"
        sys.exit()


    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
    index = sys.argv[3]
    projectname = sys.argv[4]
    outdir = sys.argv[5]

    samfile = outdir +  "/" + projectname + "_bowtie.sam"
    bamfile = outdir +  "/" + projectname + "_bowtie.bam"
    sorted = outdir + "/" + projectname + "_bowtie_sorted"
    resultfile = outdir +  "/" + projectname + "_bowtie_flagstat.txt"

    print samfile
    print bamfile
    print resultfile

    # Running Bowtie ...
    runBowtiePair(infile1,infile2,index,samfile)
    convertSamToBam(samfile,bamfile)
    sortBam(bamfile,sorted)
    #generateSamFlagstat(bamfile,resultfile)

if __name__ == '__main__':
    main()
