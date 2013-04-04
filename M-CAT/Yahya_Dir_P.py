import sys
import os
import bowtie_sample_pipeline as bp

def runSystemCMDQsub(cmd):
    print "Running below command using qsub ..."
    print cmd
    qsub_cmd = "qsub /home/nsheth/qsub_general.sh \'" + cmd + "\'"
    bp.runSystemCMD(qsub_cmd)
    
def main():

    if len(sys.argv) < 3 :
        print "USAGE: python sys.argv[0] input-dir output-dir index \n"
        sys.exit()

    indir = sys.argv[1]
    outdir = sys.argv[2]
    index = sys.argv[3]
    index2 = sys.argv[4]

    filepath = indir
    files = os.listdir(filepath)
    for filename in files:
         if filename.endswith("trimmed.1.fastq"):
            read1 = indir + filename
            read2 = indir + filename.replace("trimmed.1.fastq","trimmed.2.fastq")
            name1 = filename.replace(".denovo_duplicates_marked.trimmed.1.fastq","_index1") 
            name2 = filename.replace(".denovo_duplicates_marked.trimmed.1.fastq","_index2")
            name3 = filename.replace(".denovo_duplicates_marked.trimmed.1.fastq","_m.bam")
            name4 = name3.replace(".bam",".sam")
            

            cmd = "python Yahya_sample_pLine.py " + read1 + " " + read2 + " " + index + " " + name1 + " " + outdir
            runSystemCMDQsub(cmd)
            cmd = "python bowtie_sample_pipe.py " + read1 + " " + read2 + " " + index2 + " " + name2 + " " + outdir
            runSystemCMDQsub(cmd)
            cmd = "/home/bnfo620/bin/samtools cat -o " + name3 + " " + name1 + "_bowtie_sorted.bam " + name2 + "_bowtie_sorted.bam"
            runSystemCMDQsub(cmd)
            cmd = "/home/bnfo620/bin/samtools view -h -o " + name4 + " " + name3
            runSystemCMDQsub(cmd)
 


if __name__ == '__main__':
        main()
        

