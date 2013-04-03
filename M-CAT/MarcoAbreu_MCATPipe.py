#Marco Abreu
from __future__ import division
import subprocess
import sys
import os
import re
import subprocess as sp
Test = True
Source = '/test/bnfo/bnfo620/M-CAT/sampledata'
Source_Index1 = '/home/bnfo620/M-CAT/All_Bacteria_1'
Source_Index2 = '/home/bnfo620/M-CAT/All_Bacteria_2'
Results_to = os.getcwd()

try:
    if len(sys.argv)<2:
        print "USAGE: python sys.argv[0] Source_directory directory/index1 directory/index2 \n"
        print "index2 optional"
        print "Attempting default value test parameters...."

    else:
        Source = sys.argv[1]
        Source_Index1 = sys.argv[2]
        if len(sys.argv)>2:
            Source_Index2 = sys.argv[3]
        else:
            Source_Index2 = "unused"
except IOError:
    print "Error in input"
print "Source: ",Source, "\t", Source_Index1, "\t", Source_Index2, "\n"
print "Results_to: ", Results_to



class B2_PLAN(object):
    def __init__(self,source,results,index1,index2=""):
        self.source = source
        self.results = results
        self.index1 = index1
        self.index2 = index2
        self.BAMFILE = ""
        self.SAMFILE = ""
        self.BAM_FLAG = self.bam_filecheck()
        self.SAM_FLAG = self.sam_filecheck()

    def sam_filecheck(self):
        for sams in os.listdir(self.results):
            sam_len = (len(sams))
            sam_flag = sams[sam_len-3:]
            if sam_flag == "sam":
                return 1
            else:
                pass
        return 0
    def bam_filecheck(self):
        for bams in os.listdir(self.results):
            bam_len = (len(bams))
            bam_flag = bams[bam_len-3:]
            if bam_flag == "bam":
                return 1
            else:
                pass
        return 0

    def RunCMD(self,cmd):
        print cmd
        subprocess.call([cmd],shell = True)

    #Takein arguments from commandline, and run script which runs 3 programs
    def bowtie_OPS(self, index=""):
        FILE_EXT = "fna"
        if len(index) < 1:
            index = self.index1
        for filename in os.listdir(self.source):
            L = (len(filename))
            fq_flag = filename[L-len(FILE_EXT):]
            if fq_flag == FILE_EXT:
                self.SAMFILE = filename[:L-6]+'_bt_result.sam'
                #print "NAME",filename, filename[:L-6]
                cmd = "/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -x " + index + " -U "+ self.source+filename," -S " + self.results+self.SAMFILE
                self.RunCMD(cmd)

    def SAM_OPS(self):
        #print "SAM to BAM"
        bamrunlist = []
        for sams in os.listdir(self.results):
        #/home/bnfo620/bin/samtools view -bS $SAMFILE > $BAMFILE
            sam_len = (len(sams))
            sam_flag = sams[sam_len-3:]
            #print sam_flag
            if sam_flag == 'sam':
                self.BAMFILE = sams[:sam_len-4]+'.bam'
                bamrunlist.append(self.BAMFILE)
                #print "/home/bnfo620/bin/samtools view -bS",Results_to+SAMFILE, ">",Results_to+BAMFILE
                cmd = "/home/bnfo620/bin/samtools view -bS " + self.results + self.SAMFILE + " > " + self.Results + self.BAMFILE
                self.RunCMD(cmd)
        return bamrunlist

    def BAM_OPS(self):
        #print "BAM to flag"
        for bams in os.listdir(self.results):
        #/home/bnfo620/bin/samtools flagstat $BAMFILE > $FLAGSTATFILE
            #print bams
            bam_len = (len(bams))
            bam_flag = bams[bam_len-3:]
            #print bam_flag
            if bam_flag == 'bam':
                FLAGSTATFILE = bams[:bam_len-4]+'.txt'
                #print FLAGSTATFILE
                #print "/home/bnfo620/bin/samtools flagstat",Results_to+BAMFILE, ">",Results_to+FLAGSTATFILE
                cmd = "/home/bnfo620/bin/samtools flagstat "+ self.results + self.BAMFILE + " > " + self.results + FLAGSTATFILE
                self.RunCMD(cmd)

    def BAMMERGE_OPS(self,list=[]):
        #print "BAM to flag"
        if len(list)==2:
            bamlist = list
            cmd = str("/home/bnfo620/bin/samtools cat -o "+ self.results + "BAMMERGE.bam " + self.results + bamlist[0] + " " + self.results + bamlist[1])
            self.RunCMD(cmd)
        else:
            bamlist = []
            for bams in os.listdir(self.results):
                bam_len = (len(bams))
                bam_flag = bams[bam_len-3:]
                #print bam_flag
                if bam_flag == 'bam':
                    bamlist.append(bams)
                    if len(bamlist) == 2:
                        cmd = str("/home/bnfo620/bin/samtools merge -nuf"+ self.results + "BAMMERGE.bam " + self.results + bamlist[0] + " " + self.results + bamlist[1])
                        self.RunCMD(cmd)
                        return "Auto BAM MERGER"
            return "Failed to find enout *.bam files for merge"
        return "BAMMERGE_OPS FAILURE!  Missed condition catch"

    def B2S_OPS(self,name):
        merged = self.results+"BAMMERGE.bam"
        cmd = "/home/bnfo620/bin/samtools view -h "+ merged + " " + self.results+name
        self.RunCMD(cmd)
#################################################################################

Genetics = B2_PLAN(Source,Source_Index1,Source_Index2)
if Genetics.BAM_FLAG == 0:
    Genetics.bowtie_OPS(Source_Index1)
    list1 = Genetics.SAM_OPS()
    Genetics.bowtie_OPS(Source_Index2)#needs a rename convention
    list2 = Genetics.SAM_OPS()
    for i in xrange(len(list1)):
        Genetics.BAMMERGE_OPS([list1[i],list2[i]])
        Genetics.B2S_OPS(str(list1[i]+"merge"))
