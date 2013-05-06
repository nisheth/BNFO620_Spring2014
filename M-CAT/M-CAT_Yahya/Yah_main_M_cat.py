import sys
import os
import bowtie_sample_pipeline as bp

def runSystemCMDQsub(cmd):
    print "Running below command using qsub ..."
    print cmd
    qsub_cmd = "qsub /home/nsheth/qsub_general.sh \'" + cmd + "\'"
    bp.runSystemCMD(qsub_cmd)

def runSystemCMD(cmd):
    print cmd
    subprocess.call([cmd],shell=True)

    
def main():
    if len(sys.argv) < 5 :
        print "USAGE: python sys.argv[0] 1-input 2-output-dir 3-index1 4-index2 5-run name 6-bin file name 7-finalOutput \n"
        sys.exit()

    input = sys.argv[1]  
    outdir = sys.argv[2]
    index1 = sys.argv[3]
    index2 = sys.argv[4]
    runName = sys.argv[5]
    bin = sys.argv[6]
    finalOutput=sys.argv[7]


    if input.endswith("1.fastq"):
        projectname = input.replace(".1x.1.fastq","_bowtie_merged.bam")
        read1 = input                                        # XXXXXX.1x.1.fastq
        read2 = input.replace("1.fastq","2.fastq")           # XXXXXX.1x.2.fastq
        name1 = input.replace(".1x.1.fastq","_index1.fastq") # XXXXXX_index1.fastq  
        projectname1 = runName+"_"+name1                     # runname_XXXXXX_index1.fastq
        name2 = input.replace(".1x.1.fastq","_index2.fastq") # XXXXXX_index2.fastq
        projectname2 = runName+"_"+name2                     # runname_XXXXXX_index1.fastq
        mergedSam = projectname.replace(".bam",".sam")       # runname_XXXXXX_bowtie_sorted.sam



            cmd = "/home/bnfo620/bin/samtools view " +outdir+ projectname + " > " + outdir+ merged

            runSystemCMD(cmd)


        cmd = "python Yahya_sample_pLine.py " + read1 + " " + read2 + " " + index1 + " " + projectname1 + " " + outdir
        bp.runSystemCMD(cmd)
        cmd = "python Yahya_sample_pLine.py " + read1 + " " + read2 + " " + index2 + " " + projectname2 + " " + outdir
        bp.runSystemCMD(cmd)
        cmd = "/home/bnfo620/bin/samtools cat -o "+ outdir+ projectname + " " + outdir + projectname1 + "_bowtie_sorted.bam " + outdir + projectname2 + "_bowtie_sorted.bam " 
        bp.runSystemCMD(cmd)
        cmd = "/home/bnfo620/bin/samtools view " +outdir+ projectname + " > " + outdir+ mergedSam
        bp.runSystemCMD(cmd)
        cmd = "python Yah_M_CAT_Final.py " +outdir+ mergedSam + " " + bin + " " + outdir + finalOutput
        bp.runSystemCMD(cmd)





if __name__ == '__main__':
        main()
        

