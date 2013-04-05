import sys
import os
import seydoux_bowtie_pipeline as bp

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

    filepath = indir
    files = os.listdir(filepath)
    for filename in files:
        if filename.endswith("read1.fastq"): 
            read1 = indir + filename
            read2 = indir + filename.replace("read1","read2") 
            projectname = filename.replace("_read1.fastq","")

            #print read1
            #print read2
            #print projectname

            cmd = "python bowtie_sample_pipeline.py " + read1 + " " + read2 + " " + index + " " + projectname + " " + outdir

            runSystemCMDQsub(cmd)
        
            
            
            


if __name__ == '__main__':
        main()
        


                        
