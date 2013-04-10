#Marco Abreu
from __future__ import division
import subprocess
import sys
import os
import re
import subprocess as sp
Test = True
Source = '/home/bnfo620/M-CAT/sampledata/simulatddata/'
Source_Index1 = '/home/bnfo620/M-CAT/All_Bacteria_1'
Source_Index2 = '/home/bnfo620/M-CAT/All_Bacteria_2'
Results_to = os.getcwd()+"/"
samtools = '/home/bnfo620/bin/samtools'

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
print "Source: ",Source, "\nIndex1", Source_Index1, "\nIndex2", Source_Index2, ""
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
        FILE_EXT = "fastq"

        for filename in os.listdir(self.source):
            L = (len(filename))
            fq_flag = filename[L-len(FILE_EXT):]
            samver1 = filename[:-len(FILE_EXT)-1]+"_I1_bt.sam"
            samver2 = filename[:-len(FILE_EXT)-1]+"_I2_bt.sam"
            check1 = re.search("_bt",filename)
            check2 = True
            check3 = True
            for nemfile in os.listdir(self.results):
                if samver1 == nemfile:
                    check2 = False
                if samver2 == nemfile:
                    check3 = False
            print "Check for","\n\t",filename,"\n\t", "Check1, not bt2 processed:",check1,"\n\t","Check2, no sam version in folder:",check2,"\n\t","Check3, no sam version in folder:",check3
            if fq_flag == FILE_EXT and check1 is None and check2 is True and check3 is True:
                self.SAMFILE = filename[:L-6]+'_bt.sam'
                print "Processing",filename
                #print "NAME",filename, filename[:L-6]
                cmd = str("/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -x " + self.index1 + " -U "+ self.source+filename + " -S " + self.results+filename[:L-6]+'_I1'+'_bt.sam')
                self.RunCMD(cmd)
                if len(self.index2) > 3:
                    cmd = str("/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -x " + self.index2 + " -U "+ self.source+filename + " -S " + self.results+filename[:L-6]+'_I2'+'_bt.sam')
                    self.RunCMD(cmd)
            else:
                print "Found!",samver1,samver2,"Present Bypassing file"

    def SAM_OPS(self):
        #print "SAM to BAM"
        bamrunlist = []
        for sams in os.listdir(self.results):
        #/home/bnfo620/bin/samtools view -bS $SAMFILE > $BAMFILE
            sam_len = (len(sams))
            sam_flag = sams[sam_len-6:]
            #print sam_flag
            if sam_flag == 'bt.sam':
                self.BAMFILE = sams[:sam_len-4]+'.bam'
                bamrunlist.append(self.BAMFILE)
                #print "/home/bnfo620/bin/samtools view -bS",Results_to+SAMFILE, ">",Results_to+BAMFILE
                cmd = samtools +" view -bS " + sams[:len(sams)-6]+'bt.sam' + " > " + self.BAMFILE
                self.RunCMD(cmd)
                self.sortbam(self.BAMFILE)
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

    def BAMMERGE_OPS(self):
        #print "BAM to flag"
        bamlist = []
        for bams in os.listdir(self.results):
            bam_len = (len(bams))
            bam_flag = bams[bam_len-7:]
            #print bam_flag
            #print bams,bam_flag
            if bam_flag == 'srt.bam':
                proto = bams[:bam_len-12]
                #print proto,
                if str(proto+'1_bt_srt.bam')==bams and str(proto+'2_bt_srt.bam') in os.listdir(self.results):
                    #print "pass1"
                    if str(proto[:-1]+'BAMMERGE.bam') not in os.listdir(self.results):
                        cmd = str(samtools+" cat -o "+ self.results + proto[:-1] +"BAMMERGE.bam " + self.results + proto+'1_bt_srt.bam' + " " + self.results +proto+'2_bt_srt.bam')
                        print cmd
                        self.RunCMD(cmd)
                        #return "Auto BAM MERGER"
                    else:
                        print "Previous MERGE present"
                else:
                    print "Non-mergable file, BYPASSING"
        return "Failed to find enout *.bam files for merge"

    def sortbam(self,bam):
        cmd = str(samtools+" sort -on "+ self.results + bam +" abc > "+ self.results + bam[:len(bam)-4] + "_srt.bam")
        self.RunCMD(cmd)

    def B2S_OPS(self):
        for filename in os.listdir(self.results):
            check = re.search("BAMMERGE",filename)
            if check is not None and str(filename[:-12]+"CSAM.sam") not in os.listdir(self.results):
                cmd = samtools+ " view "+ filename + " > " + filename[:-12]+"CSAM.sam"
                self.RunCMD(cmd)
            else:
                print str(filename[:-12]+"CSAM.sam"), 'most likely already exist'
    #################################################################################

Genetics = B2_PLAN(Source,Results_to,Source_Index1,Source_Index2)
Genetics.bowtie_OPS(Source_Index1)
Genetics.SAM_OPS()
Genetics.BAMMERGE_OPS()
Genetics.B2S_OPS()
