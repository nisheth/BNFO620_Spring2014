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
        cmd = "/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 2 -1 " + infile1 + " -2 " + infile2 + " -x " + index + " -S " + samfile
        runSystemCMD(cmd)
    
def runBowtieSingle(infile1,index,samfile):
    if not isFileThere(samfile) :
        cmd = "/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 2 -U " + infile1 + " -x " + index + " -S " + samfile
        runSystemCMD(cmd)

def convertSamToBam(samfile, bamfile):
    if not isFileThere(bamfile) :
        cmd = "/home/bnfo620/bin/samtools view -bS " + samfile + " > " + bamfile
        runSystemCMD(cmd)

def generateSamFlagstat(bamfile,flagstatfile):
    if not isFileThere(flagstatfile) :
        cmd = "/home/bnfo620/bin/samtools flagstat " + bamfile + " > " + flagstatfile
        runSystemCMD(cmd)
def mergeBams(file1, file2, mergefile):
    if not isFileThere(mergefile):
        cmd = "/home/bnfo620/bin/samtools cat -o " + mergefile + " " + file1 + " " + file2
        runSystemCMD(cmd)
def sortBams(bamFile, sortedFile):
    if not isFileThere(sortedFile):
        cmd = "/home/bnfo620/bin/samtools sort " + bamFile + " " + sortedFile
        runSystemCMD(cmd)

def main(): 

    if len(sys.argv) < 6 :
        print "USAGE: python sys.argv[0] infile1 infile2 index project-name outdir\n"
        sys.exit()

        
    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
    index = sys.argv[3]
    index2 = sys.argv[4]
    projectname = sys.argv[5]
    outdir = sys.argv[6]
        
#    samfile = outdir +  "/" + projectname + "_bowtie.sam"
#    bamfile = outdir +  "/" + projectname + "_bowtie.bam"
#    resultfile = outdir +  "/" + projectname + "_bowtie_flagstat.txt"

    # Running Bowtie ...
    i = 0
    while i <= 1:
        if i == 0:
            samfile = "sample_1.sam"
            bamfile = "sample_1.bam"
            resultfile = "sample_1_results_flagstat.txt"
            sortedfile1 = "sample_1_sorted.bam"

            runBowtiePair(infile1,infile2,index,samfile)
            convertSamToBam(samfile,bamfile)
            generateSamFlagstat(bamfile,resultfile)
            sortBams(bamfile, sortedfile1)
        if i == 1:

            samfile = "sample_2.sam"
            bamfile = "sample_2.bam"
            resultfile = "sample_2_results_flagstat.txt"
            sortedfile2 = "sample_2_sorted.bam"

            runBowtiePair(infile1,infile2,index2,samfile)
            convertSamToBam(samfile,bamfile)
            generateSamFlagstat(bamfile,resultfile)
            sortBams(bamfile, sortedfile2)

        ### now merge the two files
        mergefile = "merged.bam"
        mergeBams(sortedfile1, sortedfile2, mergefile)

        
if __name__ == '__main__':
    main()





