#Marco Abreu
from __future__ import division
import subprocess
import sys
import os
import re
import subprocess as sp


Results_to = os.getcwd()+"/"
samtools = '/home/bnfo620/bin/samtools'


class B2_PLAN(object):

    def __init__(self,source,results,index1,index2=""):
        self.source = source
        self.results = results
        self.index1 = index1
        self.index2 = index2
        self.tag = '1x.1.fastq'

    def master_run(self):
        for filename in os.listdir(self.source):
            if filename.endswith(self.tag):
                self.bowtie_OPS(filename,self.index1)
                if self.index2 != "":
                    self.bowtie_OPS(filename,self.index2)
                self.SAM_OPS(filename)
                self.BAMMERGE_OPS(filename)
                self.B2S_OPS(filename)

    def RunCMD(self,cmd):
        print cmd
        subprocess.call([cmd],shell = True)

    #Takein arguments from commandline, and run script which runs 3 programs
    def bowtie_OPS(self, filename, index):
        read1 = filename
        read2 = filename.replace(self.tag,"1x.2.fastq" )
        number = index[-1:]
        bamfile1 = read1.replace(self.tag,'_I'+number+'_bt.sam')
        bamfile2 = read2.replace("1x.2.fastq",'_I'+number+'_bt.sam')
        bamfile3 = read1.replace(self.tag,'D_I'+number+'_bt.sam')

        cmd = str("/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -x " + index + " -U "+ self.source+filename + " -S " + self.results+bamfile1)
        self.RunCMD(cmd)

        if read2 in os.listdir(self.source) and read1 != read2:
            cmd = str("/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -x " + index + " -U "+ self.source+filename + " -S " + self.results+bamfile2)
            self.RunCMD(cmd)

            cmd = str("/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -x " + index + " -1 " + self.source+read1 + " -2 " + self.source+read2 +" -S " + self.results+bamfile3)
            self.RunCMD(cmd)

    def SAM_OPS(self,filename):
        #print "SAM to BAM"
        samfileI1 = filename.replace(self.tag,"_I1_bt.sam")
        samfileI2 = filename.replace(self.tag,"_I2_bt.sam")
        samfileDI1 = filename.replace(self.tag,"D_I1_bt.sam")
        samfileDI2 = filename.replace(self.tag,"D_I2_bt.sam")

        if samfileI1 in os.listdir(self.results):
            #samfile = filename
            bamfile = samfileI1.replace('.sam','.bam')
            cmd = samtools +" view -bS " + self.results+samfileI1 + " > " + self.results+bamfile
            self.RunCMD(cmd)
            print "Sending",bamfile
            self.sortbam(bamfile)

        if samfileI2 in os.listdir(self.results):
            #samfileI2 = filename
            bamfile = samfileI2.replace('.sam','.bam')
            cmd = samtools +" view -bS " + self.results+samfileI2 + " > " + self.results+bamfile
            self.RunCMD(cmd)
            print "Sending",bamfile
            self.sortbam(bamfile)

        if samfileDI1 in os.listdir(self.results):
            #samfileI2 = filename
            bamfile = samfileDI1.replace('.sam','.bam')
            cmd = samtools +" view -bS " + self.results+samfileDI1 + " > " + self.results+bamfile
            self.RunCMD(cmd)
            print "Sending",bamfile
            self.sortbam(bamfile)

        if samfileDI2 in os.listdir(self.results):
            #samfileI2 = filename
            bamfile = samfileDI2.replace('.sam','.bam')
            cmd = samtools +" view -bS " + self.results+samfileDI2 + " > " + self.results+bamfile
            self.RunCMD(cmd)
            print "Sending",bamfile
            self.sortbam(bamfile)

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

    def BAMMERGE_OPS(self,filename):
        bamfileI1 = filename.replace(self.tag,"_I1_bt.srt_bam")
        bamfileI2 = filename.replace(self.tag,"_I2_bt.srt_bam")
        bamfileDI1 = filename.replace(self.tag,"D_I1_bt.srt_bam")
        bamfileDI2 = filename.replace(self.tag,"D_I2_bt.srt_bam")

        bammerge = filename.replace(self.tag,"_merge.bam")
        bammergeD = filename.replace(self.tag,"_D_merge.bam")

        if bamfileI2 in os.listdir(self.results) and bamfileI1 in os.listdir(self.results):
            cmd = str(samtools+" cat -o "+ self.results + bammerge + " " + self.results + bamfileI1 + " " + self.results + bamfileI2)
            print cmd
            self.RunCMD(cmd)

        if bamfileDI2 in os.listdir(self.results) and bamfileDI1 in os.listdir(self.results):
            cmd = str(samtools+" cat -o "+ self.results + bammergeD + " " + self.results + bamfileDI1 + " " + self.results + bamfileDI2)
            print cmd
            self.RunCMD(cmd)


    def sortbam(self,bam):
        bam2 = bam.replace('.bam','.srt_bam')
        cmd = str(samtools+" sort -on "+ self.results + bam +" abc > "+ self.results + bam2)
        self.RunCMD(cmd)

    def B2S_OPS(self,filename):
        bammerge = filename.replace(self.tag,"_merge.bam")
        bammergeD = filename.replace(self.tag,"_D_merge.bam")

        merge2 = filename.replace(self.tag,"_D_CSAM.sam")
        merge1 = filename.replace(self.tag,"_CSAM.sam")

        if bammerge in os.listdir(self.results) and merge1 not in os.listdir(self.results):
            cmd = samtools+ " view "+ bammerge + " > " + merge1
            self.RunCMD(cmd)
        if bammergeD in os.listdir(self.results) and merge2 not in os.listdir(self.results):
            cmd = samtools+ " view "+ bammergeD + " > " + merge2
            self.RunCMD(cmd)

     #################################################################################

#Genetics = B2_PLAN(Source,Results_to,Source_Index1,Source_Index2)
#Genetics.bowtie_OPS(Source_Index1)
#Genetics.SAM_OPS()
#Genetics.BAMMERGE_OPS()
#Genetics.B2S_OPS()
#Genetics.master_run()
